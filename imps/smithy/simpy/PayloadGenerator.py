from imps.smithy.elements.Element import Element
from imps.smithy.simpy.RandomStringGenerator import RandomStringGenerator
from imps.smithy.Generator import Generator
from imps.smithy.smarty.grammar.attacks.Attack import Attack


class PayloadGenerator(Generator):
    config = None

    def applyConfig(self, configuration):
        self.config = configuration

    def generate(self):
        payloads = []

        if self.config["checks"]['max_get_length']:
            payloads.append(self._getLongRandomString())

        if self.config["checks"]['specialchars']:
            payloads.append(self._getSpecialCharsString())

        if self.config["checks"]['chars']:
            payloads.append(self._getRandomString(RandomStringGenerator.MIXEDCASE))

        return payloads

    def _getRandomString(self, type):
        stringconf = self.config['stringgenerator']['length']
        rs = RandomStringGenerator(stringconf['min'], stringconf['max'])
        element = Element('RANDOMSTRING')
        element.setValue(rs.get(type))
        return Attack([element])

    def _getLongRandomString(self, type=RandomStringGenerator.MIXEDCASE):
        rs = RandomStringGenerator(1000, 16000)
        element = Element('RANDOMLONGSTRING', rs.get(type))

        return Attack([element])

    def _getSpecialCharsString(self):
        elements = []
        for key in self.config['stringgenerator']['specialchars']:
            elements.append(self.getElements().getElementForUsage(key))

        return Attack(elements)
