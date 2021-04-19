import storm
# Counter is a nice way to count things,
# but it is a Python 2.7 thing
from collections import Counter


class CountBolt(storm.BasicBolt):
    # Initialize this instance
    def initialize(self, conf, context):
        self._conf = conf
        self._context = context

        storm.logInfo("Counter bolt instance starting...")

        # Hint: Add necessary instance variables and classes if needed
        self.c = Counter

    def process(self, tup):
        # TODO
        # Task: word count
        # Hint: using instance variable to tracking the word count
        if tup[0] not in self.c:
            self.c[tup[0]] = 1
        else:
            self.c[tup[0]] += 1
        storm.logInfo("Emmiting %s %d" % (tup[0], self.c[tup[0]]))
        storm.emit([self.c[tup[0]])
        pass
        # End


# Start the bolt when it's invoked
CountBolt().run()
