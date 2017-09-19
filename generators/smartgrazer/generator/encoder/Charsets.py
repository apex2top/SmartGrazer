import json
from random import randint


class Charsets(object):
    charsets = None

    def __init__(self):
        self.loadFromConfig()

    def loadFromConfig(self):
        with open('config/mutator.json') as json_data:
            data = json.load(json_data)
        self.charsets = data['charsets']

    def getAvailableCharsets(self):
        return self.charsets

    def getRandomCharset(self):
        index = randint(0, len(self.charsets) - 1)
        return self.charsets[index]

    def encode(self, string, set=None):
        if set is None:
            set = self.getRandomCharset()

        return {"original": string, "encoded": string.encode(set), "charset": set}
