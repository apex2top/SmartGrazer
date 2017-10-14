from __future__ import print_function

import logging
import sys

from imps.annelysa.ResponseAnalyser import ResponseAnalyser
from imps.clint.CLIManager import CLIManager as Clint
from imps.confy.JSONConfigManager import JSONConfigManager as Confy
from imps.smithy.PayloadGeneratorFactory import PayloadGenerator as Smithy
from imps.smithy.smarty.grammar.attacks.Attack import Attack
from imps.webber.PayloadTester import PayloadTester as Webber


class SmartGrazer(object):
    """Representation of the SmartGrazer application."""

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
        """Initialize, configure, generate, execute and analyze the payloads.

            :returns:  int -- the return code.
            :raises: ValueError -- Thrown in situations, when a valid response cannot be found.
        """

        # Handle the cli args
        self.clint.handle()

        # Merge the config, the runconfig and the overrides into one big json-config
        self.confy.getConfig(self.clint.get('execute'), self.clint.parseOverwrites())

        if self.confy.getConfig()["smartgrazer"]["imps"]["webber"]["cleanup"] or self.clint.get("cleanup"):
            self.webber.cleanUp()

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
            modifiedElements = responseAnalyser.setResponseObject(response).analyze()
            self.smithy.adjustElements(modifiedElements)

        self.smithy = Smithy(self.confy.getConfig()["smartgrazer"]["imps"])

        successfull = None
        tries = 0

        while (not successfull) and tries < self.confy.getConfig()["smartgrazer"]["imps"]["webber"]["maxattempts"]:
            # Send generated payloads to webpage.
            self.webber.setPayloads(payloads)

            for response in self.webber.run(attackConfig):
                print("#" + str(tries) + " : " + str(response.getPayload()))

                # execute and analyze
                modifiedElements = responseAnalyser.setResponseObject(response).analyze()

                if not modifiedElements:
                    successfull = responseAnalyser.getResponse().getPayload()
                    print("#\t\t\tFound a good one: " + str(successfull))
                    break
                else:
                    self.smithy.adjustElements(modifiedElements)
                    payloads = self.smithy.generate()
                    tries = tries + 1

        if not successfull:
            print("#\t SmartGrazer: Could not find a working payload!")
            return 1

        return 0


if __name__ == "__main__":
    sys.exit((SmartGrazer()).run())
