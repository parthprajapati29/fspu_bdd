"""to read the config.ini"""
from configparser import ConfigParser
import os


class ReadProperty:
    """methods to read the config.ini & sharing credentials w.r.t HR Portal"""

    def read_config(self, key):
        """method to return the config file"""
        config = ConfigParser()
        config_path = os.path.join('configuration', 'config.ini')
        config.read(config_path)
        return config.get(self, key)

    @staticmethod
    def environment_ssp_url():
        """to return the environment url"""
        environment = ReadProperty.read_config("configuration", "environment")
        return ReadProperty.read_config(environment, "ssp_url")

    @staticmethod
    def environment_details():
        """to return the environment"""
        if ReadProperty.read_config("configuration", "pipeline") == "True":
            environment = os.getenv("ENVIRONMENT_NAME")
            return environment
        environment = ReadProperty.read_config("configuration", "environment")
        return environment

    @staticmethod
    def environment_hr_url():
        """to return the environment url"""
        environment = ReadProperty.read_config("configuration", "environment")
        return ReadProperty.read_config(environment, "hr_url")

    @staticmethod
    def get_user_id():
        """to return the HR credentials details from environment variable """
        user_id = os.getenv('USER_ID')
        return user_id

    @staticmethod
    def get_pwd():
        """to return the HR credentials details from environment variable """
        password = os.getenv('PASSWORD')
        return password
