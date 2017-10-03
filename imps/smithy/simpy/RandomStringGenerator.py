import random
import string

from django.utils.crypto import get_random_string


class RandomStringGenerator(object):
    LOWERCASE = 0
    UPPERCASE = 1
    DIGITS = 2
    MIXEDCASE = 3

    minlength = 1
    maxlength = 50

    def __init__(self, minLength, maxLength):
        self.minlength = minLength
        self.maxlength = maxLength
        self.chars = ''

    def _getRandomLength(self):
        return random.randint(self.minlength, self.maxlength)

    def get(self, type):
        if type == self.LOWERCASE:
            self.chars = string.ascii_lowercase
        if type == self.UPPERCASE:
            self.chars = string.ascii_uppercase
        if type == self.DIGITS:
            self.chars = string.digits
        if type == self.MIXEDCASE:
            self.chars = string.ascii_letters + string.digits

        if self.chars != "":
            return get_random_string(self._getRandomLength(), self.chars)

        return self.chars
