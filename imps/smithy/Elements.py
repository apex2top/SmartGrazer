import logging
from random import randint

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.mutty.PayloadMutator import PayloadMutator
from imps.smithy.elements.Element import Element
from imps.smithy.smarty.grammar.Life import Life


class Elements(object):
    """ This class manages the loading, instantiation and maintaining of all element instances during generation.

        :param filePath: str -- The JSON-File containing the elements.
    """
    _rawElements = {}
    _loadedElements = {}
    _memory = {}
    _defaultLife = 100
    _defaultLifes = {}
    _mutator = None

    # private

    def __init__(self, filePath):
        self._rawElements = (JSONConfigManager(filePath)).getConfig()
        self._mutator = PayloadMutator(filePath.replace(".json", ".mutator.json"))

    def _getElementsWithUsage(self, usage):
        """ This method returns a list of elements with a given usage from the rawElements - memory.

            :param usage: str - the usage like e.g. SPACE = ["/","+"," "]

            :return: list<`imps.smithy.elements.Element.Element`>
        """
        elements = []

        for entry in self._rawElements:
            if usage in self._rawElements[entry]:
                elements.append(entry)

        return elements

    def _getRawElement(self, identifier):
        # handle dharmas fixed generated one char elements e.g. '='
        if not identifier.isdigit() and len(identifier) == 1:
            identifier = ord(identifier)

        if identifier in self._rawElements.keys():
            return {'key': identifier, 'usage': self._rawElements[identifier]}

        return {'key': identifier, 'usage': []}

    def setDefaultLifes(self, defaultLifes):
        self._defaultLifes = defaultLifes

    def getDefaultLife(self, key):
        if key in self._defaultLifes.keys():
            life = self._defaultLifes[key]
            logging.getLogger('SmartGrazer').debug("Initialize element: " + str(key) + " with " + str(life) + " life!")
            return life

        return self._defaultLife

    def getElement(self, identifier):
        if identifier in self._loadedElements.keys():
            return self._loadedElements[identifier]

        raw = self._getRawElement(identifier)

        if raw['key'] in self._loadedElements.keys():
            element = self._loadedElements[raw['key']]
        else:
            element = Element(raw['key'])
            element.setValue(raw['key'])
            element.setUsage(raw['usage'])
            element.setLife(self.getDefaultLife(raw['key']))

        return self._mutator.mutate(element)

    def clearElementMemory(self):
        self._memory = {}

    def clearMutations(self):
        for key in self._loadedElements.keys():
            self._loadedElements[key].setMutated(None)
        return self

    def getElementForUsage(self, usage):
        memkey = None

        # Important! some elements must be the same char e.g. QUOTES
        # Therefore the user can attach ':[0-9]' to some tags
        # these randomly chosen chars will be saved to _memory[key][memkey]

        if len(usage) > 1 and usage[-2] == ':':
            memkey = usage[-1]
            usage = usage[0:-2]

            if not usage in self._memory:
                self._memory[usage] = {}

            if not memkey in self._memory[usage]:
                self._memory[usage][memkey] = None
            else:
                return self._memory[usage][memkey]

        candidates = self.getElementsForUsage(usage)

        element = self._pickWeightedRandom(candidates)

        # now we can store the picked element for later
        if memkey:
            self._memory[usage][memkey] = element

        return self._mutator.mutate(element)

    def getElementsForUsage(self, usage):
        # get all element identifiers for usage e.g. SPACE
        elements = self._getElementsWithUsage(usage)
        if not elements:
            # all other identifier e.g. ATTACK, SPACE
            elements.append(usage)

        # get element instances
        candidates = []
        for elementid in elements:
            element = None

            if elementid in self._loadedElements.keys():
                element = self._loadedElements[elementid]
            else:
                element = Element(elementid)
                element.setValue(elementid)
                element.setUsage(usage)
                element.setLife(self.getDefaultLife(elementid))

                self._loadedElements[elementid] = element

            candidates.append(element)

        return candidates

    def getRawElements(self):
        return self._rawElements

    def getLoadedElements(self):
        return self._loadedElements

    def replaceElement(self, element):
        # print(element.getKey() + " -> " + str(element) + " => " + str(element.getLife()) + " >> " + str(self._loadedElements[element.getKey()].getLife()))
        self._loadedElements[element.getKey()] = element

    def _pickWeightedRandom(self, weightedList):
        """
        This method gets a weighted list of elements
        and returns a random but weighted selected element.

        :param: weightedList: list<`imps.smithy.elements.Element.Element`> -- A list with Elements

        :return: choise: `imps.smithy.elements.Element.Element` -- The selected element
        """
        sortedList = Life.sortASC(weightedList)

        maxValue = Life.getLifeFromList(sortedList)
        currentLimit = randint(0, maxValue + 1)

        currentSum = 0
        for entry in sortedList:
            currentSum = currentSum + entry.getLife()

            if currentSum >= currentLimit:
                return entry

        return entry