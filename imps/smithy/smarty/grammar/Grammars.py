from random import choice, randint

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy import Elements
from imps.smithy.simpy.RandomStringGenerator import RandomStringGenerator
from imps.smithy.smarty.grammar.Attacks import Attacks
from imps.smithy.smarty.grammar.grammars.Grammar import Grammar


class Grammars(object):
    _elements = None

    _grammarPatterns = []
    _payload = None

    _attackConfig = ''

    def __init__(self, filePath):
        self._grammarPatterns = (JSONConfigManager(filePath)).getConfig()

    def getPayload(self):
        self._loadPayload()
        return self._payload

    def setElements(self, elements):
        self._elements = elements

    def getElements(self):
        return self._elements

    def _getAttackGenerator(self):
        attackGenerator = Attacks(self._attackConfig)
        attackGenerator.setElements(self._elements)

        return attackGenerator

    def _loadPayload(self):
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

        self._payload = self._getWithMostPotential(candidates)

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

        totalLife = 0

        for candidate in candidates:
            totalLife = totalLife + candidate.getLife()

        current = None
        lastPotential = 0

        for candidate in candidates:
            life = candidate.getLife()
            potential = life/totalLife

            if lastPotential < potential:
                current = candidate
                lastPotential = potential

        return current
