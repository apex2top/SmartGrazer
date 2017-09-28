from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy.simpy.grammar.elements.Element import Element


class Elements(object):
    _rawElements = {}
    _loadedElements = {}

    def __init__(self, filePath):
        self._rawElements = (JSONConfigManager(filePath)).getConfig()

    def getElement(self, entry):
        # get the instance from memory
        if entry in self._loadedElements.keys():
            return self._loadedElements[entry]

        # create the instance
        if entry in self._rawElements.keys():
            element = Element(entry, self._rawElements[entry])
        else:
            element = Element(entry, entry)

        # store the created instance to memory
        self._loadedElements[entry].append(element)

        return self._loadedElements[entry]

    def storeElement(self, key, element):
        self._loadedElements[key] = element

    def getRawElements(self):
        return self._rawElements

    def getLoadedElements(self):
        return self._loadedElements
