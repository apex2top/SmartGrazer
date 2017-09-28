from math import ceil, sqrt
from random import randint

from imps.smithy.smarty.grammar.Life import Life


class RandomPicker(object):
    def pickWeightedRandom(weightedList):
        maxValue = Life.getLifeFromList(weightedList)
        if maxValue > 1:
            nearlymax = maxValue - 1
            value = randint(1, nearlymax)
        else:
            value = 1

        calcIndex = int(ceil(-.5 + sqrt(.25 + 2 * value)))

        entry = Life.getEntryForLife(calcIndex, weightedList)

        return entry
