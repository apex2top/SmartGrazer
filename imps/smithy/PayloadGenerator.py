import importlib


class PayloadGenerator(object):
    impName = ''
    config = {}
    impConfig = {}
    amount = 1

    def __init__(self, configuration):
        self.config = configuration
        self.impName = self.config["smithy"]["generator"]

    def getImpString(self, name):
        self.amount = self.config["smithy"]["generate"]["amount"]
        self.impConfig = self.config[name]

        return "imps.smithy.{0}".format(name)

    def _getGenerator(self, name):
        module = importlib.import_module(self.getImpString(name) + ".PayloadGenerator")
        generator = module.PayloadGenerator()
        generator.applyConfig(self.impConfig)

        return generator

    def getSimpy(self):
        return self._getGenerator("simpy")

    def generate(self):
        return self._getGenerator(self.impName).generate(self.amount)
