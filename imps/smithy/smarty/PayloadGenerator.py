from imps.smithy.Generator import Generator
from imps.smithy.smarty.grammar.Grammars import Grammars


class PayloadGenerator(Generator):
    _config = None
    _grammar = None

    def applyConfig(self, configuration):
        self._config = configuration

    def getGrammar(self):
        if self._grammar is None:
            self._grammar = Grammars(self._config['grammars'])
        return self._grammar

    def generate(self, amount):
        grammarGenerator = self.getGrammar()
        grammarGenerator.setElements(self.getElements())

        grammarGenerator.setAttackConfig(self._config['attacks'])

        grammars = []
        for _ in range(0, amount):
            grammars.append(grammarGenerator.getPayload())

        return grammars
