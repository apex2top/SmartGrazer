from random import choice

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy.simpy.RandomStringGenerator import RandomStringGenerator
from imps.smithy.smarty.grammar.Attacks import Attacks
from imps.smithy.smarty.grammar.grammars.Grammar import Grammar


class Grammars(object):
    """
    This class loads, initiates and populates pattern based payloads.

    :param: filePath: str -- The path to the JSON configuration, containing the grammar patterns.
    """

    _elements = None
    _grammarPatterns = []
    _attackConfig = ''

    def __init__(self, filePath):
        self._grammarPatterns = (JSONConfigManager(filePath)).getConfig()

    def getPayload(self):
        """
            Creates three random payloads and chooses the payload with the most potential.

            :raises: ValueError -- Thrown, when no Elements instance is provided.
            :returns: `imps.smithy.smarty.grammars.Grammar.Grammar`
        """
        if self._elements is None:
            raise ValueError(
                "Elements are not initialized! Please provide an elements instance via setElements.")

        attackGenerator = self._getAttackGenerator()

        # setting up the random string generator
        text = (RandomStringGenerator(RandomStringGenerator.minlength, RandomStringGenerator.maxlength)).get(
            RandomStringGenerator.MIXEDCASE)

        attack = attackGenerator.getAttack()

        candidates = []
        for i in range(0, 3):
            candidates.append(self._createPayload(attack, text))

        return self._getWithMostPotential(candidates)


    def setElements(self, elements):
        self._elements = elements

    def getElements(self):
        return self._elements

    def _getAttackGenerator(self):
        attackGenerator = Attacks(self._attackConfig)
        attackGenerator.setElements(self._elements)

        return attackGenerator

    def _createPayload(self, attack, text):
        pattern = choice(self._grammarPatterns)

        # creating elements
        components = []
        for entry in pattern:
            element = self._elements.getElementForUsage(entry)
            components.append(element)

        # choose an attack pattern
        # populating the chosen grammar
        grammar = Grammar(components)

        # here jsfuck could be integrated
        grammar.populateAttack(attack)
        grammar.populateRandomText(text)

        return grammar

    def setAttackConfig(self, attackConfig):
        self._attackConfig = attackConfig

    def _getWithMostPotential(self, candidates):
        """
        This method calculates the grammar with most potential.

        :param candidates: list<`imps.smithy.smarty.grammars.Grammar.Grammar`> -- The candidates to choose from.
        :return: `imps.smithy.smarty.grammars.Grammar.Grammar`
        """
        totalLife = 0

        for candidate in candidates:
            totalLife = totalLife + candidate.getLife()

        current = None
        lastPotential = 0

        for candidate in candidates:
            life = candidate.getLife()
            potential = life / totalLife

            if lastPotential < potential:
                current = candidate
                lastPotential = potential

        return current
