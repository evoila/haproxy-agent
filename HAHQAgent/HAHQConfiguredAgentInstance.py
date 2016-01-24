import config
import HAHQAgent


class HAHQConfiguredAgentInstance(object):
    """
    this class is a wrapper for an instance of a HAHQAgent with the config from the config.py
    """
    def __init__(self):
        self.agent = HAHQAgent.HAHQAgent(
            config.SERVER_URL,
            config.AGENT_ID,
            config.AGENT_TOKEN,
            config.MQTT_BROKER_ADRESS,
            config.MQTT_BROKER_PORT,
            config.MQTT_TOPIC,
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
