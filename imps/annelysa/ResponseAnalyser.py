class ResponseAnalyser(object):
    _config = {}
    _response = None
    _startIndex = 0

    def __init__(self, config):
        self._config = config

    def setResponseObject(self, response):
        self._response = response
        return self

    def getResponse(self):
        return self._valid

    def analyze(self):
        print("-> " + str() + " => " + str(self._response.getPayload()))
        pass
