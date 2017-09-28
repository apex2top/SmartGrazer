import random
from math import floor

from imps.confy.JSONConfigManager import JSONConfigManager


class Attacks(object):
    _attackPatterns = []
    _attacks = []

    def __init__(self, filePath):
        self._attackPatterns = (JSONConfigManager(filePath)).getConfig()
        for pattern in self._attackPatterns:
            self._attacks.append(Attack(pattern))

    def getAttack(self):
        return random.choice(self._attacks)


class Attack(object):
    _life = 100
    _pattern = []
    _populated = []

    def __init__(self, pattern):
        self._pattern = pattern

    def __str__(self):
        return "".join(self.getPopulated())

    def getPopulated(self):
        return "attack goes here!"

    def getPattern(self):
        return self._pattern

    def getElements(self):
        return

    def getLife(self):
        return self._life

    def decreaseLife(self):
        self._life = floor(self._life / 2)

    def increaseLife(self):
        self._life = floor(self._life + (self._life * .5))
