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

        # Execute valid request to know the pages' default response
        self.webber.validRun()

        # Simple tests to teach smarty how to generate
        simpy = self.smithy.getSimpy()
        simplePayloads = simpy.generate()

        # Send simple payloads to webpage.
        self.webber.setPayloads(simplePayloads)
        # execute and analyze
        self.webber.run()

        # Send generated payloads to webpage.
        self.webber.setPayloads(payloads)
        # execute and analyze
        print(self.webber.run())




        return 0

if __name__ == "__main__":
    sys.exit((SmartGrazer()).run())
