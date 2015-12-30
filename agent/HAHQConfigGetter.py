import requests

import config
from agent.HAHQConfigurator import HAHQConfigurator


class HAHQConfigGetter(object):
    def __init__(self, url, token):
        self.config_data = requests.get(url).json()
        self.config_string = HAHQConfigurator(config_data=self.config_data).get_config_string()

    def save_config(self):
        print self.config_string
        # with open(config.HA_PROXY_CONFIG_PATH, 'w') as config_file:
        #     config_file.write(self.config_string)



if __name__ == "__main__":
    config_getter = HAHQConfigGetter(
        config.SERVER_URL,
        config.AGENT_TOKEN
    )
    config_getter.save_config()