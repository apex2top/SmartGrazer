import importlib

from imps.confy.JSONConfigManager import JSONConfigManager


class PayloadMutator(object):
    _elements = []
    _config = {}
    _mutator = {}

    def __init__(self, filePath):
        self._config = (JSONConfigManager(filePath)).getConfig()

        for mutator in self._config:
            module = importlib.import_module("imps.mutty." + mutator + ".Mutator")
            mutateGenerator = module.Mutator()
            mutateGenerator.applyConfig(self._config[mutator])

            self._mutator[mutator] = mutateGenerator

    def mutate(self, element, additional=[]):
        for mutator in self._mutator:
            if element.getUsage() in self._mutator[mutator].getElements():
                element = self._mutator[mutator].mutate(element)

        return element
