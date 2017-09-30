from imps.smithy.smarty.grammar.Life import Life


class Element(Life):
    _key = None
    _value = None

    def __init__(self, key, value):
        self._key = key
        self._value = value

    def __str__(self):
        if self._value.isdigit():
            return chr(int(self._value))
        else:
            return self._value

    def getKey(self):
        return self._key

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value
