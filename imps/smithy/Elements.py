from random import randint

import math

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.mutty.PayloadMutator import PayloadMutator
from imps.smithy.elements.Element import Element
from imps.smithy.smarty.grammar.Life import Life
from imps.smithy.smarty.grammar.RandomPicker import RandomPicker


class Elements(object):
    _rawElements = {}
    _loadedElements = {}
    _memory = {}
    _defaultLife = 1
    _mutator = None

    # private

    def __init__(self, filePath):
        self._rawElements = (JSONConfigManager(filePath)).getConfig()
        self._mutator = PayloadMutator(filePath.replace(".json",".mutator.json"))

    def _getElementsWithUsage(self, usage):
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

    def setDefaultLife(self, amount):
        self._defaultLife = amount

    def getDefaultLife(self):
        if self._defaultLife > 100:
            return randint(1, 101)
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
            element.setLife(self.getDefaultLife())

        return self._mutator.mutate(element)

    def clearMutations(self):
        for key in self._loadedElements.keys():
            self._loadedElements[key].setMutated(None)
        return self

    def getElementForUsage(self, usage):
        memkey = None

        # Important! some elements must be the same char e.g. QUOTES
        # Therefore the user can attach ':[0-9]' to some tags
        # these randomly chosen chars will be saved to _memory[key][memkey]
        if usage[-2] == ':':
            memkey = usage[-1]
            usage = usage[0:-2]

            if not usage in self._memory:
                self._memory[usage] = {}

            if not memkey in self._memory[usage]:
                self._memory[usage][memkey] = None
            else:
                return self._memory[usage][memkey]

        candidates = self.getElementsForUsage(usage)

        element = RandomPicker.pickWeightedRandom(candidates)

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
                element.setLife(self.getDefaultLife())

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