#HAProxyHQ/Agent

This is the HAProxyHQ agent. It needs to be running on every machine running a HAProxy instance, which is supposed to be managed by HAProxyHQ, to apply the configurations rolled out by the server.

##Requirements

The only thing you'll need is the python package manager pip, the rest will be taken care of by the setup script. In case you don't already have pip installed, just install it with the package manager of your choice/OS.

For example Ubuntu:
>sudo apt-get install python-pip


##Setup

To install further requirements and get everything up and running, just run the setup.py script.

>sudo ./setup

Then you'll have to edit the config.py file. Here you'll find further instruction on how to configure the HAProxyHQ/Agent.

##Usage

The agent can be started by running

>./agent

Once the agent is running, it will be updated by the HAProxyHQ. In case you edit the config file manually, the agent will detect file changes and push them to the server. If this doesn't work for some reason, you can manually push the new config to the server by calling

>./agent --push

also it's possible to manually pull the current config

>./agent --pull