import binascii
import html
from random import choice, randint

from imps.mutty.PayloadMutator import PayloadMutator
from imps.smithy.smarty.grammar.Life import Life


class Element(Life):
    _key = None
    _value = None
    _mutated = None
    _usage = []

    def __init__(self, key):
        self._key = key

    def __str__(self):
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
        if self._value.isdigit():
            # value to insert
            val = format(int(self._value), "02x")

            # insert zero
            zeroCount = randint(0,5)

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
        if self._value.isdigit():
            return "&#" + str(self._value)

        return self._value

    def setMutated(self, value):
        self._mutated = value

    def getMutated(self):
        return self._mutated
