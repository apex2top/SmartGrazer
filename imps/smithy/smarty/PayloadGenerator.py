from imps.smithy.simpy.grammar.Attacks import Attacks


class PayloadGenerator(object):
    config = None

    def applyConfig(self, configuration):
        self.config = configuration
        print(self.config)
        pass

    def generate(self, amount):
        attackGenerator = Attacks(self.config["attacks"])
        print(attackGenerator.getAttack().getLife())

        return []