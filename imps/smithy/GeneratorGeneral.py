class GeneratorGeneral(object):
    """ This class represents the base attributes of a Generator.

        Every class extending this class, has to implement its own `generate` method.

    """
    _elements = None

    def generate(self, amount):
        return []

    def setElements(self, elements):
        self._elements = elements

    def getElements(self):
        return self._elements

    def adjustElements(self, elements):
        """
            Every changed element instance given to this method will be replaced in the
            loaded memory storage, so it can be used during generation in the next run.

            :param elements: list<`imps.smithy.elements.Element.Element`> -- The modified elements
        """
        for key in elements.keys():
            if key in self.getElements().getLoadedElements().keys():
                self.getElements().replaceElement(elements[key])
