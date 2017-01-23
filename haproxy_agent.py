import os
import time
from sys import argv
from threading import Thread

import pika
import requests

import config


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


class HAHQConfigGetter(object):
    """
    this is a light helper class, to retrieve the config data from a server
    specified in the config.py file and convert the config data to a config
    string using the HAHQConfigurator, to then save it to the HAProxy config
    file
    """

    def __init__(self, url, token, config_file_path):
        """
        the data is retrieved and converted as soon as the object is
        initialized. It needs a token for authentication

        :param url: the server url the data is retrieved from
        :param token: a token for authentication
        :param config_file_path: path to the HAProxy config file
        """
        self.config_file_path = config_file_path
        response_data = requests.get(url, headers={
            'X-Auth-Token': token
        }).json()
        self.config_data = response_data['haProxyConfig']
        self.config_timestamp = response_data['configTimestamp']
        self.config_string = HAHQConfigurator(
            config_data=self.config_data).get_config_string()

    def save_config(self):
        """
        saves the converted config string to the HAProxy config file and reloads
        HAProxy
        """
        with open(self.config_file_path, 'w') as config_file:
            config_file.write(self.config_string)

        os.system('service haproxy reload')


class HAHQConfigPoster(object):
    """
    this is a light helper class, to send the config data to a server specified
    in the config.py file, after converting it to json from the HAProxy config
    file, using the HAHQConfigurator class
    """

    def __init__(self, config_file_path):
        """
        converts the given file to a config dict

        :param config_file_path: the HAProxy config file path
        """
        self.config_timestamp = int(os.stat(config_file_path).st_mtime * 1000)
        self.config_string = self.stringify_file(config_file_path)

        if self.config_string:
            self.config_data = HAHQConfigurator(
                config_string=self.config_string).get_config_data()
        else:
            self.config_data = {
                'config': []
            }

    def post_config(self, url, token):
        """
        sends the converted data to the server

        :param url: url of the server
        :param token: token for authentication
        """
        request_data = {
            'haProxyConfig': self.config_data,
            'configTimestamp': self.config_timestamp,
            'agentHeartbeatTimestamp': int(round(time.time() * 1000)),
        }
        if os.popen('service haproxy status').read() == 'haproxy is running.\n':
            request_data['haproxyHeartbeatTimestamp'] = request_data[
                'agentHeartbeatTimestamp']
        requests.patch(url, json=request_data, headers={
            'X-Auth-Token': token
        })

    def stringify_file(self, file):
        """
        this method returns the content of a file as a string

        :param file: file path
        :return: string
        """
        with open(file, 'r') as config_file:
            return config_file.read()


class HAHQConfigurator(object):
    """
    This class helps converting a config dict to a string which has the format
    of the HAProxy config file.

    Converting works bi-directional.

    SECTION_KEYWORDS is a list of keywords indicating the begin of a section in
    the HAProxy config file
    """

    SECTION_KEYWORDS = [
        'global',
        'defaults',
        'frontend',
        'backend',
        'listen',
        'peers',
        'mailers',
        'userlist',
        'namespace_list',
        'resolvers',
    ]

    def __init__(self, config_data=None, config_string=None):
        """
        a HAHQConfigurator can be initialized either with a dict describing the
        config, or a string formatted like the config file.

        :param config_data: dict with config data
        :param config_string: string in config file format
        """
        self.config_data = config_data if config_data else None
        self.config_string = config_string if config_string else None

    def __str__(self):
        return self.get_config_string()

    def __dir__(self):
        return self.get_config_data()

    def __eq__(self, other):
        if not isinstance(other, HAHQConfigurator) or \
                        self.get_config_data() != other.get_config_data():
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_config_string(self):
        """
        returns the config as string and converts it to string, in case it's
        only available as a dict

        :return: config string
        """
        if not self.config_string:
            self.__build_config_string()

        return self.config_string

    def get_config_data(self):
        """
        returns the config data as a dict and converts it to dict, in case it's
        only available as a string

        :return: config data
        """
        if not self.config_data:
            self.__build_config_data()

        return self.config_data

    def __build_config_string(self):
        """
        builds the config string from config data
        """
        self.config_string = ''

        if self.config_data:
            for section in self.config_data['sections']:
                self.config_string += section['section']['type'] + ' ' + \
                                      section['section']['name'] + '\n'

                for value in section['values']:
                    self.config_string += '\t' + value + '\n'

                self.config_string += '\n'

    def __build_config_data(self):
        """
        builds the config data from config string
        """
        if self.config_string:
            self.config_data = {
                'sections': []
            }

            section = None

            for line in self.config_string.split('\n'):
                words = line.split()

                if len(words) > 0 and words[0][0] != '#':
                    if words[0] in self.SECTION_KEYWORDS:
                        if section:
                            self.config_data['sections'].append(section)

                        section = {
                            'section': {
                                'type': words[0],
                                'name': ' '.join(words[1:]),
                            },
                            'values': [],
                        }
                    else:
                        if section:
                            section['values'].append(' '.join(words))

            if section:
                self.config_data['sections'].append(section)


