from imps.annelysa.Converter import Converter


class ResponseAnalyser(object):
    _config = {}
    _response = None
    _startIndex = None

    def __init__(self, config):
        self._config = config

    def setResponseObject(self, response):
        self._response = response
        return self

    def getResponse(self):
        return self._response

    def analyze(self):
        # Is the first run SmartGrazer does.
        if self._startIndex is None:
            self._startIndex = self.findSubList(self._response.getDecPayload(), self._response.getDecHtml())

        if self._startIndex < 0:
            raise ValueError("Valid entry was not found!")

        sliceOfHTML = self._response.getDecHtml()[self._startIndex:]

        if str(self._response.getPayload()) in Converter.getString(sliceOfHTML):
            print("Found payload without analyzing!\t\t>>>>>>>>>>>>>>>\t" + str(self._response.getPayload()))
            return True

        return False

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
