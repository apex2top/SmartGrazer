from random import randint

from imps.mutty.Mutator import Mutator


class Mutator(Mutator):
    def mutate(self, element):
        if not self._isEnabled():
            return element

        strVal = str(element)
        newVal = ''
        for c in strVal:
            if randint(0, 1) > 0:
                newVal = newVal + c.upper()
            else:
                newVal = newVal + c

        element.setMutated(newVal)
        return element
