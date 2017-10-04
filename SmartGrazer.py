from __future__ import print_function

import logging
import sys

from imps.clint.CLIManager import CLIManager as Clint
from imps.confy.JSONConfigManager import JSONConfigManager as Confy
from imps.smithy.PayloadGenerator import PayloadGenerator as Smithy
from imps.smithy.smarty.grammar.attacks.Attack import Attack
from imps.webber.PayloadTester import PayloadTester as Webber
from imps.annelysa.ResponseAnalyser import ResponseAnalyser


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

        self.webber = Webber(self.confy.getConfig()["smartgrazer"]["imps"]["sandy"])

    def run(self):
        # Handle the cli args
        self.clint.handle()

        # Merge the config, the runconfig and the overrides into one big json-config
        self.confy.getConfig(self.clint.get('execute'), self.clint.parseOverwrites())

        self.smithy = Smithy(self.confy.getConfig()["smartgrazer"]["imps"])
        payloads = self.smithy.generate()

        # Generate the payloads and exit
        if self.clint.get('generate'):
            for p in payloads:
                print(p)
            exit(0)

        responseAnalyser = ResponseAnalyser(self.confy.getConfig()["smartgrazer"]["imps"]["annelysa"])

        validConfig = self.confy.getConfig()["runconfig"]["valid"]
        attackConfig = self.confy.getConfig()["runconfig"]["attack"]

        # Load the instance of simpy to perform valid request and simple payloads
        simpy = self.smithy.getSimpy()

        # Execute valid request to know the pages' default response
        # ! only one result
        attack = Attack([])
        self.webber.setPayloads([attack])
        response = (self.webber.run(validConfig)).pop()

        responseAnalyser.setResponseObject(response).analyze()

        # Simple tests to teach smarty how to generate
        simplePayloads = simpy.generate()

        # Send simple payloads to webpage.
        self.webber.setPayloads(simplePayloads)
        # execute and analyze
        for response in self.webber.run(attackConfig):
            responseAnalyser.setResponseObject(response).analyze()

        # Send generated payloads to webpage.
        self.webber.setPayloads(payloads)
        # execute and analyze
        for response in self.webber.run(attackConfig):
            responseAnalyser.setResponseObject(response).analyze()


if __name__ == "__main__":
    sys.exit((SmartGrazer()).run())
