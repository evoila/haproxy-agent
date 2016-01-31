#HAProxyHQ
HAProxyHQ is the headquarter for all your HAProxy instances. It allows you to configure and manage different HAProxy instances, while keeping track of they're health status. The project consists of three different repositories:
- [HAProxyHQ/Backend](https://github.com/haproxyhq/backend) - This is the backend, which takes care of managing HAProxy instances and rolling out configs. Implemented in Java Spring.
- [HAProxyHQ/Frontend](https://github.com/haproxyhq/frontend) - This is the frontend, which provides a simple user interface. Implemented in Angular 2.
- [HAProxyHQ/Agent](https://github.com/haproxyhq/agent) - This is the agent, which runs on every HAProxy instance and takes care of communication between the instance and the HAProxyHQ/Backend and applys settings, made by the user. Implementes in Python 2.7.

##HAProxyHQ/Agent/Introduction

This is the HAProxyHQ agent. It needs to be running on every machine running a HAProxy instance, which is supposed to be managed by HAProxyHQ, to apply the configurations rolled out by the server.

##HAProxyHQ/Agent/Requirements

The only thing you'll need is the python package manager pip, the rest will be taken care of by the setup script. In case you don't already have pip installed, just install it with the package manager of your choice/OS.

For example Ubuntu:
>sudo apt-get install python-pip


##HAProxyHQ/Agent/Setup
s
To install further requirements and get everything up and running, just run the setup.py script.

>sudo ./setup

Then you'll have to edit the config.py file. Here you'll find further instruction on how to configure the HAProxyHQ/Agent.


##HAProxyHQ/Agent/Usage

The agent needs privileges to edit the HAProxy config file, which usually is found in /etc/haproxy/, and reload the HAProxy service whenever a new config is rolled out. Therefore it's required to either run the agent as root, or as another user with these privileges. The agent can be started by running

>sudo ./agent

Once the agent is running, it will be updated by the HAProxyHQ. In case you edit the config file manually, the agent will detect file changes and push them to the server. If this doesn't work for some reason, you can manually push the new config to the server by calling

>./agent --push

also it's possible to manually pull the current config

>sudo ./agent --pull