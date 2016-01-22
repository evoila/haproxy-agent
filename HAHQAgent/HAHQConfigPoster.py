import requests
import os

from HAHQConfigurator import HAHQConfigurator


class HAHQConfigPoster(object):
    """
    this is a light helper class, to send the config data to a server specified in the config.py file, after converting
    it to json from the HAProxy config file, using the HAHQConfigurator class
    """
    def __init__(self, config_file_path):
        """
        converts the given file to a config dict

        :param config_file_path: the HAProxy config file path
        """
        self.config_timestamp = os.stat(config_file_path).st_mtime
        self.config_string = self.stringify_file(config_file_path)

        if self.config_string:
            self.config_data = HAHQConfigurator(config_string=self.config_string).get_config_data()
        else:
            self.config_data = {'config': []}

    def post_config(self, url, token):
        """
        sends the converted data to the server

        :param url: url of the server
        :param token: token for authentication
        """
        request_data = self.config_data
        request_data['timestamp'] = self.config_timestamp
        requests.post(url, json=request_data)

    def stringify_file(self, file):
        """
        this method returns the content of a file as a string

        :param file: file path
        :return: string
        """
        with open(file, 'r') as config_file:
            return config_file.read()
