import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

sender = os.getenv("EMAIL_SENDER")
receiver = os.getenv("EMAIL_RECEIVER")
password = os.getenv("EMAIL_PASSWORD")

if not all([sender, receiver, password]):
    raise ValueError("Missing required environment variables: EMAIL_SENDER, EMAIL_RECEIVER, or EMAIL_PASSWORD")

testrail_url = os.getenv("TESTRAIL_RUN_URL", "#")
github_url = os.getenv("GITHUB_RUN_URL", "#")

msg = MIMEMultipart("alternative")
msg["Subject"] = "🚀 CI Run Summary: Playwright + TestRail"
msg["From"] = sender if sender is not None else ""
msg["To"] = receiver if receiver is not None else ""

html = f"""
<html>
  <body>
    <h3>✅ Playwright Test Execution Completed</h3>
    <p>
      <strong>TestRail Run:</strong> <a href="{testrail_url}">{testrail_url}</a><br>
      <strong>GitHub Workflow:</strong> <a href="{github_url}">{github_url}</a><br>
    </p>
    <p>
      Please check TestRail for detailed test results and GitHub for logs.
    </p>
  </body>
</html>
"""

msg.attach(MIMEText(html, "html"))

try:
    # Ensure sender, receiver, and password are not None (already checked above, but for type checkers)
    assert sender is not None
    assert receiver is not None
    assert password is not None

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
