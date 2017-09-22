from __future__ import print_function

import logging
import sys

from imps.clint.CLIManager import CLIManager as Clint
from imps.confy.JSONConfigManager import JSONConfigManager as Confy
from imps.smithy.PayloadGenerator import PayloadGenerator as Smithy
from imps.webber.PayloadTester import PayloadTester as Webber


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
        self.confy.getConfig(self.clint.get('runconfig'), self.clint.parseOverwrites())

        self.smithy = Smithy(self.confy.getConfig()["smartgrazer"]["imps"])
        payloads = self.smithy.generate()

        # Generate the payloads and exit
        if self.clint.get('generate'):
            print(payloads)
            exit(0)

        if not self.clint.get('generate') and not self.clint.get('execute'):
            raise ValueError("You either have to set the -g or the -x mode.")
            exit(1)

        self.webber = Webber(self.confy)

        executeValidRun = True
        self.webber.run(executeValidRun)

        simpy = self.smithy.getSimpy()
        simplePayloads = simpy.generate()

        self.webber.setPayloads(simplePayloads)
        self.webber.run(False)

        return 0

if __name__ == "__main__":
    sys.exit((SmartGrazer()).run())
