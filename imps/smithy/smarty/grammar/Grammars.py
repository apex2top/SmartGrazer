from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy.simpy.RandomStringGenerator import RandomStringGenerator
from imps.smithy.smarty.grammar.Life import Life
from imps.smithy.smarty.grammar.RandomPicker import RandomPicker
from imps.smithy.smarty.grammar.grammars.Grammar import Grammar
from imps.smithy.smarty.grammar.Attacks import Attacks


class Grammars(object):
    _elements = None

    _grammarPatterns = []
    _payloads = []

    _attackConfig = ''

    def __init__(self, filePath):
        self._grammarPatterns = (JSONConfigManager(filePath)).getConfig()

    def getPayload(self):
        if not self._payloads:
            self._loadPayloads()

        return Life.sortASC(self._payloads)[0]

    def setElements(self, elements):
        self._elements = elements

    def _getAttackGenerator(self):
        attackGenerator = Attacks(self._attackConfig)
        attackGenerator.setElements(self._elements)

        return attackGenerator

    def _loadPayloads(self):
        for pattern in self._grammarPatterns:
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

            attackGenerator = self._getAttackGenerator()
            attack = attackGenerator.getAttack()

            text = (RandomStringGenerator(RandomStringGenerator.minlength, RandomStringGenerator.maxlength)).get(RandomStringGenerator.MIXEDCASE)

            grammar = Grammar(components)

            grammar.populateAttack(attack)
            grammar.populateRandomText(text)

            #print(str(grammar) + " with a life of: %s!" %  grammar.getLife())

            self._payloads.append(grammar)

    def setAttackConfig(self, attackConfig):
        self._attackConfig = attackConfig