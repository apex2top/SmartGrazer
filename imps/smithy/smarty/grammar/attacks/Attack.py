from imps.smithy.smarty.grammar.Life import Life


class Attack(Life):
    _life = 100
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
        life = Life.getLifeFromList(self._elements)
        return life
