import urllib.parse
from random import randint

from generators.smartgrazer.Settings import Settings


class Encoder(object):
    encodings = None

    def __init__(self):
        settings = Settings()
        self.encodings = settings.getSettings()['encodings']
        pass

    def getAvailableEncodings(self):
        return self.encodings

    def getRandom(self):
        index = randint(0, len(self.encodings) - 1)
        return self.encodings[index]

    def encode(self, string, encoder=None):
        if encoder is None:
            encoder = self.getRandom()

            return string

    def urlencode(self, params):
        return urllib.parse.urlencode(params)
