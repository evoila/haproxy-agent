#HaProxy HQ
HaProxy HQ is a project based on the implementations of @buettner123 and @jdepoix. For the usage in the Cloud Foundry Service Broker enviornment we have forked the project and made some smaller changes to fit into our usage scenario.

The original implementation is located under:
- [HAProxyHQ/Backend](https://github.com/haproxyhq/backend) - This is the backend, which takes care of managing HAProxy instances and rolling out configs. Implemented in Java Spring.

- [HAProxyHQ/Agent](https://github.com/haproxyhq/agent) - This is the agent, which runs on every HAProxy instance and takes care of communication between the instance and the HAProxyHQ/Backend and applies settings, made by the user. Implemented in Python 2.7.

##Install
To install the agent on specific host you need to run the following steps:

>python setup.py install

## Configure

When you have successfully pulled the dependencies from your endpoint the next step is to configure your configuration file etc/haproxyhq/agent.conf. The default contents looks as follows:

````ini
[agent]
id
token

[haproxy]
config_file = /etc/haproxy/haproxy.conf

[rabbitmq]
host = localhost
port = 1883
virtualhost = /
username
password
exchange

[server]
address = localhost
port = 8080
api_endpoint = agents
````

## Run

When you have completed to fill all relevant values, you can start the agent via

>haproxy-agent [--config-file=<agent.conf path>] [--push | --pull]
