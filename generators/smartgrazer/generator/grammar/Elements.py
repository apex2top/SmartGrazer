from random import randint

from generators.smartgrazer.Settings import Settings
from generators.smartgrazer.generator.grammar.Element import Element


class Elements(object):
    elements = []

    def __init__(self):
        settings = Settings()
        self.elements = settings.getSettings()['elements']

    def getAvailableElements(self):
        return self.elements

    def getElement(self, name):
        if name in self.elements.keys():
            element = self.elements[name]
            if len(element) == 1:
                return Element(name, element[0])
            else:
                index = randint(0, len(element) - 1)
                return Element(name, element[index])
        else:
            return Element(name, name)
