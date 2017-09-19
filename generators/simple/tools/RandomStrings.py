import string

from django.utils.crypto import get_random_string

from generators.simple.tools.SpecialChars import SpecialChars


class RandomStrings(object):
    # Length of the generated String
    length = None
    # All available chars
    chars = ""
    # variable to map which charsets should be available, default ascii_lowercase
    control = {'lcc': None, 'ucc': None, 'scc': None}

    def __init__(self, lcc, ucc, scc, length=1):
        self.chars = ''
        self.control['lcc'] = lcc
        self.control['ucc'] = ucc
        self.control['scc'] = scc
        self.length = int(length)

    def setLength(self, length):
        self.length = int(length)

    def getAllowedChars(self):
        self.chars = ''
        for key in self.control:
            if self.control[key] == 'true':
                if key == 'lcc':
                    self.chars = self.chars + string.ascii_lowercase
                if key == 'ucc':
                    self.chars = self.chars + string.ascii_uppercase
                if key == 'scc':
                    scc = SpecialChars()
                    self.chars = self.chars + scc.getSpecialChars()

        return self.chars

    def getRandomString(self, chars=""):
        if chars != "":
            self.chars = chars
        else:
            self.chars = self.getAllowedChars()

        if self.chars != "":
            return get_random_string(self.length, self.chars)
        return ""
