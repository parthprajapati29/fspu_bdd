"""
This class contains generic methods to be called in other pages,
and is called in the steps definition file
"""

import os
import re
import string
import time
from datetime import datetime
from pathlib import Path
import random
from random import randint
import subprocess
import yaml

from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common.base import AppiumOptions
from appium import webdriver as appium_webdriver

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utilities.read_config import ReadProperty
from utilities import custom_logger
logger = custom_logger.get_logger()


class BasePage:
    """contains the generic methods that has to be used for the page actions methods"""

    def __init__(self, driver):
        self.driver = driver

    """ Mobile applications elements which are commonly used in the BasePage """

    message_list_count_xpath = '(//android.widget.TextView[@resource-id="com.samsung.android.messaging:id' \
                               '/content_text_view"])'
    delete_button_element_id = AppiumBy.ACCESSIBILITY_ID, 'Delete'
    delete_all_button_element_classname = AppiumBy.CLASS_NAME, 'android.widget.Button'
    delete_select_all_button_element = 'com.samsung.android.messaging:id/bubble_all_select_checkbox'
    delete_select_all_button_element_id = AppiumBy.ID, 'com.samsung.android.messaging:id/bubble_all_select_checkbox'
    move_to_recycle_bin_id = AppiumBy.ID, 'android:id/button1'
    Firefox_app_id = AppiumBy.ACCESSIBILITY_ID, 'Firefox'
    Authenticator_xpath = AppiumBy.XPATH, '//android.view.View[@text=\"Open in Microsoft Authenticator app \"]'
    Authenticator_open_xpath = AppiumBy.XPATH, '//android.widget.Button[@resource-id="android:id/button1"]'
    Authenticator_wallet_id = AppiumBy.ACCESSIBILITY_ID, 'Open in Microsoft Authenticator wallet'
    Authenticator_open_wallet_id = AppiumBy.ID, 'android:id/button1'
    mobile_clear_notifications_ID = AppiumBy.ACCESSIBILITY_ID, "Clear,Button"
    mobile_clear_notifications_xpath = AppiumBy.XPATH, ('//android.widget.TextView['
                                                        '@resource-id="com.android.systemui:id/clear_all"]')

    """Delete Message elements updated """
    message_back_button_id = AppiumBy.ID, 'com.samsung.android.messaging:id/composer_up_button_touch_layout'
    message_lists_count_xpath = '(//android.widget.RelativeLayout[' \
                                '@resource-id="com.samsung.android.messaging:id/card_view_list_item"])'
    delete_menu_option_id = AppiumBy.ID, 'com.samsung.android.messaging:id/sesl_action_bar_overflow_button'
    delete_button_xpath = AppiumBy.XPATH, '//android.widget.TextView[@resource-id=\"com.samsung.android.messaging:id' \
                                          '/title\" and @text=\"Delete\"]'
    select_all_message_id = AppiumBy.ID, 'com.samsung.android.messaging:id/select_all_wrapper'
    delete_all_message_id = AppiumBy.ACCESSIBILITY_ID, 'Delete all'
    recycle_bin_id = AppiumBy.ID, 'android:id/button1'
    Authenticator_open_wallet_xpath = AppiumBy.XPATH, "//android.widget.Button[@resource-id=\"android:id/button1\"]"

    def open_browser_mobile(self):
        """Open browser based on the browser and run the appium server"""
        if ReadProperty.read_config("configuration", "browser_mobile") == 'firefox':
            options = AppiumOptions()
            options.load_capabilities({
                "platformName": "Android",
                "appium:platformVersion": "14.0",
                "appium:deviceName": "Galaxy A23 5G",
                "appium:automationName": "UIAutomator2",
                "appium:appPackage": 'org.mozilla.firefox',
                "appium:appActivity": 'org.mozilla.fenix.HomeActivity',
                "appium:firefoxOptions": {
                    'args': ['--disable-popup-blocking']
                }
            })
            appium_server_url = 'http://127.0.0.1:4723'
            self.driver = appium_webdriver.Remote(appium_server_url, options=options)
            logger.info("Browser is open")
            return self.driver
        if ReadProperty.read_config("configuration", "browser_mobile") == 'edge':
            options = AppiumOptions()
            options.load_capabilities({
                "platformName": "Android",
                "appium:platformVersion": "14.0",
                "appium:deviceName": "Galaxy A23 5G",
                "appium:automationName": "UIAutomator2",
                "appium:appPackage": 'com.microsoft.emmx',
                "appium:appActivity": 'org.chromium.chrome.browser.ChromeTabbedActivity',
                'appium:chromeOptions': {
                    'args': ['--disable-popup-blocking', '--disable-notifications'],
                    'noReset': True
                }
            })
            appium_server_url = 'http://127.0.0.1:4723'
            self.driver = appium_webdriver.Remote(appium_server_url, options=options)
            logger.info("Browser is open")
            return self.driver
        logger.info("Not able to open browser.")
        raise ValueError("Browser is not supported")

    def open_browser_web(self):
        """open the browser as per the config.ini file"""
        headless_option = ReadProperty.read_config("configuration", "headless")
        if ReadProperty.read_config("configuration", "browser_web") == 'chrome':
            options = webdriver.ChromeOptions()
            options.use_chromium = True
            options.add_argument("--no-sandbox")
            options.add_argument("start-maximized")
            options.add_argument("ignore-certificate-errors")
            if headless_option == 'True':
                options.add_argument("--headless")
            # To avoid undesired logging on console
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            # Set the interceptor on the driver
            self.driver = webdriver.Chrome(options=options)
            self.driver.set_page_load_timeout(60)
            logger.info("Chrome Browser is open")
            return self.driver
        if ReadProperty.read_config("configuration", "browser_web") == 'edge':
            edge_options = webdriver.EdgeOptions()
            edge_options.use_chromium = True
            edge_options.add_argument('--ignore-certificate-errors')
            edge_options.add_argument("start-maximized")
            if headless_option == 'True':
                edge_options.add_argument("--headless")
            self.driver = webdriver.Edge(service=EdgeService(
                EdgeChromiumDriverManager().install()),
                options=edge_options)
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(600)
            logger.info("Edge Browser is open.")
            return self.driver
        logger.info("Not able to open browser.")
        raise ValueError("Browser is not supported")

    def load_run_appium_server(self):
        """ run the appium server"""
        options = AppiumOptions()
        options.load_capabilities({
            "platformName": "Android",
            "appium:platformVersion": "14.0",
            "appium:deviceName": "Galaxy A23 5G",
            "appium:automationName": "UIAutomator2",
        })
        appium_server_url = 'http://127.0.0.1:4723'
        self.driver = appium_webdriver.Remote(appium_server_url, options=options)
        logger.info("Appium is running")
        return self.driver

    def open_dsp_ss_portal_application_url(self):
        """invoke the browser and open SSP Portal URL."""
        try:
            self.driver.get(ReadProperty.environment_ssp_url())
            logger.info("DSP SSP application URL is open.")
            return self.driver
        except InvalidSelectorException:
            logger.error("DSP SSP application URL is not open.")
            self.driver.close()
            assert False, "Test is failed in open login page section"

    def open_lander_application_url(self):
        """invoke the browser and open HR Portal URL."""
        try:
            self.driver.get(ReadProperty.environment_hr_url())
            logger.info("DSP HR application URL is open.")
            return self.driver
        except InvalidSelectorException:
            logger.error("DSP HR application URL is not open.")
            self.driver.close()
            assert False, "Test is failed in open login page section"

    def close_browser(self):
        """close the current instance of browser"""
        self.driver.close()
        logger.info("Browser is closed.")

    def navigate_url(self, value):
        """ Navigate to the standalone URL as required"""
        self.driver.get(value)
        logger.info("URL is opened.")

    def open_mobile_notifications(self):
        """ Invoke the mobile notification panel in mobile """
        self.driver.open_notifications()

    def custom_clear_all_notifications(self):
        """User clicks on clear notification button"""
        self.user_defined_wait(2)
        self.open_mobile_notifications()
        if self.verify_element_displayed(self.mobile_clear_notifications_xpath):
            self.click_element(self.mobile_clear_notifications_xpath, "Click")

    def click_element(self, by_locator, objname=None):
        """click the element"""
        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(by_locator)
            )
            element.click()
            logger.info("%s is clicked", objname)
        except InvalidSelectorException:
            logger.error("Exception! Can't click on the element %s", objname)

    def click_element_wait(self, by_bojtype, by_locator, objname=None):
        """clicks the element passed as by_locator"""
        try:
            element = self.driver.find_element(by_bojtype, by_locator)
            element.click()
            logger.info("%s is clicked", objname)
        except InvalidSelectorException:
            logger.error("Exception! Can't click on the element %s", objname)

    def type_element(self, by_locator, text):
        """types the passed text into the web element"""
        try:
            WebDriverWait(self.driver,
                          30).until(EC.presence_of_element_located(by_locator)).send_keys(text)
            logger.info("Value entered is: %s for field.", text)
        except InvalidSelectorException:
            logger.error("Exception! Can't type on the element")

    def get_title(self, title):
        """returned title of the driver (current url)"""
        try:
            WebDriverWait(self.driver, 30).until(EC.title_contains(title))
            logger.info("Title is : %s", self.driver.title)
            return self.driver.title
        except InvalidSelectorException:
            logger.error("Exception! Can't find page title")
            return "Can't find page title"

    def read_value_from_element(self, by_locator):
        """returns the value of .text property of a web element"""
        try:
            element = WebDriverWait(self.driver,
                                    30).until(EC.presence_of_element_located(by_locator))
            logger.info("Element value is : %s", element.text)
            return element.text
        except InvalidSelectorException:
            logger.info("Exception! Can't read value from element")
            return "Can't read value from element"

    def get_element_attribute(self, by_locator, attribute_name):
        """returns the value of requested attribute of the requested element"""
        try:
            element = WebDriverWait(self.driver,
                                    30).until(EC.presence_of_element_located(by_locator))
            text = element.get_attribute(attribute_name)
            return text
        except InvalidSelectorException:
            logger.error("Exception! Can't find attribute of element")
            return "Can't find attribute of element"

    def verify_element_displayed(self, by_locator):
        """checks if the element is displayed"""
        try:
            element = WebDriverWait(self.driver,
                                    60).until(EC.presence_of_element_located(by_locator))
            return element
        except InvalidSelectorException:
            logger.error("Element not found")
            return "Element not found"

    def send_keys_photo(self, by_objtype, by_locator, by_type, by_full_locator):
        """sets photo path based on value of by_type parameter(photo-change or add-photo) """
        if by_type == "create":
            photo_name = "addPhoto.png"
        else:
            photo_name = "change-photo.jpg"
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(by_full_locator))
        elem = self.driver.find_element(by_objtype, by_locator)
        photo_path = os.path.join("pages/profile_picture", photo_name)
        path = os.path.abspath(photo_path)
        elem.send_keys(path)

    def clear_text_field_data(self, by_bojtype, by_locator):
        """clears existing text from the web elements"""
        self.driver.find_element(by_bojtype, by_locator).click()
        self.driver.find_element(by_bojtype, by_locator).send_keys(Keys.CONTROL + "a")
        self.driver.find_element(by_bojtype, by_locator).send_keys(Keys.DELETE)

    def clear_text_field_data_with_wait(self, by_locator):
        """waits for web-element to load then clears existing text from the web elements"""
        elem = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(by_locator))
        elem.click()
        elem.send_keys(Keys.CONTROL + "a")
        elem.send_keys(Keys.DELETE)

    def is_selected(self, by_locator):
        """checks if element is selected"""
        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator))
            element.is_enabled()
            logger.info("Element is enabled and clickable")
        except InvalidSelectorException:
            logger.info("Exception! Can't click on the element %s")
            return False

    def switch_to_new_tab(self):
        """Switching to new tab"""
        original_window = self.driver.current_window_handle
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

    @staticmethod
    def file_name_generation(file_status):
        """returns format for filename"""
        date_time = datetime.now()
        year = date_time.year
        month = date_time.month
        day = date_time.day
        hour = date_time.hour
        minute = date_time.minute
        sec = date_time.second
        date_today = f"{year}-{month}-{day}-{hour}-{minute}-{sec}"
        if file_status == "PASS":
            file_name = str("Pass_" + date_today + ".png")
            return file_name
        if file_status == "FAIL":
            file_name = str("Fail_" + date_today + ".png")
            return file_name
        file_name = str("Unknown_" + date_today + ".png")
        return file_name

    def take_screenshot(self, status):
        """take screenshot and save"""
        file_path = str(Path("screenshots"))
        file_name = str(BasePage.file_name_generation(status))
        screenshots_file_path = os.path.join(file_path, file_name)
        self.driver.get_screenshot_as_file(screenshots_file_path)

    @staticmethod
    def save_data_into_yaml_file(value, filename):
        """to save data to datafile"""
        try:
            file_path = os.path.join("data", filename)
            path = os.path.abspath(file_path)
            save_data = {"OTP": {"code": value}}
            with open(path, "w", encoding="utf-8") as f_f:
                yaml.safe_dump(save_data, f_f)
        except yaml.YAMLError as exception:
            logger.warning(exception)

    @staticmethod
    def save_link_into_yaml_file(value, filename):
        """to save data to datafile"""
        try:
            file_path = os.path.join("data", filename)
            path = os.path.abspath(file_path)
            save_data = {"ACCESS": {"link": value}}
            with open(path, "w", encoding="utf-8") as f_f:
                yaml.safe_dump(save_data, f_f)
        except yaml.YAMLError as exception:
            logger.warning(exception)

    @staticmethod
    def get_test_data(page, field, filename):
        """to read test data"""
        try:
            file_path = os.path.join("data", filename)
            path = os.path.abspath(file_path)
            with open(path, 'r', encoding="utf-8") as f_f:
                doc = yaml.safe_load(f_f)
        except yaml.YAMLError as exception:
            logger.warning(exception)
        return doc[page][field]

    def get_element_count(self, by_obj_type, by_locator):
        """to get the number of elements """
        element_count = len(self.driver.find_elements(by_obj_type, by_locator))
        return element_count

    def list_of_web_elements(self, by_obj_type, by_locator):
        """to get list of web elements"""
        elements = self.driver.find_elements(by_obj_type, by_locator)
        return elements

    def read_text_from_element(self, by_obj_type, by_locator):
        """returns the value of .text property of a web element"""
        try:
            text = self.driver.find_element(by_obj_type, by_locator).text
            logger.info("Element value is : %s", text)
            return text
        except InvalidSelectorException:
            logger.info("Exception! Can't read value from element")
            return "Can't read value from element"

    def verify_element_visible(self, by_obj_type, by_locator, objname=None):
        """verify the element"""
        time.sleep(3)
        try:
            self.driver.find_element(by_obj_type, by_locator).is_displayed()
            logger.info("Exception! Object is visible: %s", objname)
            return True
        except NoSuchElementException:
            logger.info("Object is not visible: %s", objname)
            return False

    def verify_element_enabled(self, by_obj_type, by_locator, objname=None):
        """verify the element"""
        time.sleep(3)
        try:
            self.driver.find_element(by_obj_type, by_locator).is_enabled()
            logger.info("Exception! Object is visible: %s", objname)
            return True
        except NoSuchElementException:
            logger.info("Object is not visible: %s", objname)
            return False

    def verify_element_selected(self, by_obj_type, by_locator):
        """verify the element is selected"""
        try:
            element = self.driver.find_element(by_obj_type, by_locator)
            return element.is_selected()
        except NoSuchElementException:
            logger.info(f"Element not found using {by_obj_type} with locator '{by_locator}'.")
            return None

    @staticmethod
    def org_data_details():
        """get org details"""
        env_name = ReadProperty.environment_details()
        if env_name == "preprod":
            return "FindOrgPreprod"
        return "FindOrgLT"

    @staticmethod
    def get_random_email_string():
        """get random email ids """
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(10))
        return result_str + "@nhs.net"

    @staticmethod
    def generate_phone_number():
        """get random phone number"""
        range_begin = 10 ** (10 - 1)
        range_end = (10 ** 10) - 1
        phone_number = randint(range_begin, range_end)
        return str(phone_number)

    def small_wait_to_complete(self, by_locator):
        """checks if the success element is displayed using small wait"""
        try:
            element = WebDriverWait(self.driver,
                                    180).until(EC.visibility_of_element_located(by_locator))
            return element
        except InvalidSelectorException:
            logger.error("Element not found")
            return "Element not found"

    def select_static_dropdown_element(self, by_bojtype: object, by_locator: object, text: object) -> object:
        """select from the static dropdown by passing the locator & value"""
        try:
            dropdown = Select(self.driver.find_element(by_bojtype, by_locator))
            dropdown.select_by_value(text)
            logger.info("%s is selected", text)
        except InvalidSelectorException:
            logger.error("Exception! Can't select on the element %s", text)

    def scroll_page_to_bottom(self):
        """Function to scroll down the page"""
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def complete_close_browser(self):
        """close the instance of browser"""
        self.user_defined_wait(3)
        self.driver.quit()
        logger.info("Event is closed.")

    @staticmethod
    def user_defined_wait(sleep_seconds):
        """To be called when next action is not immediate"""
        time.sleep(sleep_seconds)

    def select_checkbox(self, by_bojtype, by_locator, objname=None):
        """select checkbox"""
        self.driver.find_element(by_bojtype, by_locator).is_selected()
        try:
            self.driver.find_element(by_bojtype, by_locator).click()
        except NoSuchElementException:
            logger.error("Exception! Can't click on the element %s", objname)

    @staticmethod
    def extract_verification_code(email_text_body):
        """Split the email body by whitespace to extract words """

        words = email_text_body.split()

        # Look for a 6-digit code (adjust if the code length is different)
        for word in words:
            if word.isdigit() and len(word) == 6:
                return word

        # If no 6-digit code is found, return None
        return None

    @staticmethod
    def extract_one_time_passcode(sms_text_body):
        """Implement your logic to extract the one-time passcode from SMS """
        passcode = None
        for word in sms_text_body.split():
            if word.isdigit() and len(word) == 6:
                passcode = word
                break
        return passcode

    @staticmethod
    def extract_links_from_text(text):
        """Regular expression to find URLs in the text"""
        url_pattern = re.compile(r'https?://\S+')

        # Find all matches in the text
        links = re.findall(url_pattern, text)
        return links

    def open_ms_authenticator(self):
        """Invoking the MS Authenticator"""
        if self.verify_element_displayed(self.Authenticator_xpath):
            self.click_element(self.Authenticator_xpath, "Click")
            self.user_defined_wait(5)

        if self.verify_element_displayed(self.Authenticator_open_xpath):
            self.click_element(self.Authenticator_open_xpath, "Click")
            self.user_defined_wait(5)

    def open_ms_authenticator_wallet(self):
        """Adding the credentials to MS Authenticator"""
        if self.verify_element_displayed(self.Authenticator_wallet_id):
            self.click_element(self.Authenticator_wallet_id, "Click")
            self.user_defined_wait(5)

        if self.verify_element_displayed(self.Authenticator_open_wallet_id):
            self.click_element(self.Authenticator_open_wallet_id, "Click")
            self.user_defined_wait(5)

    def qr_code_click_openms_inbuilt(self):
        """Adding the credentials to MS Authenticator"""
        if self.verify_element_displayed(self.Authenticator_open_wallet_xpath):
            self.user_defined_wait(3)
            self.click_element(self.Authenticator_open_wallet_xpath, "Click")
            self.user_defined_wait(5)

    def delete_sms_messages_old(self):
        """Logic to delete SMS messages from the mobile """
        message_count = self.get_element_count("xpath", self.message_list_count_xpath)
        if message_count > 1:
            self.click_element(self.delete_button_element_id, "Click")
            self.user_defined_wait(2)
            self.click_element(self.delete_select_all_button_element_id, "Click")
            self.user_defined_wait(2)
            self.click_element(self.delete_all_button_element_classname, "Click")
            self.user_defined_wait(2)
            self.click_element(self.move_to_recycle_bin_id, "Click")
        else:
            self.click_element(self.delete_button_element_id, "Click")
            self.user_defined_wait(2)
            self.click_element(self.delete_all_button_element_classname, "Click")
            self.user_defined_wait(2)
            self.click_element(self.move_to_recycle_bin_id, "Click")

    def delete_sms_messages(self):
        """Logic to delete SMS messages from the mobile """
        self.user_defined_wait(2)
        self.click_element(self.message_back_button_id)
        self.user_defined_wait(2)
        message_count = self.get_element_count("xpath", self.message_lists_count_xpath)
        if message_count > 1:
            self.click_element(self.delete_menu_option_id, "Click")
            self.user_defined_wait(2)
            self.click_element(self.delete_button_xpath, "Click")
            self.user_defined_wait(2)
            self.click_element(self.select_all_message_id, "Click")
            self.user_defined_wait(2)
            self.click_element(self.delete_all_message_id, "Click")
            self.user_defined_wait(2)
            self.click_element(self.recycle_bin_id, "Click")
            self.user_defined_wait(2)
        else:
            self.click_element(self.delete_menu_option_id, "Click")
            self.user_defined_wait(2)
            self.click_element(self.delete_button_xpath, "Click")
            self.user_defined_wait(2)
            self.click_element(self.delete_all_message_id, "Click")
            self.user_defined_wait(2)
            self.click_element(self.recycle_bin_id, "Click")
            self.user_defined_wait(2)

    def mobile_menu_out_button(self):
        """ Click on Menu Button """
        self.driver.press_keycode(3)

    def mobile_back_button(self):
        """ Click on Back Button """
        self.driver.press_keycode(4)

    def navigate_back_mobile_browser(self):
        """ Logic to navigate to mobile web browser """
        self.driver.press_keycode(3)
        if self.verify_element_displayed(self.Firefox_app_id):
            self.click_element(self.Firefox_app_id, "Click")
            self.user_defined_wait(5)

    def mobile_webpage_scroll_down_small(self):
        """ Method to scroll down through mobile web-pages - small scroll """
        self.scroll_down_mobile_webpage(100, 100, 200, 300, 3.0)

    def mobile_webpage_scroll_down_medium(self):
        """ Method to scroll down through mobile web-pages - medium scroll """
        self.scroll_down_mobile_webpage(100, 100, 200, 400, 3.0)

    def mobile_webpage_scroll_down_large(self):
        """ Method to scroll down through mobile web-pages - large scroll """
        self.scroll_down_mobile_webpage(100, 100, 200, 600, 3.0)

    def mobile_webpage_scroll_down_extra_large(self):
        """ Method to scroll down through mobile web-pages - extra large scroll """
        self.scroll_down_mobile_webpage(100, 100, 200, 700, 3.0)

    def scroll_down_mobile_webpage(self, left, top, width, height, percent):
        """ Logic to scroll down through mobile web-pages"""
        self.driver.execute_script('mobile: scrollGesture', {
            'left': left, 'top': top, 'width': width, 'height': height,
            'direction': 'down',
            'percent': percent
        })
        logger.info("Scroll down feature")

    def mobile_webpage_scroll_up_large(self):
        """ Method to scroll up through mobile web-pages - medium scroll """
        self.scroll_up_mobile_webpage(0, 500, 500, 800, 3.0)

    def scroll_up_mobile_webpage(self, left, top, width, height, percent):
        """ Logic to scroll up through mobile web-pages"""
        self.driver.execute_script('mobile: scrollGesture', {
            'left': left, 'top': top, 'width': width, 'height': height,
            'direction': 'up',
            'percent': percent
        })
        logger.info("Scroll up feature")

    @staticmethod
    def start_appium():
        """ Function to start appium server"""
        command = 'appium -p 4723'
        appium_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10)
        stdout, stderr = appium_process.communicate(timeout=5)
        if stderr:
            print(f"Appium stderr: {stderr.decode()}")
        if stdout:
            print(f"Appium stdout: {stdout.decode()}")

    @staticmethod
    def kill_browser():
        """ Function to kill browser process"""
        command = 'taskkill /F /IM "chrome.exe"'
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=True)
        process.communicate()

    def scroll_page_to_middle(self):
        """This will scroll to specific element present on the page"""
        self.driver.execute_script("window.scrollBy(0, 1000);")

    def scroll_page_to_top(self):
        """This will scroll to specific element present on the page"""
        self.driver.execute_script("window.scrollBy(0, -1300);")

    def change_element_bg_color(self, by_bojtype, by_locator):
        element = self.driver.find_element(by_bojtype, by_locator)
        return self.driver.execute_script("arguments[0].style.backgroundColor = 'lightgreen';", element)

    def scroll_small_mobile_page_click_element(self, by_obj_type, by_locator):
        i = 10
        while i > 2:
            self.mobile_webpage_scroll_down_small()
            try:
                if self.verify_element_visible(by_obj_type, by_locator):
                    self.click_element_wait(by_obj_type, by_locator)
                    break
            except NoSuchElementException:
                print("Element not found, scrolling down...")
            i -= 1

    def scroll_large_mobile_page_click_element(self, by_obj_type, by_locator):
        i = 10
        while i > 2:
            self.mobile_webpage_scroll_down_large()
            try:
                if self.verify_element_visible(by_obj_type, by_locator):
                    self.click_element_wait(by_obj_type, by_locator)
                    break
            except NoSuchElementException:
                print("Element not found, scrolling down...")
            i -= 1

    def scroll_mobile_page_type_element(self, by_obj_type, by_locator, value):
        i = 10
        while i > 2:
            self.mobile_webpage_scroll_down_small()
            try:
                if self.driver.find_element(by_obj_type, by_locator):
                    self.driver.find_element(by_obj_type, by_locator).send_keys(value)
                    break
            except NoSuchElementException:
                print("Element not found, scrolling down...")
            i -= 1

    def scroll_page_to_small(self):
        """This will scroll to specific element present on the page"""
        self.driver.execute_script("window.scrollBy(0, 500);")
