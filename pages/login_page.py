# Login page URL
LOGIN_URL = "https://automationexercise.com/login"

def get_email_input(page):
    return page.locator("[data-qa='login-email']")

def get_password_input(page):
    return page.locator("[data-qa='login-password']")

def get_login_button(page):
    return page.locator("[data-qa='login-button']")

def get_home_button(page):
    return page.locator("header li:nth-child(5)")

def get_error_message(page):
    return page.locator("form > input+p")

def get_welcome_message(page):
    return page.locator(".welcome-message")  # Update based on actual page

def get_account_identifier():
    return "/account"  # Update based on actual URL pattern
