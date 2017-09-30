import random

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy.smarty.grammar.attacks.Attack import Attack


class Attacks(object):
    _elements = None

    _attackPatterns = []
    _attack = []

    def __init__(self, filePath):
        self._attackPatterns = (JSONConfigManager(filePath)).getConfig()

    def getAttack(self):
        if not self._attack:
            self._loadAttack()

        return self._attack

    def setElements(self, elements):
        self._elements = elements

    def _loadAttack(self):
        pattern = random.choice(self._attackPatterns)

        components = []

        for entry in pattern:
            if self._elements is None:
                raise ValueError(
                    "Elements are not initialized! Please provide an elements instance via setElements.")
            element = self._elements.getElement(entry)
            components.append(element)

        self._attack = Attack(components)
