Feature: Login Functionality for Automation Exercise Website

  Background:
    Given The user is on the Login page
    
  @smoke
  Scenario: C2313 - Successful login with valid credentials
    When The user enters valid email 
    And The user enters valid password 
    And The user clicks the login button
    Then The user should be redirected to the account page


  Scenario: C2314 - Unsuccessful login with invalid email
    When The user enters invalid email 
    And The user enters valid password 
    And The user clicks the login button
    Then An error message "Your email or password is incorrect!" should be displayed

  Scenario: C2315 - Unsuccessful login with invalid password
    When The user enters valid email 
    And The user enters invalid password 
    And The user clicks the login button
    Then An error message "Your email or password is incorrect!" should be displayed 