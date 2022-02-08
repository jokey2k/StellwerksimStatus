import threading
import os
import sys
import cx_Logging
pjoin = os.path.join
import stellwerksimstatus


class Handler:
    def __init__(self):
        self.stopEvent = threading.Event()
        self.stopRequestedEvent = threading.Event()

    def initialize(self, configFileName):
        self.directory = os.path.dirname(sys.executable)
        cx_Logging.StartLogging(pjoin(self.directory, "teste.log"), cx_Logging.DEBUG)

    def run(self):
        cx_Logging.Debug("stdout=%r", sys.stdout)
        thread = threading.Thread(target=stellwerksimstatus.main, args=[self.stopRequestedEvent])
        sys.stdout = open(pjoin(self.directory, "stdout.log"), "a")
        sys.stderr = open(pjoin(self.directory, "stderr.log"), "a")
        thread.start()
        self.stopRequestedEvent.wait()
        self.stopEvent.set()

    def stop(self):
        self.stopRequestedEvent.set()
        self.stopEvent.wait()