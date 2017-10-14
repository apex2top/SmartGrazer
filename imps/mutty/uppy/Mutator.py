from random import randint

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

        strVal = str(element)
        newVal = ''
        for c in strVal:
            if randint(0, 1) > 0:
                newVal = newVal + c.upper()
            else:
                newVal = newVal + c

        element.setMutated(newVal)
        return element
