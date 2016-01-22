from HAHQMQTTClient import HAHQMQTTClient
from HAHQFileWatcherDaemon import HAHQFileWatcherDaemon
from HAHQConfigGetter import HAHQConfigGetter
from HAHQConfigPoster import HAHQConfigPoster

class HAHQAgent(object):
    """
    this class wraps all the functionality of the HAProxyHQ/Agent into one class
    """
    def __init__(self,
                 server_url,
                 agent_id,
                 agent_token,
                 mqtt_broker_adress,
                 mqtt_broker_port,
                 mqtt_topic,
                 config_file_path):
        """
        initializes the agent with the configs needed

        :param server_url: the url to the HAProxyHQ/Backend
        :param agent_id: the ID of this agent
        :param agent_token: the token the agents needs for authentication
        :param mqtt_broker_adress: the adress if the MQTT broker
        :param mqtt_broker_port: the MQTT brokers port
        :param mqtt_topi: the MQTT topic
        :param config_file_path: the path to the config file
        """
        self.server_url = server_url
        self.agent_id = agent_id
        self.agent_token = agent_token
        self.mqtt_broker_adress = mqtt_broker_adress
        self.mqtt_broker_port = mqtt_broker_port
        self.mqtt_topic = mqtt_topic
        self.config_file_path = config_file_path

    def post_config(self):
        """
        posts the config using the HAHQConfigPoster
        """
        config_poster = HAHQConfigPoster(config_file_path=self.config_file_path)
        config_poster.post_config(
            self.server_url,
            self.agent_token
        )

    def get_config(self):
        """
        retrieves the current config from the backend
        """
        config_getter = HAHQConfigGetter(
            self.server_url,
            self.agent_token
        )
        config_getter.save_config()

    def __start_mqtt_client_loop(self):
        """
        starts the MQTT client in a loop
        """
        HAHQMQTTClient(self.mqtt_broker_adress, self.mqtt_broker_port, self.mqtt_topic, self.get_config)

    def __start_file_watcher_daemon(self):
        """
        starts the HAHQFileWatcherDaemon
        """
        HAHQFileWatcherDaemon(self.config_file_path).start()

    def start_agent(self):
        self.post_config()
        self.__start_file_watcher_daemon()
        self.__start_mqtt_client_loop()