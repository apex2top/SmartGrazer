from random import randint

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy.smarty.grammar.RandomPicker import RandomPicker
from imps.smithy.smarty.grammar.elements.Element import Element


class Elements(object):
    _rawElements = {}
    _loadedElements = {}
    _memory = {}
    _defaultLife = 1

    def __init__(self, filePath):
        self._rawElements = (JSONConfigManager(filePath)).getConfig()
        
    def setDefaultLife(self, amount):
        self._defaultLife = amount

    def getDefaultLife(self):
        if self._defaultLife > 100:
            return randint(1, 101)
        return self._defaultLife


    def getElement(self, key):
        memkey = None

        # get the instance from memory
        if key in self._loadedElements.keys():
            value = self._loadedElements[key]

            if type(value) is list:
                return RandomPicker.pickWeightedRandom(self._loadedElements[key])

        # Important! some elements must be the same char e.g. QUOTES
        # Therefore the user can attach ':[0-9]' to some tags
        # these randomly chosen chars will be saved to _memory[key][memkey]
        if key[-2] == ':':
            memkey = key[-1]
            key = key[0:-2]

            if not key in self._memory:
                self._memory[key] = {}

            if not memkey in self._memory[key]:
                self._memory[key][memkey] = None
            else:
                return self._memory[key][memkey]

        # create a list of possible values
        self._loadedElements[key] = []

        ### create the instance(s)

        # a normal string or number is given e.g. plaintext -> alert
        if not key in self._rawElements.keys():
            element = Element(key, key)
            element.setLife(self.getDefaultLife())
            # store the created instance to memory
            self._loadedElements[key].append(element)
        elif not type(self._rawElements[key]) is list:
            # a value representing a tag e.g. TAG_SCRIPT
            element = Element(key, self._rawElements[key])
            element.setLife(self.getDefaultLife())

            # store the created instance to memory
            self._loadedElements[key].append(element)
        else:
            # in case there are multiple chars for one key e.g. SPACE
            for representation in self._rawElements[key]:
                if type(representation) is int:
                    representation = str(representation)

                value = representation

                element = Element(key, value)
                element.setLife(self.getDefaultLife())

                # store the created instance to memory
                self._loadedElements[key].append(element)

            # after all chars has been added, pick one random, depending on its weight
            element = RandomPicker.pickWeightedRandom(self._loadedElements[key])

        # now we can store the picked element for later
        if memkey:
            self._memory[key][memkey] = element

        return element

    def getRawElements(self):
        return self._rawElements

    def getLoadedElements(self):
        return self._loadedElements
