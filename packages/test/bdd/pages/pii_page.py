from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from utilities import custom_logger

logger = custom_logger.get_logger()


class PiiPage(BasePage):
    """POM for pii page"""
    first_name_xpath = By.XPATH, "//input[@id=\"firstName\"]"
    last_name_xpath = By.XPATH, "//input[@name=\"userLname\"]"
    phone_name_xpath = By.XPATH, "//input[@id=\"phoneNumber\"]"
    pii_continue_button_xpath = By.XPATH, '(//span[normalize-space()=\'Continue\'])[1]'
    street_name_xpath = By.XPATH, "//input[@id=\"address\"]"
    zipcode_xpath = By.XPATH, "//input[@id=\"zipcode\"]"
    gender_xpath = By.XPATH, "//label[@for=\"male\"]"
    dobmonth_xpath = By.XPATH, "//select[@name=\"dobmonth\"]"
    dobdate_xpath = By.XPATH, "//select[@name=\"dobdate\"]"
    dobyear_xpath = By.XPATH, "//select[@name=\"dobyear\"]"
    jan_xpath = By.XPATH, "//option[text()=\"Jan\"]"
    date_xpath = By.XPATH, "//option[text()=\"02\"]"
    year_xpath = By.XPATH, "//option[text()=\"1993\"]"

    def enter_first_name(self, value):
        """enter first name"""
        if self.verify_element_displayed(self.first_name_xpath):
            self.type_element(self.first_name_xpath, value)

    def enter_last_name(self, value):
        """enter first name"""
        if self.verify_element_displayed(self.last_name_xpath):
            self.type_element(self.last_name_xpath, value)

    def enter_mobile_name(self, value):
        """enter first name"""
        if self.verify_element_displayed(self.phone_name_xpath):
            self.type_element(self.phone_name_xpath, value)
            self.user_defined_wait(2)
            self.click_element(self.pii_continue_button_xpath)

    def enter_street_name(self, value):
        """enter street name"""
        self.user_defined_wait(5)
        if self.verify_element_displayed(self.street_name_xpath):
            self.type_element(self.street_name_xpath, value)
            self.user_defined_wait(2)

    def enter_zipcode_name(self, value):
        """enter zipcode"""
        if self.verify_element_displayed(self.zipcode_xpath):
            self.type_element(self.zipcode_xpath, value)
            self.user_defined_wait(2)

    def enter_gender_name(self):
        """enter gender"""
        if self.verify_element_displayed(self.gender_xpath):
            self.click_element(self.gender_xpath)
            self.user_defined_wait(2)

    def enter_dobmonth(self):
        """enter dob month"""
        if self.verify_element_displayed(self.dobmonth_xpath):
            self.click_element(self.dobmonth_xpath)
            self.click_element(self.jan_xpath)
            self.user_defined_wait(2)

    def enter_dobdate(self):
        """enter dob date"""
        if self.verify_element_displayed(self.dobdate_xpath):
            self.click_element(self.dobdate_xpath)
            self.click_element(self.date_xpath)
            self.user_defined_wait(2)

    def enter_dobyear(self):
        """enter dobdate"""
        if self.verify_element_displayed(self.dobyear_xpath):
            self.click_element(self.dobyear_xpath)
            self.click_element(self.year_xpath)
            self.user_defined_wait(2)
            self.click_element(self.pii_continue_button_xpath)
