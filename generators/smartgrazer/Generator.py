from random import randint

from generators.simple.tools.RandomStrings import RandomStrings
from generators.smartgrazer.Settings import Settings
from generators.smartgrazer.generator.grammar.Elements import Elements


class Generator(object):
    elements = {}
    randomStringGen = None
    grammars = []

    def __init__(self):
        self.elements = Elements()
        self.loadFromConfig()
        self.randomStringGen = RandomStrings(lcc=True, ucc=False, scc=False, length=1)

    def loadFromConfig(self):
        settings = Settings()
        self.grammars = settings.getSettings()['grammars']

    def getAvailableGrammars(self):
        return self.grammars

    def pupulateGrammar(self, grammar):
        elcntr = 0
        tag = None
        quotes = {"QUOTE_INNER": None, "QUOTE_OUTER": None}
        gr = {}

        for element_name in grammar:
            element = self.elements.getElement(element_name)

            elcntr += 1
            gr[element.getName() + str(elcntr)] = element.getElement()
            '''
            print(" - ".join([element.getName(),element.getElement()]))
            if element.getName() == "TEXT":
                el = self.randomStringGen.getRandomString()
                gr[element.getName()] = el
            elif element.getName() in self.elements:
                el = self.elements[element]

                if isinstance(el, list):
                    index = randint(0, len(el) - 1)
                    el = el[index]

                    if element == "TAG_HTML":
                        if tag is None:
                            tag = el
                        else:
                            el = tag

                    if element == "QUOTE_INNER" or element == "QUOTE_OUTER":
                        if quotes[element] is None:
                            quotes[element] = el
                        else:
                            el = quotes[element]

                if element in gr.keys():
                    elcntr += 1
                    gr[element + str(elcntr)] = el
                else:
                    gr[element] = el
            else:
                elcntr += 1
                gr[element + str(elcntr)] = element
            '''

        return gr

    def create(self, index=None):
        if index is None:
            index = randint(0, len(self.grammars) - 1)

        gr = self.grammars[index]
        populated = self.pupulateGrammar(gr)

        string = ''.join('{0}'.format(value) for (value) in populated.values())

        gen = {
            "tools": ''.join('{0} '.format(value) for (value) in gr),
            "populated": populated,
            "string": string
        }

        return string.encode()

    def generate(self, amount=5):
        attacks = []

        for i in range(0, amount):
            attacks.append(self.create())

        return {'generator': self.__class__.__name__, 'payloads': attacks}
