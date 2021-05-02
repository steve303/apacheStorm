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
        #storm.logInfo('******************************************************************')
        word0 = tup.values[0].strip()
        if word0 == '':
            return
        #storm.logInfo("*********************** %s " % word0)
        count0 = int(tup.values[1]) * -1   #in order to create maxheap
        #storm.logInfo("*********************** %s " % count0)
              
        if len(self.h) == 0:
            heapq.heappush(self.h, (count0, word0))
        else:
            max = -1e10
            index_max = None
            wordInList = False
            index_word = None
            for i in range(len(self.h)):
                if self.h[i][0] > max:
                    max = self.h[i][0]
                    index_max = i
                if word0 == self.h[i][1]:
                    wordInList = True
                    index_word = i
            if wordInList == True:        
                if count0 < self.h[index_word][0]:  #if new# is smaller del old value and then replace
                    del self.h[index_word]
                    heapq.heappush(self.h, (count0, word0))
            elif wordInList == False:
                if len(self.h) < 10:
                    heapq.heappush(self.h, (count0, word0))
                elif count0 < max:
                    del self.h[index_max]
                    heapq.heappush(self.h, (count0, word0))  #put new word and its count into the heap:
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
