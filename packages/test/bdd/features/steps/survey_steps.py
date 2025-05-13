import logging

from behave import given, when, then
from pages.base_page import BasePage
from pages.survey import SurveyPage


@then("Validate the survey page is displayed")
def validate_survey_page(context):
    context.survey_page = SurveyPage(context.driver)
    context.survey_page.validate_title_text()


@then("User perform survey positively")
def perform_survey_positive(context):
    context.survey_page.answer_positively()


@then("User validate iconfirm and click on checkbox")
def validate_i_confirm(context):
    context.survey_page.i_confirm()


@then("User validates the thankyou page")
def validate_thankyou_page(context):
    context.survey_page.validate_thankyou()