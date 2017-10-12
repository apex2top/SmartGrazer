import html

from imps.annelysa.Converter import Converter


class ResponseAnalyser(object):
    _config = {}
    _response = None
    _startIndex = None

    _modifiedElements = {}

    def __init__(self, config):
        self._config = config

    def setResponseObject(self, response):
        self._response = response
        return self

    def getResponse(self):
        return self._response

    def getModifiedElements(self):
        return self._modifiedElements

    def analyze(self):
        self._modifiedElements = {}

        # Is the first run SmartGrazer does.
        if self._startIndex is None:
            self._startIndex = self.findSubList(self._response.getDecPayload(), self._response.getDecHtml())

        if self._startIndex < 0:
            raise ValueError("Valid entry was not found!")

        print("Testing : " + str(self._response.getPayload()))

        sliceOfHTML = self._response.getDecHtml()[self._startIndex:]
        if str(self._response.getPayload()) in Converter.getString(sliceOfHTML):
            return {}

        elements = self._response.getPayload().getElements()

        step = 0
        suspicionMissing = None
        for element in elements:
            l = len(str(element))
            current = sliceOfHTML[step:step + l]

            if Converter.getString(current) == str(element):
                # seems like an element is missing in the response.
                if suspicionMissing:
                    self._modifiedElements[suspicionMissing.getKey()] = suspicionMissing
                    suspicionMissing = None

                step = step + len(str(element))
            else:
                # search for escaped char
                if Converter.getString(current) is "&":

                    i = 2
                    cs = step + i
                    invest = sliceOfHTML[cs:cs + 1]
                    while Converter.getString(invest) != ";":
                        i = i + 1
                        cs = step + i
                        invest = sliceOfHTML[cs:cs + 1]

                    escapedElement = html.unescape(Converter.getString(sliceOfHTML[step:i]))

                    if str(element) == escapedElement:
                        element.decreaseLife()
                        self._modifiedElements[element.getKey()] = element

                    step = step + i + 1
                else:
                    # not escaped with & ... ; -> maybe missing
                    element.decreaseLife()
                    suspicionMissing = element

        return self.getModifiedElements()

    def findSubList(self, sub, bigger):
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
