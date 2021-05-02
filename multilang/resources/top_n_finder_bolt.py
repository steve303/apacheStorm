import heapq
from collections import Counter
import storm


class TopNFinderBolt(storm.BasicBolt):
    # Initialize this instance
    def initialize(self, conf, context):
        self._conf = conf
        self._context = context
        storm.logInfo("topN bolt instance starting...")

        # TODO:
        # Task: set N
        self.h = []
        self.c = Counter() 
        # End
        # Hint: Add necessary instance variables and classes if needed

    def process(self, tup):
        '''
        TODO:
        Task: keep track of the top N words
        Hint: implement efficient algorithm so that it won't be shutdown before task finished
              the algorithm we used when we developed the auto-grader is maintaining a N size min-heap
        '''
        word0 = tup.values[0].strip()
        if word0 == '':
            return
        count0 = int(tup.values[1])    
        index = -1    
                  
        for i in range(len(self.h)):
            if word0 == self.h[i][1]:
                index = i
     
        if index > -1:  #case when word in in the heap at index i
            if count0 > self.h[index][0]:
                self.h.pop(index)
                heapq.heappush(self.h, (count0, word0))
        else:  #case when word is not in the heap
            if len(self.h) < 10:
                heapq.heappush(self.h, (count0, word0))
            elif count0 > self.h[0][0]:
                heapq.heappushpop(self.h, (count0, word0))

        #print top 10
        for i in range(len(self.h)):
            if i == 0:
                topNstring = self.h[i][1]
            else:
                topNstring = self.h[i][1] + ', ' + topNstring 
        word = 'top-N'
        count = topNstring
        storm.logInfo("Emitting %s %s" % (word, count))
        storm.emit([word, count])
        return
        # End
# Start the bolt when it's invoked
TopNFinderBolt().run()
