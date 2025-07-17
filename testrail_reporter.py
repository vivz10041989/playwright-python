import os
import re
import requests
from dotenv import load_dotenv
from junitparser import JUnitXml
from typing import cast

# Load secrets from .env
load_dotenv()

# Fetch and validate TestRail credentials
TESTRAIL_URL = os.getenv("TESTRAIL_URL")
USERNAME = os.getenv("TESTRAIL_USERNAME")
API_KEY = os.getenv("TESTRAIL_API_KEY")
PROJECT_ID = os.getenv("TESTRAIL_PROJECT_ID")
RESULTS_FILE = "results.xml"

# ✅ Type safety checks
missing_vars = []
if TESTRAIL_URL is None:
    missing_vars.append("TESTRAIL_URL")
if USERNAME is None:
    missing_vars.append("TESTRAIL_USERNAME")
if API_KEY is None:
    missing_vars.append("TESTRAIL_API_KEY")
if PROJECT_ID is None:
    missing_vars.append("TESTRAIL_PROJECT_ID")

if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

BASE_API = f"{TESTRAIL_URL}/index.php?/api/v2"
HEADERS = {"Content-Type": "application/json"}


def extract_case_ids(name: str) -> list[int]:
    """Extract TestRail case IDs like C1234 from scenario/test name"""
    return [int(match[1:]) for match in re.findall(r"[cC]\d+", name)]



def parse_junit_results(xml_path: str) -> tuple[list[dict], list[int]]:
    """Parse JUnit XML and build TestRail-compatible result objects"""
    xml = JUnitXml.fromfile(xml_path)
    results = []
    case_ids = []

    for suite in xml:
        for case in suite:
            name = case.name  # should contain "C1234"
            ids = extract_case_ids(name)
            if not ids:
                continue

            if not case.result:
                status = 1  # Passed
            elif any(getattr(r, "_tag", None) == "skipped" for r in case.result):
                status = 2  # Blocked
            elif any(getattr(r, "_tag", None) in ["failure", "error"] for r in case.result):
                status = 5  # Failed
            else:
                status = 5

            case_id = ids[0]  # assume one case ID per test

            results.append({
                "case_id": case_id,
                "status_id": status,
                "comment": f"Result from GitHub Actions: {'PASSED' if status == 1 else 'FAILED'}"
            })

            case_ids.append(case_id)

    return results, list(set(case_ids))


def create_test_run(case_ids: list[int]) -> int:
    """Create a TestRail test run with the matched case IDs"""
    payload = {
        "name": "Automated Test Run from GitHub Actions",
        "include_all": False,
        "case_ids": case_ids
    }
    response = requests.post(
        f"{BASE_API}/add_run/{PROJECT_ID}",
        json=payload,
        auth=(cast(str, USERNAME), cast(str, API_KEY)),
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()["id"]


def post_results(run_id: int, results: list[dict]) -> None:
    """Post test results to the created TestRail run"""
    payload = {"results": results}
    response = requests.post(
        f"{BASE_API}/add_results_for_cases/{run_id}",
        json=payload,
        auth=(cast(str, USERNAME), cast(str, API_KEY)),
        headers=HEADERS
    )
    response.raise_for_status()


def close_test_run(run_id: int) -> None:
    """Close the test run (this may trigger email if enabled)"""
    response = requests.post(
        f"{BASE_API}/close_run/{run_id}",
        auth=(cast(str, USERNAME), cast(str, API_KEY)),
        headers=HEADERS
    )
    response.raise_for_status()


def main():
    print("📥 Parsing JUnit XML test results...")
    results, case_ids = parse_junit_results(RESULTS_FILE)

    if not results:
        print("❌ No valid TestRail case IDs (e.g. C1234) found in test results.")
        return

    print(f"🚀 Creating test run for {len(case_ids)} test case(s)...")
    run_id = create_test_run(case_ids)

    print(f"📤 Posting {len(results)} test result(s) to TestRail run ID: {run_id}...")
    post_results(run_id, results)

    print(f"✅ Closing TestRail run ID: {run_id}...")
    close_test_run(run_id)

    print("🎉 Test results successfully uploaded to TestRail!")


if __name__ == "__main__":
    main()
