from random import randint, choice

from imps.mutty.MutatorGeneral import MutatorGeneral


class Mutator(MutatorGeneral):
    """ This class is used to exchange some characters with their upper case variant.
    """

    def mutate(self, element):
        """
            Replace random chars with their uppercase representation.

            The whitelisted files are configured in elements.mutator.json

            :param element: `imps.smithy.elements.Element.Element` -- The current element, which should be mutated.

            :return: element: `imps.smithy.elements.Element.Element` -- The modified element.
        """
        if not self._isEnabled():
            return element

        if randint(0,1) > 0:
            return element

        spaces = [7, 9, 10, 11, 12, 32]

        strVal = str(element)
        strlen = len(str(strVal))

        index = randint(0, strlen - 1)
        i = 0

        newVal = ''
        for c in strVal:
            if i == index:
                newVal = newVal + chr(choice(spaces))

            newVal = newVal + c
            i = i+1

        element.setMutated(newVal)
        return element
