"""
class contains method to capture, create log file & update logs
"""
from datetime import datetime, date
import logging
import os
import allure
from selenium.webdriver.common.by import By


class LogGenerator(logging.Handler):
    """used for capturing logs"""
    @staticmethod
    def log(level_name, message):
        """to capture screenshot only for error logs"""
        with allure.step(f"Log ({level_name}) {message}"):
            if level_name.lower() == "error":
                attach_screenshot_in_report()

    def emit(self, record):
        self.log(record.levelname, record.getMessage())


def get_logger():
    """method to set log level, format, and generate log file"""
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    allure_handler = LogGenerator()
    file_handler = logging.FileHandler(os.path.join("logs", 'dsp.log'))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(allure_handler)
    return logger


def attach_screenshot_in_report():
    """attach allure screenshot"""
    driver = logging.FileHandler.selenium_driver
    current_date_time = str(f'({(date.today().strftime("%d %b"))} {(datetime.now().strftime("%H_%M_%S"))})')
    screenshot_path = os.path.join(os.path.abspath(__file__ + '/../../'),
                                   f"screenshots/{current_date_time}.png")
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    driver.find_element(By.TAG_NAME, 'body').screenshot(screenshot_path)
    allure.attach.file(source=screenshot_path, attachment_type=allure.attachment_type.PNG, name="Screenshot")