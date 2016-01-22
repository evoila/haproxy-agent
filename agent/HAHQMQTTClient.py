import paho.mqtt.client as mqtt

class HAHQMQTTClient(object):
    def _init_mqtt_client(self, host, port, topic, func_on_message):
        self.host = host
        self.port = port
        self.topic = ''
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = func_on_message

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(self.topic)

    def connect(self):
        self.client.connect(self.host, self.port)
        self.client.loop_forever()