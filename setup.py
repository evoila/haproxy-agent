# this script will install requirements you'll need to run the HAProxyHQ/Agent

import os

# install virtualenv
os.system('pip install virtualenv')

# create new virtualenv
os.system('virtualenv virtualenv')

# install requests
os.system('virtualenv/bin/pip install requests')