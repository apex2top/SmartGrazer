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
        return self._valid

    def analyze(self):
        # Is the first run SmartGrazer does.
        if self._startIndex is None:
            self._startIndex = self.findSubList(self._response.getDecPayload(), self._response.getDecHtml())

        if self._startIndex < 0:
            raise ValueError("Valid entry was not found!")

        payloadSliceOfHTML = self._response.getDecHtml()[self._startIndex - 1:]

        if payloadSliceOfHTML == self._response.getPayload():
            print("Found payload!")
            return True

        # @TODO Hier jetzt alle elemente des payload durchgehen und prüfen, ob diese vorhanden sind.
        # alle nicht druckbaren zeichen werden in 0x00 oder \n dargestellt, hier muss dementspechende
        # konvertierung vorgenommen werden.

        # @TODO das elements-object vom smartgrazer übernehmen.
        # für jedes element welches nicht gefunden wird, wird decreaseLife aufgerufen. min. 1
        # für jedes gefundene wird increaseLife aufgerufen. max. 100


        pass

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
                    return pos
        except ValueError:
            return -1
