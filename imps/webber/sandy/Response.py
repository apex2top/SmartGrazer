import os

from imps.annelysa.Converter import Converter


class Response(object):
    """
    This class represents the response received from the SUT.
    """

    _file = ''
    _html = ''
    _payload = ''

    # html handling + conversion to decimal
    def _loadHtmlFromFile(self):
        lines = []
        with open(self._file, "r", encoding="utf8") as report:
            lines = report.readlines()

        self.setHtml("".join(lines))

    def setResponseFile(self, file):
        self._file = file
        self._loadHtmlFromFile()

    def getResponseFile(self):
        return self._file

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

    def clean(self):
        files = [
            self.getResponseFile(),
            self.getResponseFile().replace('.html', '')
        ]
        for file in files:
            if os.path.isfile(file):
                os.unlink(file)

    def getElements(self):
        result = {}
        for element in self.getPayload().getElements():
            result[element.getKey()] = element

        return result

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
