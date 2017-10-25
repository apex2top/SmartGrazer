import random

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy.smarty.grammar.outbreaks.Outbreak import Outbreak


class Outbreaks(object):
    """
    This class loads, initiates and populates pattern based outbreaks.

    :param: filePath: str -- The path to the JSON configuration, containing the outbreak patterns.
    """
    _elements = None

    _outbreakPatterns = []
    _outbreak = []

    def __init__(self, filePath):
        self._outbreakPatterns = (JSONConfigManager(filePath)).getConfig()

    def getOutbreak(self):
        """
        This method loads and initiate the components of an outbreak.

        :raises: ValueError -- Thrown, when no Elements instance is provided.
        :returns: `imps.smithy.smarty.outbreaks.Outbreak.Outbreak`
        """
        pattern = random.choice(self._outbreakPatterns)

        components = []

        for entry in pattern:
            if self._elements is None:
                raise ValueError(
                    "Elements are not initialized! Please provide an elements instance via setElements.")
            element = self._elements.getElementForUsage(entry)
            components.append(element)

        return Outbreak(components)

    def setElements(self, elements):
        self._elements = elements