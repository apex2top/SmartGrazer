class MutatorGeneral(object):
    """ This is the base class for Mutators.

        All implemented mutators should implement the `mutate(element)` function.
    """
    _config = {}

    def applyConfig(self, config):
        self._config = config

    def mutate(self, element):
        return element

    def getElements(self):
        return self._config['elements']

    def _isEnabled(self):
        """
            This method can be used in the mutate-method to control whether the mutator should be used or not.

            This option can be configured in the config/smarty/elements.mutator.json file.

            :returns bool -- Enabled or not
        """
        return self._config['enabled']
