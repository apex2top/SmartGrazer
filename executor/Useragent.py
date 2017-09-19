from random import randint

class Useragent(object):
    useragents = None

    def __init__(self):
        pass

    def getAvailableUseragents(self):
        return self.useragents

    def getRandom(self):
        index = randint(0, len(self.useragents) - 1)
        return self.useragents[index]
