from random import choice

from jsonmerge import merge

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy.simpy.RandomStringGenerator import RandomStringGenerator
from imps.smithy.smarty.grammar.Outbreaks import Outbreaks
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
    _context = ''
    _outbreakConfig = ''

    def __init__(self, filePath):
        self._grammarPatterns = (JSONConfigManager(filePath)).getConfig()

    def setContext(self,context):
        self._context = context

    def getContext(self):
        return self._context

    def _getAttackGenerator(self):
        attackGenerator = Attacks(self._attackConfig)
        attackGenerator.setElements(self._elements)

        return attackGenerator

    def _getOutbreakGenerator(self):
        outbreakGenerator = Outbreaks(self._outbreakConfig)
        outbreakGenerator.setElements(self._elements)

        return outbreakGenerator

    def _getRandomByContext(self):
        patterns = []

        if self.getContext() == 'html':
            patterns = self._grammarPatterns['html']
        elif self.getContext() == 'javascript':
            patterns = self._grammarPatterns['javascript']
        else:
            patterns = merge(self._grammarPatterns['html'], self._grammarPatterns['javascript'])

        return choice(patterns)

    def _createPayload(self, outbreak, attack, text):
        pattern = self._getRandomByContext()

        # creating elements
        components = []
        for entry in pattern:
            element = self._elements.getElementForUsage(entry)
            components.append(element)

        # choose an attack pattern
        # populating the chosen grammar
        grammar = Grammar(components)

        # here jsfuck could be integrated
        grammar.populateOutbreak(outbreak)
        grammar.populateAttack(attack)
        grammar.populateRandomText(text)

        return grammar

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

    def setAttackConfig(self, attackConfig):
        self._attackConfig = attackConfig

    def setOutbreakConfig(self, outbreakConfig):
        self._outbreakConfig = outbreakConfig

    def setElements(self, elements):
        self._elements = elements

    def getElements(self):
        return self._elements

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
        outbreakGenerator = self._getOutbreakGenerator()

        # setting up the random string generator
        text = (RandomStringGenerator(RandomStringGenerator.minlength, RandomStringGenerator.maxlength)).get(
            RandomStringGenerator.MIXEDCASE)

        attack = attackGenerator.getAttack()
        outbreak = outbreakGenerator.getOutbreak()

        candidates = []
        for i in range(0, 3):
            candidates.append(self._createPayload(outbreak, attack, text))

        return self._getWithMostPotential(candidates)