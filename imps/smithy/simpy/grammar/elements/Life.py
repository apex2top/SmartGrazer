from math import floor
from random import randint


class Life(object):
    _life = 100

    def getLife(self):
        return randint(0, 100)

    def decreaseLife(self):
        self._life = floor(self._life / 2)

    def increaseLife(self):
        self._life = floor(self._life + (self._life * .5))

    def getLifeFromList(listOfValues):
        health = 0
        for entry in listOfValues:
            health += entry.getLife()

        return health

    def getEntryForLife(index, listOfValues):
        health = 0

        for entry in listOfValues:
            if index <= health:
                return entry

            health += entry.getLife()

        return None
