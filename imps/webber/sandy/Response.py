from imps.annelysa.Converter import Converter


class Response(object):
    _file = ''
    _html = ''
    _decHtml = None

    _payload = ''
    _decPayload = None

    def __init__(self):
        pass

    # html handling + conversion to decimal
    def _loadHtmlFromFile(self):
        with open(self._file, "r") as report:
            self.setHtml(str(report.readlines()))

    def setResponseFile(self, file):
        self._file = file
        self._loadHtmlFromFile()

    def setHtml(self, html):
        self._html = html

    def getHtml(self):
        return self._html

    def getDecHtml(self):
        return Converter.getDecimal(self.getHtml())

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

        for element in self.getPayload().getElements():
            if element.getValue().isdigit():
                payload.append(element.getValue())
            else:
                for digit in Converter.getDecimal(element.getValue()):
                    payload.append(digit)

        return payload