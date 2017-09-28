from random import randint

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy.smarty.grammar.RandomPicker import RandomPicker
from imps.smithy.smarty.grammar.attacks.Attack import Attack


class Attacks(object):
    _elements = None

    _attackPatterns = []
    _attacks = []

    def __init__(self, filePath):
        self._attackPatterns = (JSONConfigManager(filePath)).getConfig()

    def getAttack(self):
        if not self._attacks:
            self._loadAttacks()

        return RandomPicker.pickWeightedRandom(self._attacks)

    def setElements(self, elements):
        self._elements = elements

    def _loadAttacks(self):
        for pattern in self._attackPatterns:
            components = []

            for entry in pattern:
                if self._elements is None:
                    raise ValueError(
                        "Elements are not initialized! Please provide an elements instance via setElements.")
                element = self._elements.getElement(entry)

                '''
                print("Before %s" % element.getLife())

                for i in range(0, randint(0, 3)):
                    element.decreaseLife()

                print("After %s" % element.getLife())
                print("_______________________________")
                '''
                components.append(element)

            attack = Attack(components)

            self._attacks.append(attack)
