import importlib

from imps.smithy.Elements import Elements


class PayloadGenerator(object):
    _impName = ''
    _config = {}
    _impConfig = {}
    _amount = 1

    def __init__(self, configuration):
        self._config = configuration
        self._impName = self._config["smithy"]["generator"]

    def getImpString(self, name):
        self._amount = self._config["smithy"]["generate"]["amount"]
        self._impConfig = self._config[name]

        return "imps.smithy.{0}".format(name)

    def _getGenerator(self, name):
        module = importlib.import_module(self.getImpString(name) + ".PayloadGenerator")
        generator = module.PayloadGenerator()
        generator.applyConfig(self._impConfig)

        elements = Elements(self._config["smithy"]["elements"])
        default = int(self._config["smithy"]["life"]["default"])
        elements.setDefaultLife(default)

        generator.setElements(elements)

        return generator

    def getSimpy(self):
        return self._getGenerator("simpy")

    def generate(self):
        return self._getGenerator(self._impName).generate(self._amount)
