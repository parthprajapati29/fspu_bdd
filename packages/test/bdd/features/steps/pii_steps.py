import logging

from behave import given, when, then
from pages.base_page import BasePage
from pages.pii_page import PiiPage


@then("User enters first name")
def user_enter_first_name(context):
    context.pii_page = PiiPage(context.driver)
    context.pii_page.enter_first_name(BasePage.get_test_data("PiiData", "Fname", "test_data.yaml"))


@then("User enters last name")
def user_enter_last_name(context):
    context.pii_page.enter_last_name(BasePage.get_test_data("PiiData", "Lname", "test_data.yaml"))


@then("User enters phone number and click on the continue button")
def user_enter_phone_name(context):
    context.pii_page.enter_mobile_name(BasePage.get_test_data("PiiData", "Phone", "test_data.yaml"))


@then("User enters street name")
def user_enter_street_name(context):
    context.pii_page.enter_street_name(BasePage.get_test_data("PiiData", "Street", "test_data.yaml"))


@then("User enters zipcode")
def user_enter_zipcode_name(context):
    context.pii_page.enter_zipcode_name(BasePage.get_test_data("PiiData", "Zipcode", "test_data.yaml"))


@then("User select male gender")
def user_enter_gender_name(context):
    context.pii_page.enter_gender_name()


@then("User select date of birth and click on continue button")
def user_enter_dob(context):
    context.pii_page.enter_dobmonth()
    context.pii_page.enter_dobdate()
    context.pii_page.enter_dobyear()
