# import os
# from os.path import join
from time import sleep

# from streamparse import Spout
import storm

FILENAME = "/tmp/data.txt"
class FileReaderSpout(storm.Spout):

    def initialize(self, conf, context):
        self._conf = conf
        self._context = context
        self._complete = False

        storm.logInfo("Spout instance starting...")

        # TODO:
        # Task: Initialize the file reader
        self.f = open(FILENAME) 
        # End

    def nextTuple(self):
        # TODO:
        # Task 1: read the next line and emit a tuple for it
        # Task 2: don't forget to sleep for 1 second when the file is entirely read to prevent a busy-loop
        #for sentence in self.f.readline():  
        sentence = self.f.readline()
        if len(sentence) == 0:
            sleep(1)
            return
        else:
          storm.logInfo("Emitting %s" % sentence)
          storm.emit([sentence])
        return 
        
# Start the spout when it's invoked
FileReaderSpout().run()
