import re
from random import randint

from config.Configuration import Configuration
from generators.simple.tools.RandomStrings import RandomStrings
from generators.simple.tools.SpecialChars import SpecialChars


class Generator(object):
    config = None
    randomStringGen = None

    def __init__(self):
        self.config = Configuration()
        self.randomStringGen = RandomStrings(
            lcc=self.config.get('randomstrings.chars.lowercase'),
            ucc=self.config.get('randomstrings.chars.uppercase'),
            scc=self.config.get('randomstrings.chars.special'),
            length=randint(0, int(self.config.get('get.request.length.start')))
        )

    def getRandomString(self, length=-1):
        return self.randomStringGen.getRandomString()

    def getMaxLengthRandomString(self):
        self.randomStringGen.setLength(self.config.get('get.request.length.max'))
        return self.randomStringGen.getRandomString()

    def getSpecialChars(self, maxLength=0):
        if maxLength < 1:
            return (SpecialChars()).getSpecialChars()

        # returning all special chars from generator.json and splits them into a maxlength long array
        return re.findall('.{1,' + str(maxLength) + '}', (SpecialChars()).getSpecialChars())
