from imps.smithy.smarty.grammar.Life import Life


class Attack(Life):
    """
    This Class represents an payload in JavaScript.

    :todo: This is the place to integrate the JSFuck mutator.

    :param: elements: `imps.smithy.Elements.Elements`
    """
    _elements = []
    _populated = []

    def __init__(self, elements):
        self._elements = elements

    def __str__(self):
        return "".join(self.getPopulated())

    def getPopulated(self):
        populated = []
        for element in self._elements:
            string = str(element)
            populated.append(string)

        return populated

    def getElements(self):
        return self._elements

    def getLife(self):
        """
        This method is overwritten and returns the sum of all its elements lifes.

        :return: life: int -- The sum of all its elements lifes.
        """
        life = Life.getLifeFromList(self._elements)
        return life
