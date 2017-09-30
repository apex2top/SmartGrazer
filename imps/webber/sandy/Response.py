class Response(object):
    _html = ''
    _decHtml = None

    _payload = ''
    _decPayload = None

    def __init__(self):
        pass

    # html handling + conversion to decimal
    def loadHtmlFromFile(self, file):
        with open(file, "r") as report:
            self.setHtml(str(report.readlines()))

    def setHtml(self, html):
        self._html = html

    def getHtml(self):
        return self._html

    def getDecimalHtml(self):
        return self._getDecimalFromString(self.getHtml())

    # payload handling + conversion to decimal
    def setPayload(self, payload):
        self._payload = payload

    def getPayload(self):
        return self._payload

    def getStrPayload(self):
        payload = []
        for element in self.getPayload():
            payload.append(str(element))
        return payload

    def getDecPayload(self):
        payload = []
        for element in self.getPayload():
            if element.getValue().isdigit():
                return element.getValue()
            else:
                return self._getDecimalFromString(element.getValue())
        return payload

    def _getDecimalFromString(self, string):
        return ''.join(str(ord(c)) for c in string)
