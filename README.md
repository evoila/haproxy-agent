#HAProxyHQ/Agent

This is the HAProxyHQ agent. It needs to be running on every machine running a HAProxy instance, which is supposed to be managed by HAProxyHQ, to apply the configurations rolled out by the server.

##Requirements

The only thing you'll need is the python package manager pip, the rest will be taken care of by the setup script. In case you don't already have pip installed, just install it with the package manager of your choice/OS.

For example Ubuntu:
>sudo apt-get install python-pip


##Setup

To install further requirements and get everything up and running, just run the setup.py script.

>sudo ./setup