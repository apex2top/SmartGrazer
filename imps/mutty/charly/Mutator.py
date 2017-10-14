from random import choice

from imps.mutty.MutatorGeneral import MutatorGeneral


class Mutator(MutatorGeneral):
    """ This class is used to exchange some characters with an alternative representation.
    """

    def mutate(self, element):
        """
            Replace a given Element with an alternative representation.

            The whitelisted files are configured in elements.mutator.json

            :param element: `imps.smithy.elements.Element.Element` -- The current element, which should be mutated.

            :return: element: `imps.smithy.elements.Element.Element` -- The modified element.
        """

        if not self._isEnabled():
            return element

        variants = []

        variants.append(str(element))
        variants.append(element.getDec())
        variants.append(element.getHex())

        element.setMutated(choice(variants))
        return element
