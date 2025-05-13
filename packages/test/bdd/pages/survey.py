from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from utilities import custom_logger

logger = custom_logger.get_logger()


class SurveyPage(BasePage):
    """DOM of survey page"""
    answer_easy_question_xpath = By.XPATH, "//div[@class=\"grid\"]/h2"
    answer_easy_question_txt = By.XPATH, "Answer a few easy questions"
    select_first_option = By.XPATH, "//label[@class=\"opt\"][1]"
    i_confirm_xpath = By.XPATH, "//label[@id=\"iconfirm\"]/div"
    i_confirm_txt = "I CONFIRM"
    tcpa_continue_xpath = By.XPATH, "//button[@id=\"entersweep\"]/span"
    signup_completed_xpath = By.XPATH, "//h1[contains(text(),'Signup Completed!')]"
    signup_completed_txt = "SIGNUP COMPLETED!"

    def validate_title_text(self):
        """validate the title"""
        self.verify_element_displayed(self.answer_easy_question_xpath)
        message = self.read_value_from_element(self.answer_easy_question_xpath)
        assert message in self.answer_easy_question_txt

    def answer_positively(self):
        """Answer positive"""
        for i in range(15):
            try:
                if self.verify_element_displayed(self.select_first_option):
                    self.click_element(self.select_first_option)
                    self.user_defined_wait(2)
            except Exception as e:
                print("No option found")
                break

    def i_confirm(self):
        """validate the i confirm"""
        self.verify_element_displayed(self.i_confirm_xpath)
        message = self.read_value_from_element(self.i_confirm_xpath)
        assert message in self.i_confirm_txt
        self.click_element(self.i_confirm_xpath)
        self.click_element(self.tcpa_continue_xpath)

    def validate_thankyou(self):
        """validate thankyou page"""
        self.verify_element_displayed(self.signup_completed_xpath)
        message = self.read_value_from_element(self.signup_completed_xpath)
        assert message in self.signup_completed_txt
        self.close_browser()
