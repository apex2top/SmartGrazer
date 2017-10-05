class Generator(object):
    _elements = None

    def generate(self, amount):
        return []

    def setElements(self, elements):
        self._elements = elements

    def getElements(self):
        return self._elements