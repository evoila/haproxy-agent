import paho.mqtt.client as mqtt


class HAHQMQTTClient(object):
    """
    this is a wrapper class for the paho MQTT python client, for the purposes of the HAProxyHQ/Agent
    """
    def __init__(self, host, port, topic, func_on_message):
        """
        initializes the client with required information and a callback function

        :param host: the adress fo the MQTT broker
        :param port: the MQTT brokers port
        :param topic: the topic this agent will subscribe to
        :param func_on_message: the callback function which will be called every time a message is received
        """
        self.host = host
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = func_on_message

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(self.topic)

    def connect(self):
        """
        connects the client and goes into a loop. Be aware, that this is a blocking command
        """
        self.client.connect(self.host, self.port)
        self.client.loop_forever()
