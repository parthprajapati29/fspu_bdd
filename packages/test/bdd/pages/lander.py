from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from utilities import custom_logger

logger = custom_logger.get_logger()


class landerPage(BasePage):

    """POM for lander page"""
    enter_your_email_text_xpath = By.XPATH, "(//h4[normalize-space()=\"Enter your email\"])[1]"
    enter_your_email_txt = 'Enter your email'
    input_email_xpath = By.XPATH, '//input[@type="email"]'
    email_continue_button_xpath = By.XPATH, '(//span[normalize-space()=\'Continue\'])[1]'

    def open_lander_page(self):
        """Open test link is browser"""
        self.open_lander_application_url()
        self.user_defined_wait(5)
        if self.verify_element_displayed(self.enter_your_email_text_xpath):
            message = self.read_value_from_element(self.enter_your_email_text_xpath)
            assert message in self.enter_your_email_txt

    def enter_email_click_continue(self, value):
        """Enter email"""
        if self.verify_element_displayed(self.input_email_xpath):
            self.type_element(self.input_email_xpath, value)
        if self.verify_element_displayed(self.email_continue_button_xpath):
            self.click_element(self.email_continue_button_xpath)
