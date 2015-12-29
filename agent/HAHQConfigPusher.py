import config
from agent.HAHQConfigurator import HAHQConfigurator


class HAHQConfigPusher(object):
    def __init__(self, config_string):
        self.config_data = HAHQConfigurator(config_string=config_string).get_config_data()

    def push_config(self, url, token):
        print self.config_data


if __name__ == "__main__":
    with open(config.HA_PROXY_CONFIG_PATH, 'r') as config_file:
        config_pusher = HAHQConfigPusher(config_file.read())
        config_pusher.push_config(
            config.SERVER_URL + ':' + config.SERVER_PORT + '/config/' + config.AGENT_ID + '/',
            config.AGENT_TOKEN
        )