import logging

from w3lib.html import replace_entities

from imps.annelysa.Converter import Converter


class ResponseAnalyser(object):
    """ This class is responsible for analyzing website-responses.
    """
    _config = {}
    _response = None
    _startIndex = None
    _logger = None

    AND = 38
    SEMICOLON = 59

    _modifiedElements = {}

    def __init__(self, config):
        self._config = config
        self._logger= logging.getLogger("SmartGrazer")

    def setResponseObject(self, response):
        self._response = response
        return self

    def getResponse(self):
        return self._response

    def getModifiedElements(self):
        return self._modifiedElements

    def analyze(self):
        """
            This method takes the response, and searches the payloads in the according responses.

            During one smartgrazer run there is only one response-object, holding all loaded elements and adjusting their life.

            :return: list<`imps.smithy.elements.Element.Element`>
        """
        self._modifiedElements = {}

        # Is the first run SmartGrazer does.
        if self._startIndex is None:
            self._startIndex = self.findSubList(self._response.getDecPayload(), self._response.getDecHtml())

        if self._startIndex < 0:
            raise ValueError("Valid entry was not found!")

        sliceOfHTML = self._response.getDecHtml()[self._startIndex:]
        if str(self._response.getPayload()) in Converter.getString(sliceOfHTML):
            return {}

        self._logger.debug("#> Analyzing: " + str(self._response.getPayload()))
        elements = self._response.getPayload().getElements()

        step = 0
        for element in elements:
            l = len(str(element))

            nextResponseElementDecList = self._getElementFromResponse(sliceOfHTML[step:])
            nextResponseElementString = Converter.getString(nextResponseElementDecList)

            if str(element) == nextResponseElementString:
                step = step + len(nextResponseElementDecList)
            else:
                if nextResponseElementString == '':
                    self._logger.debug("Missing element: " + str(element) + " - Life: " + str(element.getLife()))
                    element.decreaseLife()
                    self._addToModified(element)

                next = int(nextResponseElementDecList[0])
                if next == self.AND:
                    escapedElement = replace_entities(nextResponseElementString)
                    if escapedElement == str(element):
                        self._logger.debug("Decreasing: " + str(element) + " - Life: " + str(element.getLife()))
                        element.decreaseLife()
                        self._addToModified(element)
                        step = step + len(nextResponseElementDecList)
                    else:
                        self._logger.debug("Missing element: " + str(element) + " - Life: " + str(element.getLife()))
                        element.decreaseLife()
                        self._addToModified(element)
                else:
                    self._logger.debug("Missing element: " + str(element) + " - Life: " + str(element.getLife()))
                    element.decreaseLife()
                    self._addToModified(element)

        return self.getModifiedElements()

    def _addToModified(self, element):
        if not element.getKey() in self._modifiedElements:
            self._modifiedElements[element.getKey()] = element

    def _getElementFromResponse(self, declist):
        index = 0

        firstchar = int(declist[index])
        if firstchar != self.AND:
            return [declist[index]]


        if firstchar == self.AND:
            index = index + 1
            nextchar = int(declist[index])

            while nextchar != self.SEMICOLON and len(declist)-1 <= index:
                print(index)
                index = index + 1
                nextchar = int(declist[index])

            return declist[0:index+1]

        return []

    def findSubList(self, sub, bigger):
        """ A method to search array in a nother array
            Source: https://stackoverflow.com/a/2251638

            :param sub: list<int> -- the needle to search
            :param bigger: list<int> -- the haystack

            :return: int -- the start index >= 0, else -1
        """
        if not bigger:
            return -1
        if not sub:
            return 0
        first, rest = sub[0], sub[1:]
        pos = 0
        try:
            while True:
                pos = bigger.index(first, pos) + 1
                if not rest or bigger[pos:pos + len(rest)] == rest:
                    return pos - 1
        except ValueError:
            return -1
