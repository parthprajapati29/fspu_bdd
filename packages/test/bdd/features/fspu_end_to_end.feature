Feature: User perform the survey
  Scenario: User perform email submit & enter pii1
    Given Browser is opened and user opens the test link
    When User enters the email and click on the continue button
    Then User enters first name
    Then User enters last name
    Then User enters phone number and click on the continue button
    Then User enters street name
    Then User enters zipcode
    Then User select male gender
    Then User select date of birth and click on continue button
    Then Validate the survey page is displayed
    Then User perform survey positively
    And User validate iconfirm and click on checkbox
    And User validates the thankyou page