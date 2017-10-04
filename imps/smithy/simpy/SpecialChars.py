from generators.smartgrazer.Settings import Settings
from generators.smartgrazer.generator.grammar.Element import Element


class SpecialChars(object):
    special_chars = None

    def __init__(self):
        settings = Settings()
        self.special_chars = settings.getSettings()['specialchars']

        tmp = []

        #for elem in self.special_chars:
        #    elem = Element(elem, elem)
        #    tmp.append(elem.getElement())

        self.special_chars = tmp

    def getSpecialChars(self):
        return ''.join(self.special_chars)
