import random

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy.smarty.grammar.attacks.Attack import Attack


class Attacks(object):
    """
    This class loads, initiates and populates pattern based attacks.

    :param: filePath: str -- The path to the JSON configuration, containing the attack patterns.
    """
    _elements = None

    _attackPatterns = []
    _attack = []

    def __init__(self, filePath):
        self._attackPatterns = (JSONConfigManager(filePath)).getConfig()

    def getAttack(self):
        """
        This method loads and initiate the components of an attack.

        :raises: ValueError -- Thrown, when no Elements instance is provided.
        :returns: `imps.smithy.smarty.attacks.Attack.Attack`
        """
        pattern = random.choice(self._attackPatterns)

        components = []

        for entry in pattern:
            if self._elements is None:
                raise ValueError(
                    "Elements are not initialized! Please provide an elements instance via setElements.")
            element = self._elements.getElementForUsage(entry)
            components.append(element)

        return Attack(components)

    def setElements(self, elements):
        self._elements = elements
