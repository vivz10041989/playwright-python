import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from data.test_credentials import CREDENTIALS
from pages.login_page import LOGIN_URL, get_email_input, get_password_input, get_login_button, get_error_message, get_welcome_message, get_home_button

# Import the feature file
scenarios('../../features/login.feature')

@given('The user is on the Login page')
def navigate_to_login(page):
    page.goto(LOGIN_URL)
    get_email_input(page).wait_for(state="visible")
    assert page.url == LOGIN_URL

@when('The user enters valid email')
def enter_valid_email(page):
    get_email_input(page).fill(CREDENTIALS['valid']['email'])

@when('The user enters invalid email')
def enter_invalid_email(page):
    get_email_input(page).fill(CREDENTIALS['invalid']['email'])

@when('The user enters valid password')
def enter_valid_password(page):
    get_password_input(page).fill(CREDENTIALS['valid']['password'])

@when('The user enters invalid password')
def enter_invalid_password(page):
    get_password_input(page).fill(CREDENTIALS['invalid']['password'])

@when('The user clicks the login button')
def click_login(page):
    get_login_button(page).click()


@then('The user should be redirected to the account page')
def verify_account_page(page):
    assert get_home_button(page).inner_text().strip() == "Logout"

@then(parsers.parse('An error message "{message}" should be displayed'))
def verify_error_message(page, message):
    error_element = get_error_message(page)
    error_element.wait_for(state="visible")
    actual_message = error_element.inner_text()
    assert message in actual_message, f"Expected error message '{message}' but got '{actual_message}'" 