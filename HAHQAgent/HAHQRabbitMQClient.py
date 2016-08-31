import pika


class HAHQRabbitMQClient(object):
    """
    this is a wrapper class for the paho RabbtMQ python client, for the purposes
    of the HAProxyHQ/Agent
    """

    def __init__(self, client_id, rabbit_mq_host, rabbit_mq_port,
                 rabbit_mq_exchange, func_on_message):
        """
        initializes the client with required information and a callback function

        :param rabbit_mq_host: the adress fo the RabbitMQ server
        :param rabbit_mq_port: the RabbitMQ servers port
        :param rabbit_mq_exchange: the topic this agent will subscribe to
        :param func_on_message: the callback function which will be called every
        time a message is received
        """
        self.rabbit_mq_host = rabbit_mq_host
        self.rabbit_mq_port = rabbit_mq_port
        self.rabbit_mq_exchange = rabbit_mq_exchange
        self.client_id = client_id
        self.func_on_message = func_on_message

        # TODO: Insert credentials
        # self.rabbit_mq_username = rabbit_mq_username
        # self.rabbit_mq_password = rabbit_mq_password
        # self.rabbit_mq_virtual_host = rabbit_mq_virtual_host
        self.channel = None

    def connect(self):
        """
        connects the client and goes into a loop. Be aware, that this is a
        blocking command
        """
        credentials = None

        # TODO: See above
        # if self.rabbit_mq_username is not None:
        #    credentials = pika.PlainCredentials(
        #        username=self.rabbit_mq_username,
        #        password=self.rabbit_mq_password,
        #    )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbit_mq_host,
                port=self.rabbit_mq_port,
                # virtual_host=self.rabbit_mq_virtual_host,
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
