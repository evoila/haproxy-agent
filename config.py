# the url and port of the server the HAProxyHQ is running on and the API endpoint for the config
SERVER_ADDRESS = ''
SERVER_PORT = '80'
SERVER_API_ENDPOINT = 'config'

# the ID of this agent and it's token, which the HAProxyHQ will need to identify and authenticate this agent
AGENT_ID = ''
AGENT_TOKEN = ''

# the adress and port of the MQTT broker
MQTT_BROKER_ADRESS = ''
MQTT_BROKER_PORT = '1883'

# the path of the HAProxy config, which the agent will manage
HA_PROXY_CONFIG_PATH = ''


# complete URL. There should be no need to change this!
SERVER_URL = SERVER_ADDRESS + ':' + SERVER_PORT + '/' + SERVER_API_ENDPOINT + '/' + AGENT_ID + '/'