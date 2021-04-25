import heapq
from collections import Counter

import storm


class TopNFinderBolt(storm.BasicBolt):
    # Initialize this instance
    def initialize(self, conf, context):
        self._conf = conf
        self._context = context

        storm.logInfo("Counter bolt instance starting...")

        # TODO:
        # Task: set N
        self.heap = []
        
        # End

        # Hint: Add necessary instance variables and classes if needed

    def process(self, tup):
        '''
        TODO:
        Task: keep track of the top N words
        Hint: implement efficient algorithm so that it won't be shutdown before task finished
              the algorithm we used when we developed the auto-grader is maintaining a N size min-heap
        '''
        word0 = tup.values[0]
        count0 = tup.values[1] * -1  #in order to create maxheap
        heapq.heappush(self.heap, (count0, word0))
        
        if len(self.heap) > 10:
            self.heap.pop()
        
        
        for i in range(len(self.heap)):
            if i = 0:
                word = self.heap[i][1]
            else:
                word = self.heap[i][1] + ', ' + word

            storm.logInfo("Emitting %s" % word)
            storm.emit([word])
        
        # End


# Start the bolt when it's invoked
TopNFinderBolt().run()
