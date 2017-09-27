from pygments.util import xrange

from imps.webber.annelysa.Converter import Converter


class ResponseAnalyser(object):
    response = ''
    runConfig = {}

    def __init__(self, config):
        self.config = config

    def loadResponse(self, file):
        f = open(file, 'r')
        self.response = Converter.getDecimal(f.read().encode("UTF-8"))

    def loadRunConfig(self, file):
        renamed = file.replace(".html", '.json')
        f = open(renamed, 'r')
        config = f.read()

        self.runConfig = eval(config)

    def analyze(self):
        results = {
        }

        params = self.runConfig["action"]["params"]

        for type in params:
            for key in params[type]:
                value = params[type][key]

                # can entry be found?
                deciarray = Converter.getDecimal(value.encode())
                indexes = self.contains(deciarray, self.response)
                if not indexes is False:
                    results[value.encode()] = {"found": True}

                    print(indexes)

                else:
                    results[value.encode()] = {"found": False}

        return results

    def contains(self, small, big):
        for i in xrange(len(big) - len(small) + 1):
            for j in xrange(len(small)):
                if big[i + j] != small[j]:
                    break
            else:
                return i, i + len(small)
        return False
