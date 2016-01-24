from threading import Thread
import time

from HAHQAgent.HAHQConfiguredAgentInstance import HAHQConfiguredAgentInstance


class HAHQHeartbeatDaemon(Thread):
    def __init__(self, config_file_path):
        Thread.__init__(self)
        self.setDaemon(True)
        self.agent = HAHQConfiguredAgentInstance()

    def run(self):
        while(True):
            self.agent.post_config()
            time.sleep(1000)
