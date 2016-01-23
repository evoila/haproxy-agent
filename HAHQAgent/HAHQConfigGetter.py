import os

import requests

from HAHQConfigurator import HAHQConfigurator


class HAHQConfigGetter(object):
    """
    this is a light helper class, to retrieve the config data from a server specified in the config.py file and convert
    the config data to a config string using the HAHQConfigurator, to then save it to the HAProxy config file
    """
    def __init__(self, url, token, config_file_path):
        """
        the data is retrieved and converted as soon as the object is initialized. It needs a token for authentication

        :param url: the server url the data is retrieved from
        :param token: a token for authentication
        :param config_file_path: path to the HAProxy config file
        """
        self.config_file_path = config_file_path
        response_data = requests.get(url).json()
        self.config_data = {'configTimestamp': response_data['config']}
        self.config_timestamp = response_data['configTimestamp']
        self.config_string = HAHQConfigurator(config_data=self.config_data).get_config_string()

    def save_config(self):
        """
        saves the converted config string to the HAProxy config file and reloads HAProxy
        """
        with open(self.config_file_path, 'w') as config_file:
            config_file.write(self.config_string)


