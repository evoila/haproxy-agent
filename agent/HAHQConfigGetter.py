import config
from agent.HAHQConfigurator import HAHQConfigurator


class HAHQConfigGetter(object):
    def __init__(self, url, token):
        self.config_data = {"config": [{"backend": [{"_name": "servers"}]},{"backend": [{"_name": "mybackend"},{"mode": "tcp"},{"stick-table": "type ip size 20k peers mypeers"}]},{"peers": [{"_name": "mypeers"},{"peer": "haproxy1 192.168.0.1:1024"},{"peer": "haproxy2 192.168.0.2:1024"},{"peer": "haproxy3 10.2.0.1:1024"}]}],}
        self.config_string = HAHQConfigurator(config_data=self.config_data).get_config_string()

    def save_config(self):
        print self.config_string
        # with open(config.HA_PROXY_CONFIG_PATH, 'w') as config_file:
        #     config_file.write(self.config_string)



if __name__ == "__main__":
    config_getter = HAHQConfigGetter(
        config.SERVER_URL + ':' + config.SERVER_PORT + '/config/' + config.AGENT_ID + '/',
        config.AGENT_TOKEN
    )
    config_getter.save_config()