from random import choice

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
        pattern = choice(self._grammarPatterns)

        # creating elements
        components = []
        for entry in pattern:
            if self._elements is None:
                raise ValueError(
                    "Elements are not initialized! Please provide an elements instance via setElements.")
            element = self._elements.getElementForUsage(entry)
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

    '''def getWithMostPotential(self, grammarPatterns):
        # Count partCount, patternLifes and currentMaxLife of all patterns

        partCount = 0
        maxLife = 0
        patternLifes = {}

        for key, pattern in enumerate(grammarPatterns):
            patternLifes[key] = 0

            for part in pattern:
                elements = self.getElementsForUsage(part)

                minHealth = len(elements)
                maxHealth = self.getDefaultLife() * minHealth

                elementsLife = Life.getLifeFromList(elements) / minHealth

                health = math.floor((elementsLife - minHealth) / (maxHealth - minHealth))
                partCount = partCount + 1
                patternLifes[key] = patternLifes[key] + health

            maxLife = maxLife + patternLifes[key]

        current = None
        lastPotential = 0

        for key, life in enumerate(patternLifes):
            pCount = len(grammarPatterns[key])
            potential = int(life * pCount / maxLife * partCount)

            if lastPotential < potential:
                lastPotential = potential
                current = grammarPatterns[key]

        return current'''