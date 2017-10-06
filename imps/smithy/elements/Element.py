import binascii

from imps.smithy.smarty.grammar.Life import Life


class Element(Life):
    _key = None
    _value = None
    _usage = []

    def __init__(self, key):
        self._key = key

    def __str__(self):
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
        if self._value.isdigit():
            return "0x"+format(int(self._value), "02x")

        return self._value
