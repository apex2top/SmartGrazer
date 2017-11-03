from math import floor


class Life(object):
    """ This class represents the base of element instances,
    handling all life related management.
    """

    _life = None

    def setLife(self, amount):
        self._life = amount

    def getLife(self):
        return self._life

    def decreaseLife(self):
        """
            This method reduces the life for 25% of its initial value.

            The life of an instance cannot be lower one.

            :return: life -- the elements life
        """
        self._life = floor(self._life * 0.75)

        if self._life < 1:
            self._life = 1

    def getLifeFromList(listOfValues):
        health = 0
        for entry in listOfValues:
            health = health + entry.getLife()

        return health

    def getKey(entry):
        return entry.getLife()

    def sortDesc(listOfValues):
        return sorted(listOfValues, key=Life.getKey, reverse=true)
