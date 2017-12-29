from random import randint, choice

import math

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

        if randint(0, 3) < 3:
            return element

        strVal = str(element)
        strlen = len(str(strVal))

        index = math.ceil(strlen/2)


        newVal = strVal[:index-1] + strVal + strVal[index:]

        element.setMutated(newVal)
        return element
