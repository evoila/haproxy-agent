# the url and port of the server the HAProxyHQ is running on and the API
# endpoint for the config
SERVER_ADDRESS = 'http://my.haproxyhq.backend'
SERVER_PORT = '8080'
SERVER_API_ENDPOINT = 'agents'

# the ID of this agent and it's token, which the HAProxyHQ will need to identify
# and authenticate this agent
AGENT_ID = ''
AGENT_TOKEN = ''

# the adress and port of the RabbitMQ server
RABBIT_MQ_HOST = 'my.rabbitmq.server'
RABBIT_MQ_PORT = '1883'
RABBIT_MQ_VIRTUAL_HOST = ''
RABBIT_MQ_USERNAME = ''
RABBIT_MQ_PASSWORD = ''

# the path of the HAProxy config, which the agent will manage
HA_PROXY_CONFIG_PATH = '/etc/haproxy/haproxy.cfg'

# the RabbitMQ exchange the agent will subscribe to. There should be no need to
# change this!
RABBIT_MQ_EXCHANGE = '/haproxyhq/agents/' + AGENT_ID

# complete URL. There should be no need to change this!
SERVER_URL = SERVER_ADDRESS + ':' + SERVER_PORT + '/' + SERVER_API_ENDPOINT \
             + '/' + AGENT_ID + '/'
