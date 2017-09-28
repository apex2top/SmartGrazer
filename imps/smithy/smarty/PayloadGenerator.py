from imps.smithy.smarty.grammar.Attacks import Attacks

from imps.smithy.smarty.grammar.Elements import Elements


class PayloadGenerator(object):
    config = None

    def applyConfig(self, configuration):
        self.config = configuration
        pass

    def generate(self, amount):
        elements = Elements(self.config["elements"])
        attackGenerator = Attacks(self.config["attacks"])
        attackGenerator.setElements(elements)

        attacks = []
        for _ in range(0, amount):
            attacks.append(str(attackGenerator.getAttack()))

        return attacks
