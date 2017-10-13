class Generator(object):
    _elements = None

    def generate(self, amount):
        return []

    def setElements(self, elements):
        self._elements = elements

    def getElements(self):
        return self._elements

    def adjustElements(self, elements):
        for key in elements.keys():
            if key in self.getElements().getLoadedElements().keys():
                self.getElements().replaceElement(elements[key])
