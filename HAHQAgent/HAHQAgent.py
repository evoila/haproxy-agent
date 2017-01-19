from HAHQConfigGetter import HAHQConfigGetter
from HAHQConfigPoster import HAHQConfigPoster
from HAHQHeartbeatDaemon import HAHQHeartbeatDaemon
from HAHQRabbitMQClient import HAHQRabbitMQClient


class HAHQAgent(object):
    """
    this class wraps all the functionality of the HAProxyHQ/Agent into one class
    """

    def __init__(self,
                 server_url,
                 agent_id,
                 agent_token,
                 rabbit_mq_host,
                 rabbit_mq_port,
                 rabbit_mq_virtual_host,
                 rabbit_mq_exchange,
                 rabbit_mq_username,
                 rabbit_mq_password,
                 config_file_path):
        """
        initializes the agent with the configs needed

        :param server_url: the url to the HAProxyHQ/Backend
        :param agent_id: the ID of this agent
        :param agent_token: the token the agents needs for authentication
        :param rabbit_mq_host: the adress of the RabbitMQ server
        :param rabbit_mq_port: the RabbitMQ servers port
        :param rabbit_mq_virtual_host: virtual host on RabbitMQ server
        :param rabbit_mq_exchange: the RabbitMQ exchange
        :param rabbit_mq_username: username for the virtual host on RabbitMQ server
        :param rabbit_mq_password: password for the virtual host on RabbitMQ server
        :param config_file_path: the path to the config file
        """
        self.server_url = server_url
        self.agent_id = agent_id
        self.agent_token = agent_token
        self.rabbit_mq_host = rabbit_mq_host
        self.rabbit_mq_port = rabbit_mq_port
        self.rabbit_mq_virtual_host = rabbit_mq_virtual_host
        self.rabbit_mq_exchange = rabbit_mq_exchange
        self.rabbit_mq_username = rabbit_mq_username
        self.rabbit_mq_password = rabbit_mq_password
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
        retrieves the current config from the backend. In case the local config
        is newer than the one retrieved by the backend, the local config is
        pushed to the server.

        params are just dummies, so that this method can be called as an AMQ
        callback
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

    def __start_rabbit_mq_client_loop(self):
        """
        starts the RabbitMQ client in a loop
        """
        HAHQRabbitMQClient(
            'haproxyhq/agent-' + self.agent_id,
            self.rabbit_mq_host,
            self.rabbit_mq_port,
            self.rabbit_mq_virtual_host,
            self.rabbit_mq_exchange,
            self.rabbit_mq_username,
            self.rabbit_mq_password,
            self.get_config
        ).connect()

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
        self.__start_rabbit_mq_client_loop()
