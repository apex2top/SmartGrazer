import random

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy.simpy.grammar.elements.Life import Life


class Attacks(object):
    _elements = None

    _attackPatterns = []
    _attacks = []

    def __init__(self, filePath):
        self._attackPatterns = (JSONConfigManager(filePath)).getConfig()

    def getAttack(self):
        if not self._attacks:
            self._loadAttacks()

        return random.choice(self._attacks)

    def setElements(self, elements):
        self._elements = elements

    def _loadAttacks(self):
        for pattern in self._attackPatterns:
            attack = []

            for entry in pattern:
                if self._elements is None:
                    raise ValueError(
                        "Elements are not initialized! Please provide an elements instance via setElements.")
                element = self._elements.getElement(entry)
                attack.append(element)

            self._attacks.append(Attack(attack))


class Attack(Life):
    _life = 100
    _elements = []
    _populated = []

    def __init__(self, elements):
        self._elements = elements

    def __str__(self):
        return "".join(self.getPopulated())

    def getPopulated(self):
        populated = []
        for element in self._elements:
            populated.append(str(element))

        return populated

    def getElements(self):
        return self._elements
