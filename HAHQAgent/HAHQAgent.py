from HAHQHeartbeatDaemon import HAHQHeartbeatDaemon
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
        :param mqtt_topic: the MQTT topic
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

    def get_config(self, client=None, userdata=None, msg=None):
        """
        retrieves the current config from the backend. In case the local config is newer than the one retrieved by the
        backend, the local config is pushed to the server.

        params are just dummies, so that this method can be called as an MQTT callback
        """
        config_getter = HAHQConfigGetter(
            self.server_url,
            self.agent_token,
            self.config_file_path
        )

        config_poster = HAHQConfigPoster(self.config_file_path)

        if config_getter.config_timestamp > config_poster.config_timestamp:
            if config_getter.config_data != config_poster.config_data:
                config_getter.save_config()
        else:
            if config_getter.config_data != config_poster.config_data:
                config_poster.post_config(
                    self.server_url,
                    self.agent_token
                )

    def __start_mqtt_client_loop(self):
        """
        starts the MQTT client in a loop
        """
        HAHQMQTTClient(
            'haproxyhq/agent-' + self.agent_id,
            self.mqtt_broker_adress,
            self.mqtt_broker_port,
            self.mqtt_topic,
            self.get_config
        ).connect()

    def __start_file_watcher_daemon(self):
        """
        starts the HAHQFileWatcherDaemon
        """
        HAHQFileWatcherDaemon(self.config_file_path).start()

    def __start_heartbeat_daemon(self):
        """
        starts the HAHQHeartbeatDaemon
        """
        HAHQHeartbeatDaemon().start()

    def start_agent(self):
        """
        starts the agent. This is blocking!
        """
        self.__start_heartbeat_daemon()
        self.__start_file_watcher_daemon()
        self.__start_mqtt_client_loop()
