import logging
import sys

from imps.clint.CLIManager import CLIManager as Clint
from imps.confy.JSONConfigManager import JSONConfigManager as Confy
from imps.smithy.PayloadGenerator import PayloadGenerator as Smithy


class SmartGrazer(object):
    clint = None
    confy = None
    smithy = None

    def __init__(self):
        logging.getLogger().setLevel(logging.INFO)
        logging.basicConfig(format='%(levelname)s:\t%(message)s')

        self.clint = Clint()
        self.confy = Confy()
        pass

    def run(self):
        # Handle the cli args
        self.clint.handle()

        # Merge the config, the runconfig and the overrides into one big json-config
        self.confy.getConfig(self.clint.get('target'), self.clint.parseOverwrites())

        # Create an instance of the configured generator
        generatorname = "simpy"

        self.smithy = Smithy(generatorname)
        self.smithy.getGenerator()

        return 0


if __name__ == "__main__":
    sys.exit((SmartGrazer()).run())
