from imps.smithy.GeneratorGeneral import GeneratorGeneral
from imps.smithy.smarty.grammar.Grammars import Grammars


class PayloadGenerator(GeneratorGeneral):
    """
    This class generates the the requestet payloads.

    The payloads are represented through patterns, holding element identifier.
    """
    _config = None
    _grammar = None

    def applyConfig(self, configuration):
        self._config = configuration

    def getGrammar(self):
        if self._grammar is None:
            self._grammar = Grammars(self._config['grammars'])
        return self._grammar

    def generate(self):
        grammarGenerator = self.getGrammar()
        grammarGenerator.setElements(self.getElements().clearMutations())
        grammarGenerator.getElements().clearElementMemory()

        grammarGenerator.setAttackConfig(self._config['attacks'])
        grammarGenerator.setOutbreakConfig(self._config['outbreaks'])

        grammars = []
        for _ in range(0, 3):
            grammars.append(grammarGenerator.getPayload())

        return grammars