class HAHQConfiguredAgentInstance(object):
    """
    this class is a wrapper for an instance of a HAHQAgent with the config from
    the config.py
    """

    def __init__(self):
        self.agent = HAHQAgent(
            config.SERVER_URL,
            config.AGENT_ID,
            config.AGENT_TOKEN,
            config.RABBIT_MQ_HOST,
            config.RABBIT_MQ_PORT,
            config.RABBIT_MQ_VIRTUAL_HOST,
            config.RABBIT_MQ_EXCHANGE,
            config.RABBIT_MQ_USERNAME,
            config.RABBIT_MQ_PASSWORD,
            config.HA_PROXY_CONFIG_PATH
        )

    def start_agent(self):
        """
        starts the agent
        """
        print 'HAProxyHQ/Agent started'
        self.agent.start_agent()

    def get_config(self):
        """
        gets the config
        """
        self.agent.get_config()
        print 'HAProxyHQ/Agent pulled from server'

    def post_config(self):
        """
        posts the config
        """
        self.agent.post_config()
        print 'HAProxyHQ/Agent pushed to server'


class HAHQHeartbeatDaemon(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.agent = HAHQConfiguredAgentInstance()

    def run(self):
        while (True):
            self.agent.post_config()
            time.sleep(60)


class HAHQRabbitMQClient(object):
    """
    this is a wrapper class for the paho RabbtMQ python client, for the purposes
    of the HAProxyHQ/Agent
    """

    def __init__(self, client_id, rabbit_mq_host, rabbit_mq_port, rabbit_mq_virtual_host,
                 rabbit_mq_exchange, rabbit_mq_username, rabbit_mq_password, func_on_message):
        """
        initializes the client with required information and a callback function

        :param rabbit_mq_host: the adress fo the RabbitMQ server
        :param rabbit_mq_port: the RabbitMQ servers port
        :param rabbit_mq_virtual_host: the vhost on the server
        :param rabbit_mq_exchange: the topic this agent will subscribe to
        :param rabbit_mq_username: the username of the vhost
        :param rabbit_mq_password: the password of the vhost
        :param func_on_message: the callback function which will be called every
        time a message is received
        """
        self.rabbit_mq_host = rabbit_mq_host
        self.rabbit_mq_port = rabbit_mq_port
        self.rabbit_mq_exchange = rabbit_mq_exchange
        self.client_id = client_id
        self.func_on_message = func_on_message

        self.rabbit_mq_username = rabbit_mq_username
        self.rabbit_mq_password = rabbit_mq_password
        self.rabbit_mq_virtual_host = rabbit_mq_virtual_host
        self.channel = None

    def connect(self):
        """
        connects the client and goes into a loop. Be aware, that this is a
        blocking command
        """
        credentials = None

        if self.rabbit_mq_username is not None:
            credentials = pika.PlainCredentials(
                username=self.rabbit_mq_username,
                password=self.rabbit_mq_password,
            )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbit_mq_host,
                port=self.rabbit_mq_port,
                virtual_host=self.rabbit_mq_virtual_host,
                credentials=credentials,
            )
        )
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=self.rabbit_mq_exchange,
                                      auto_delete=False,
                                      type='direct')
        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.rabbit_mq_exchange,
                                queue=queue_name,
                                routing_key=self.rabbit_mq_exchange)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(consumer_callback=self.func_on_message,
                                   queue=queue_name, no_ack=True)


if __name__ == '__main__':
    try:
        agent = HAHQConfiguredAgentInstance()

        if '--push' in argv:
            agent.post_config()
        elif '--pull' in argv:
            agent.get_config()
        else:
            agent.start_agent()
    except KeyboardInterrupt:
        print 'HAProxyHQ/Agent stopped'
        exit(0)
