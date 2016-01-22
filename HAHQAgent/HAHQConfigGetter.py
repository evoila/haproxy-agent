import requests

import config
from HAHQConfigurator import HAHQConfigurator


class HAHQConfigGetter(object):
    """
    this is a light helper class, to retrieve the config data from a server specified in the config.py file and convert
    the config data to a config string using the HAHQConfigurator, to then save it to the HAProxy config file
    """
    def __init__(self, url, token):
        """
        the data is retrieved and converted as soon as the object is initialized. It needs a token for authentication

        :param url: the server url the data is retrieved from
        :param token: a token for authentication
        """
        self.config_data = requests.get(url).json()
        self.config_string = HAHQConfigurator(config_data=self.config_data).get_config_string()

    def save_config(self):
        """
        saves the converted config string to the HAProxy config file
        """
        with open(config.HA_PROXY_CONFIG_PATH, 'w') as config_file:
            config_file.write(self.config_string)