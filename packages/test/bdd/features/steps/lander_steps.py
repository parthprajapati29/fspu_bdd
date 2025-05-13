import logging

from behave import given, when
from pages.base_page import BasePage
from pages.lander import landerPage


@given("Browser is opened and user opens the test link")
def open_test_link_in_browser(context):
    """Step file to open browser"""
    context.driver = logging.FileHandler.selenium_driver = landerPage.open_browser_web(context)
    context.lander = landerPage(context.driver)
    context.lander.open_lander_page()


@when("User enters the email and click on the continue button")
def enter_email_and_continue(context):
    context.lander = landerPage(context.driver)
    context.lander.enter_email_click_continue(BasePage.get_test_data("PiiData", "Email", "test_data.yaml"))
