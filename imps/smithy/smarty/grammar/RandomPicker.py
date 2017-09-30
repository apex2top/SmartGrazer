from random import randint

from imps.smithy.smarty.grammar.Life import Life


class RandomPicker(object):
    def pickWeightedRandom(weightedList):
        sortedList = Life.sortASC(weightedList)

        maxValue = Life.getLifeFromList(sortedList)
        currentLimit = randint(0, maxValue + 1)

        currentSum = 0
        for entry in sortedList:
            currentSum = currentSum + entry.getLife()

            if (currentSum >= currentLimit):
                return entry

        return entry
