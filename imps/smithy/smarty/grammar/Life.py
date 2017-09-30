from math import floor


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

    def getKey(entry):
        return entry.getLife()

    def sortASC(listOfValues):
        return sorted(listOfValues, key=Life.getKey, reverse=True)
