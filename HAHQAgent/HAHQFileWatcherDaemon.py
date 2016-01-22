from threading import Thread

from whenchanged.whenchanged import WhenChanged

class HAHQFileWatcherDaemon(Thread):
    """
    this class starts a deamon thread, looking for file changes of the config file. For every file change, it pushes
    the new config to the HAProxyHQ backend.
    """
    def __init__(self, config_file_path):
        wc = WhenChanged([config_file_path], './../agent --push')
        Thread.__init__(self, target=wc)
        self.setDaemon(True)
        self.start()