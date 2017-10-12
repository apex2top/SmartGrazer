import importlib

from imps.smithy.Elements import Elements


class PayloadGenerator(object):
    _impName = ''
    _config = {}
    _impConfig = {}
    _amount = 1

    _instances = {}

    def __init__(self, configuration):
        self._config = configuration
        self._impName = self._config["smithy"]["generator"]

    def getImpString(self, name):
        self._amount = self._config["smithy"]["generate"]["amount"]
        self._impConfig = self._config[name]

        return "imps.smithy.{0}".format(name)

    def _getGenerator(self, name):
        if not name in self._instances.keys():
            module = importlib.import_module(self.getImpString(name) + ".PayloadGenerator")
            generator = module.PayloadGenerator()
            generator.applyConfig(self._impConfig)

            elements = Elements(self._config["smithy"]["elements"])
            default = int(self._config["smithy"]["life"]["default"])
            elements.setDefaultLife(default)

            generator.setElements(elements)
            self._instances[name] = generator

        return self._instances[name]

    def adjustElements(self, elements):
        self._getGenerator(self._impName).adjustElements(elements)

    def getSimpy(self):
        return self._getGenerator("simpy")

    def generate(self):
        return self._getGenerator(self._impName).generate(self._amount)
