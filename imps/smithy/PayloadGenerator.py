import importlib


class PayloadGenerator(object):
    generator = None

    def __init__(self, name):
        importString = "imps.smithy.{0}".format(name)
        self.generator = importlib.import_module(importString + ".PayloadGenerator", )

    def getGenerator(self):
        return self.generator
