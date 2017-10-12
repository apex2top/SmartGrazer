from random import choice

from imps.mutty.Mutator import Mutator

class Mutator(Mutator):
    def mutate(self, element):
        if not self._isEnabled():
            return element

        variants = []

        variants.append(str(element))
        variants.append(element.getDec())
        variants.append(element.getHex())

        element.setMutated(choice(variants))
        return element

