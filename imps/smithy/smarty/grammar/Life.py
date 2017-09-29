from math import floor
from random import randint


def getKey(entry):
    return entry.getLife()

class Life(object):
    _life = 1

    def setLife(self, amount):
        self._life = amount

    def getLife(self):
        return self._life

    def decreaseLife(self):
        self._life = floor(self._life * 0.75)

        if self._life < 1:
            self._life = 1

    def increaseLife(self):
        self._life = floor(self._life + (self._life * .5))

        if self._life > 100:
            self._life = 100

    def getLifeFromList(listOfValues):
        health = 0
        for entry in listOfValues:
            health = health + entry.getLife()

        return health

    def getEntryForLife(index, listOfValues):
        health = 0

        for entry in listOfValues:
            if index <= health:
                return entry

            health += entry.getLife()

        return entry

    def sortASC(payloads):
        return sorted(payloads, key=getKey, reverse=True)
