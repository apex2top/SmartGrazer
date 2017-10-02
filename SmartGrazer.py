from __future__ import print_function

import logging
import sys

from imps.clint.CLIManager import CLIManager as Clint
from imps.confy.JSONConfigManager import JSONConfigManager as Confy
from imps.smithy.PayloadGenerator import PayloadGenerator as Smithy
from imps.smithy.smarty.grammar.attacks.Attack import Attack
from imps.webber.PayloadTester import PayloadTester as Webber


class SmartGrazer(object):
    clint = None
    confy = None
    smithy = None

    def __init__(self):
        self.clint = Clint()
        self.confy = Confy()

        loggerConfig = self.confy.getConfig()["smartgrazer"]["logging"]
        logging.getLogger("SmartGrazer").setLevel(loggerConfig["level"])
        logging.basicConfig(format='%(levelname)s:\t%(message)s')

    def run(self):
        # Handle the cli args
        self.clint.handle()

        # Merge the config, the runconfig and the overrides into one big json-config
        self.confy.getConfig(self.clint.get('runconfig'), self.clint.parseOverwrites())

        self.smithy = Smithy(self.confy.getConfig()["smartgrazer"]["imps"])
        payloads = self.smithy.generate()

        # Generate the payloads and exit
        if self.clint.get('generate'):
            for p in payloads:
                # p.printKeys()
                print(p)
            exit(0)

        if not self.clint.get('generate') and not self.clint.get('execute'):
            raise ValueError("You either have to set the -g or the -x mode.")
            exit(1)

        self.webber = Webber(self.confy.getConfig()["smartgrazer"]["imps"]["sandy"])
        validConfig = self.confy.getConfig()["runconfig"]["valid"]
        attackConfig = self.confy.getConfig()["runconfig"]["attack"]

        # Load the instance of simpy to perform valid request and simple payloads
        simpy = self.smithy.getSimpy()

        # Execute valid request to know the pages' default response
        # ! only one result
        attack = Attack([])
        self.webber.setPayloads([attack])
        self.webber.run(validConfig)

        # Simple tests to teach smarty how to generate
        simplePayloads = simpy.generate()

        # Send simple payloads to webpage.
        self.webber.setPayloads(simplePayloads)
        # execute and analyze
        self.webber.run(attackConfig)

        # Send generated payloads to webpage.
        self.webber.setPayloads(payloads)
        # execute and analyze
        self.webber.run(attackConfig)

if __name__ == "__main__":
    sys.exit((SmartGrazer()).run())
