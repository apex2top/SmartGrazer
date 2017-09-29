from random import randint

from imps.smithy.smarty.grammar.Attacks import Attacks
from imps.smithy.smarty.grammar.Grammars import Grammars

from imps.smithy.smarty.grammar.Elements import Elements


class PayloadGenerator(object):
    config = None

    def applyConfig(self, configuration):
        self.config = configuration
        pass

    def generate(self, amount):
        elements = Elements(self.config["elements"])

        default = int(self.config["life"]["default"])
        elements.setDefaultLife(default)

        grammarGenerator = Grammars(self.config['grammars'])
        grammarGenerator.setElements(elements)
        grammarGenerator.setAttackConfig(self.config['attacks'])

        grammars = []
        for _ in range(0, amount):
            grammars.append(str(grammarGenerator.getPayload()))

        return grammars
