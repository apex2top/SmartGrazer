class Element(object):
    _key = None
    _value = None

    def __init__(self, key, value):
        self._key = key
        self._value = value

    def __str__(self):
        result = None
        if type(self._value) is list:
            result = self._pickWeightedRandom(self._value)
            print("Picked: " + str(result))
        else:
            result = self._value
        return str(result)

    def getKey(self):
        return self._key

    def getValue(self):
        return self._value

    def _pickWeightedRandom(self, weightedList):
        maxValue = Life.getLifeFromList(weightedList)
        value = randint(1, maxValue - 1)
        calcIndex = int(ceil(-.5 + sqrt(.25 + 2 * value)))

        entry = Life.getEntryForLife(calcIndex, weightedList)

        print(entry.getValue())

        return calcIndex
