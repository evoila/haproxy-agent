#HaProxy HQ
HaProxy HQ is a project based on the implementations of @buettner123 and @jdepoix. For the usage in the Cloud Foundry Service Broker enviornment we have forked the project and made some smaller changes to fit into our usage scenario.

The original implementation is located under:
- [HAProxyHQ/Backend](https://github.com/haproxyhq/backend) - This is the backend, which takes care of managing HAProxy instances and rolling out configs. Implemented in Java Spring.

- [HAProxyHQ/Agent](https://github.com/haproxyhq/agent) - This is the agent, which runs on every HAProxy instance and takes care of communication between the instance and the HAProxyHQ/Backend and applies settings, made by the user. Implemented in Python 2.7.

##Install
To install the agent on specific host you need to run the following steps:

>sudo apt-get install python-pip -y

>git clone https://github.com/evoila/haproxy-agent

>sudo ./setup

## Configure

When you have successfully pulled the dependencies from your endpoint the next step is to configure your config.py file. The default contents looks as follows:

````python
# the url and port of the server the HAProxyHQ is running on and the API endpoint for the config
SERVER_ADDRESS = 'http://my.haproxyhq.backend'
SERVER_PORT = '8080'
SERVER_API_ENDPOINT = 'agents'

# the ID of this agent and it's token, which the HAProxyHQ will need to identify and authenticate this agent
AGENT_ID = ''
AGENT_TOKEN = ''

# the adress and port of the MQTT broker
MQTT_BROKER_ADRESS = 'my.mqtt.broker'
MQTT_BROKER_PORT = '1883'

# the path of the HAProxy config, which the agent will manage
HA_PROXY_CONFIG_PATH = '/etc/haproxy/haproxy.cfg'

# the MQTT topic the agent will subscribe to. There should be no need to change this!
MQTT_TOPIC = '/haproxyhq/agents/' + AGENT_ID

# complete URL. There should be no need to change this!
SERVER_URL = SERVER_ADDRESS + ':' + SERVER_PORT + '/' + SERVER_API_ENDPOINT + '/' + AGENT_ID + '/'
````

## Run

When you have completed to fill all relevant values, you can start the agent via

>sudo ./agent
