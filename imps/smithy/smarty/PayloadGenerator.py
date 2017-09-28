from imps.smithy.simpy.grammar.Attacks import Attacks
from imps.smithy.simpy.grammar.Elements import Elements


class PayloadGenerator(object):
    config = None

    def applyConfig(self, configuration):
        self.config = configuration
        pass

    def generate(self, amount):
        elements = Elements(self.config["elements"])
        attackGenerator = Attacks(self.config["attacks"])
        attackGenerator.setElements(elements)

        print(attackGenerator.getAttack())

        return []