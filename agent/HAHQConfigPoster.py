import requests

import config
from agent.HAHQConfigurator import HAHQConfigurator


class HAHQConfigPoster(object):
    """
    this is a light helper class, to send the config data to a server specified in the config.py file, after converting
    it to json from the HAProxy config file, using the HAHQConfigurator class
    """
    def __init__(self, config_string):
        """
        converts the given string data to a config dict

        :param config_string: the HAProxy config file as string
        """
        self.config_data = HAHQConfigurator(config_string=config_string).get_config_data()

    def push_config(self, url, token):
        """
        sends the converted data to the server

        :param url: url of the server
        :param token: token for authentication
        """
        print self.config_data
        requests.post(url, json=self.config_data)


if __name__ == "__main__":
    with open(config.HA_PROXY_CONFIG_PATH, 'r') as config_file:
        config_pusher = HAHQConfigPoster(config_file.read())
        config_pusher.push_config(
            config.SERVER_URL,
            config.AGENT_TOKEN
        )
