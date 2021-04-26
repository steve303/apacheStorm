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
        #self.h = []
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
        count0 = int(tup.values[1])    #in order to create maxheap
        #storm.logInfo("*********************** %s " % count0)
        '''
        heapq.heappush(self.h, (count0, word0))
        
        if len(self.h) > 10:
            self.h.pop()

        f = open('/mp7/solution/MP7/test2.txt', 'a')
        for item in self.h:
            s = item[1] + ':' + str(item[0]) + '\n'
            f.write(s)
        f.write('\n')    
        f.close()
        for i in range(len(self.h)):
            if i == 0:
                topNstring = self.h[i][1]
            else:
                topNstring = self.h[i][1] + ', ' + topNstring 
        '''
        self.c[word0] = count0
        topN = self.c.most_common(10)

        for i in range(len(topN)):
            if i == 0:
                topNstring = topN[i][0]
            else:
                topNstring = topN[i][0] + ', ' + topNstring 

 
        word = 'top-N'
        count = topNstring
        storm.logInfo("Emitting %s %s" % (word, count))
        storm.emit([word, count])
        return
        # End


# Start the bolt when it's invoked
TopNFinderBolt().run()
