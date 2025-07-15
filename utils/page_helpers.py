from playwright.sync_api import Page


def wait_for_page_load(page: Page) -> None:
    """Wait for page to be fully loaded (DOM and network idle)."""
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle") 