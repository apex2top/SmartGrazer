from random import choice, randint

from imps.smithy.smarty.grammar.Life import Life


class Element(Life):
    """ This class represents an element entity according either to an payload or an attack.

        Its values can contain strings, chars or chars in decimal encoded manner.
    """

    _key = None
    _value = None
    _mutated = None
    _usage = []

    def __init__(self, key):
        self._key = key

    def __str__(self):
        """ The built-in `__str__` method is overwritten, so that an element can always be rendered to string by printing it or
            casting it to string via the `str()` method.

            :return: str -- the string value.
        """
        if self._mutated:
            return self._mutated

        if type(self._value) is int:
            return chr(self._value)

        if self._value.isdigit():
            return chr(int(self._value))
        else:
            return self._value

    def getValue(self):
        return self._value

    def getKey(self):
        return self._key

    def setValue(self, value):
        self._value = value

    def getUsage(self):
        return self._usage

    def setUsage(self, usage):
        self._usage = usage

    def getHex(self):
        """
        Returns hex representations of this element if the value is a digit.

        :return: str -- The hex representation.
        """
        if self._value.isdigit():
            # value to insert
            val = format(int(self._value), "02x")

            # insert zero
            zeroCount = randint(0, 5)

            zval = val
            for i in range(0, zeroCount):
                zval = "0" + zval

            values = []

            values.append("%" + val + ";")
            values.append("&#x" + zval + ";")
            values.append("&#X" + zval + ";")

            return choice(values)

        return self._value

    def getDec(self):
        """
        Renders the digit value in html-friendly
        :return: str -- the html friendly decimal representation
        """
        if self._value.isdigit():
            return "&#" + str(self._value)

        return self._value

    def setMutated(self, value):
        self._mutated = value

    def getMutated(self):
        return self._mutated
