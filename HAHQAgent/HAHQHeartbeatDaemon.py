import time
from threading import Thread

import HAHQConfiguredAgentInstance


class HAHQHeartbeatDaemon(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.agent = HAHQConfiguredAgentInstance.HAHQConfiguredAgentInstance()

    def run(self):
        while (True):
            self.agent.post_config()
            time.sleep(60)
