import os
import time
from sys import argv
from threading import Thread

import pika
import requests

import config


def callback(channel=None, method=None, properties=None, body=None):
    """
            retrieves the current config from the backend. In case the local config
            is newer than the one retrieved by the backend, the local config is
            pushed to the server.

            params are just dummies, so that this method can be called as an AMQ
            callback
            """
    response_data = requests.get(SERVER_URL, headers={
        'X-Auth-Token': AGENT_TOKEN
    }).json()
    config_data = response_data['haProxyConfig']
    config_timestamp = response_data['configTimestamp']
    config_string = HAHQConfigurator(
        config_data=config_data).get_config_string()
    if config_timestamp > get_local_config_timestamp:
        if config_data != get_local_config_data:
            with open(CONFIG_FILE_PATH, 'w') as config_file:
                config_file.write(config_string)
    else:
        if config_data != get_local_config_data:
            post_config()
    os.system('service haproxy reload')


def connect_to_rabbit_mq():
    """
    connects the client and goes into a loop. Be aware, that this is a
    blocking command
    """
    credentials = None

    if RABBIT_MQ_USERNAME is not None:
        credentials = pika.PlainCredentials(
            username=RABBIT_MQ_USERNAME,
            password=RABBIT_MQ_PASSWORD,
        )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBIT_MQ_HOST,
            port=RABBIT_MQ_PORT,
            virtual_host=RABBIT_MQ_VIRTUAL_HOST,
            credentials=credentials,
        )
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=RABBIT_MQ_EXCHANGE,
                             auto_delete=False,
                             type='direct')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=RABBIT_MQ_EXCHANGE,
                       queue=queue_name,
                       routing_key=RABBIT_MQ_EXCHANGE)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(consumer_callback=callback,
                          queue=queue_name, no_ack=True)
    channel.start_consuming()


def get_local_config_data():
    """

    :return: The content of the local haproxy.cfg
    """
    config_string = stringify_file(CONFIG_FILE_PATH)
    if config_string:
        return HAHQConfigurator(config_string=config_string).get_config_data()
    else:
        return {
            'config': []
        }


def get_local_config_timestamp():
    """

    :return: The timestamp of last modification from the local haproxy.cfg
    """
    return int(os.stat(CONFIG_FILE_PATH).st_mtime * 1000)


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

            section = dict()

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
                        if bool(section):
                            section['values'].append(' '.join(words))

            if bool(section):
                self.config_data['sections'].append(section)


class HAHQHeartbeatDaemon(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        while True:
            post_config()
            time.sleep(60)

def post_config():
    """
    sends the converted data to the server

    """
    config_timestamp = get_local_config_timestamp()
    config_data = get_local_config_data

    request_data = {
        'haProxyConfig': config_data,
        'configTimestamp': config_timestamp,
        'agentHeartbeatTimestamp': int(round(time.time() * 1000)),
    }
    if os.popen('service haproxy status').read() == 'haproxy is running.\n':
        request_data['haproxyHeartbeatTimestamp'] = request_data[
            'agentHeartbeatTimestamp']
    requests.patch(SERVER_URL, json=request_data, headers={
        'X-Auth-Token': AGENT_TOKEN
    })


def stringify_file(stringable_file):
    """
    this method returns the content of a file as a string

    :param stringable_file: file path
    :return: string
    """
    with open(stringable_file, 'r') as config_file:
        return config_file.read()


if __name__ == '__main__':
    try:
        SERVER_URL = config.SERVER_URL
        AGENT_ID = config.AGENT_ID
        AGENT_TOKEN = config.AGENT_TOKEN
        RABBIT_MQ_HOST = config.RABBIT_MQ_HOST
        RABBIT_MQ_PORT = config.RABBIT_MQ_PORT
        RABBIT_MQ_VIRTUAL_HOST = config.RABBIT_MQ_VIRTUAL_HOST
        RABBIT_MQ_EXCHANGE = config.RABBIT_MQ_EXCHANGE
        RABBIT_MQ_USERNAME = config.RABBIT_MQ_USERNAME
        RABBIT_MQ_PASSWORD = config.RABBIT_MQ_PASSWORD
        CONFIG_FILE_PATH = config.HA_PROXY_CONFIG_PATH

        if '--push' in argv:
            post_config()
        elif '--pull' in argv:
            callback()
        else:
            HAHQHeartbeatDaemon().start()
            connect_to_rabbit_mq()
    except KeyboardInterrupt:
        print 'HAProxyHQ/Agent stopped'
        exit(0)
