class Mutator(object):
    _config = {}

    def applyConfig(self, config):
        self._config = config

    def mutate(self, element, additional=[]):
        return element

    def getElements(self):
        return self._config['elements']

    def _isEnabled(self):
        return self._config['enabled']
