from random import randint

from imps.smithy.smarty.grammar.Life import Life


class Grammar(Life):
    _life = 1
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

    def populateAttack(self, attack):
        payload = []
        for element in self._elements:
            if element.getKey() == "ATTACK":
                element.setValue(str(attack))
                for attackElements in attack.getElements():
                    payload.append(attackElements)
            else:
                payload.append(element)

    def populateRandomText(self, text):
        for element in self._elements:
            if element.getKey() == "TEXT":
                element.setValue(text)
