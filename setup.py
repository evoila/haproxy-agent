#!/usr/bin/env python

from setuptools import setup

setup(
    name='HaProxy HQ - Agent',
    version='0.9.0',
    description='Agent for HaProxy HQ',
    author='evoila GmbH',
    author_email='info@evoila.de',
    url='evoila.de',
    license='Apache-2.0',
    setup_requires=['setuptools>=17.1'],
    install_requires=['pika<=0.11.2', 'requests'],
    packages=['haproxy_hq_agent'],
    entry_points={
        'console_scripts': ['haproxy-agent = '
                            'haproxy_hq_agent.agent:main']
        },
)
