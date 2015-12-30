# the url and port of the server the HAProxyHQ is running on and the API endpoint for the config
SERVER_ADDRESS = 'http://192.168.100.101'
SERVER_PORT = '5000'
SERVER_API_ENDPOINT = 'config'

# the ID of this agent and it's token, which the HAProxyHQ will need to identify and autheticate this agent
AGENT_ID = '123'
AGENT_TOKEN = ''

# the path of the HAProxy config, which the agent will manage
HA_PROXY_CONFIG_PATH = 'test.cfg'


# complete URL. There should be no need to change this!
SERVER_URL = SERVER_ADDRESS + ':' + SERVER_PORT + '/' + SERVER_API_ENDPOINT + '/' + AGENT_ID + '/'