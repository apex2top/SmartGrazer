from random import choice

from imps.confy.JSONConfigManager import JSONConfigManager
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
        pattern = choice(self._grammarPatterns)

        # creating elements
        components = []
        for entry in pattern:
            if self._elements is None:
                raise ValueError(
                    "Elements are not initialized! Please provide an elements instance via setElements.")
            element = self._elements.getElement(entry)
            components.append(element)

        # choose an attack and populating it
        attackGenerator = self._getAttackGenerator()
        attack = attackGenerator.getAttack()

        # setting up the random string generator
        text = (RandomStringGenerator(RandomStringGenerator.minlength, RandomStringGenerator.maxlength)).get(
            RandomStringGenerator.MIXEDCASE)

        # populating the chosen grammar
        grammar = Grammar(components)

        grammar.populateAttack(attack)
        grammar.populateRandomText(text)

        self._payload = grammar

    def setAttackConfig(self, attackConfig):
        self._attackConfig = attackConfig
