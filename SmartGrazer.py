from __future__ import print_function

import logging
import os
import sys
import time

from imps.annelysa.ResponseAnalyser import ResponseAnalyser
from imps.annelysa.ResponseExecutor import ResponseExecutor
from imps.clint.CLIManager import CLIManager as Clint
from imps.confy.JSONConfigManager import JSONConfigManager as Confy
from imps.smithy.PayloadGeneratorFactory import PayloadGeneratorFactory as Smithy
from imps.smithy.smarty.grammar.attacks.Attack import Attack
from imps.webber.PayloadTester import PayloadTester as Webber


class SmartGrazer(object):
    """Representation of the SmartGrazer application."""

    def run(self):
        """Initialize, configure, generate, execute and analyze the payloads.

            :returns:  int -- the return code.
            :raises: ValueError -- Thrown in situations, when a valid response cannot be found.
        """

        clint = Clint()
        confy = Confy()

        loggerConfig = confy.getConfig()["smartgrazer"]["logging"]
        smartgrazer = logging.getLogger("SmartGrazer")
        smartgrazer.setLevel(loggerConfig["level"])
        logging.basicConfig(format='%(levelname)s:\t%(message)s')

        webber = Webber(confy.getConfig()["smartgrazer"]["imps"]["sandy"])

        # Handle the cli args
        clint.handle()

        # Merge the config, the runconfig and the overrides into one big json-config
        confy.getConfig(clint.get('execute'), clint.parseOverwrites())

        logfile = confy.getConfig()["smartgrazer"]["logging"]["logfile"]
        logdir = os.path.dirname(logfile)
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.NOTSET)
        smartgrazer.addHandler(fh)

        smartgrazer.info(str(clint.getArgs()))

        if confy.getConfig()["smartgrazer"]["imps"]["webber"]["cleanup"] or clint.get("cleanup"):
            webber.cleanUp()

        smithy = Smithy(confy.getConfig()["smartgrazer"]["imps"])

        # Generate the payloads and exit
        if clint.get('generate'):
            result = []

            while len(result) < confy.getConfig()["smartgrazer"]["imps"]["smithy"]["generate"]["amount"]:
                for pl in smithy.generate():
                    result.append(pl)

            for p in result:
                print(p)
            exit(0)

        responseAnalyser = ResponseAnalyser(confy.getConfig()["smartgrazer"]["imps"]["annelysa"])

        validConfig = confy.getConfig()["runconfig"]["valid"]
        attackConfig = confy.getConfig()["runconfig"]["attack"]

        # Load the instance of simpy to perform valid request and simple payloads
        simpy = smithy.getSimpy()

        # Execute valid request to know the pages' default response
        # ! only one result
        attack = Attack([])
        webber.setPayloads([attack])
        response = (webber.run(validConfig)).pop()

        responseAnalyser.setResponseObject(response).analyze()

        # Simple tests to teach smarty how to generate
        simplePayloads = simpy.generate()

        # Send simple payloads to webpage.
        webber.setPayloads(simplePayloads)
        # execute and analyze
        for response in webber.run(attackConfig):
            modifiedElements = responseAnalyser.setResponseObject(response).analyze()
            smithy.adjustElements(modifiedElements)

        # Generation phase for x amount of time
        max_time = confy.getConfig()["smartgrazer"]["imps"]["webber"]["timelimit"] * 60
        start_time = time.time()

        enabledWebdriver = clint.get("enableWebdriver")
        requestExecutor = ResponseExecutor(confy.getConfig()["smartgrazer"]["imps"]["annelysa"]["webdriver"])
        smithy = Smithy(confy.getConfig()["smartgrazer"]["imps"])
        resultpayloads = []
        tries = 0

        payloads = smithy.generate()

        while len(resultpayloads) < confy.getConfig()["smartgrazer"]["imps"]["smithy"]["generate"]["amount"] and (
                    (time.time() - start_time) < max_time):
            # Send generated payloads to webpage.
            webber.setPayloads(payloads)

            for response in webber.run(attackConfig):
                prefix = 'O '

                # execute and analyze
                modifiedElements = responseAnalyser.setResponseObject(response).analyze()

                if len(modifiedElements) < 1:
                    prefix = '== '
                    successfull = responseAnalyser.getResponse().getPayload()

                    if not enabledWebdriver:
                        resultpayloads.append(successfull)
                        prefix = '?' + prefix
                        break

                    if requestExecutor.execute(responseAnalyser.getResponse().getResponseFile()):
                        resultpayloads.append(successfull)
                        prefix = '✔ ' + prefix
                        break
                    else:
                        prefix = 'X ' + prefix
                        # Remove reflected but invalid attempt
                        response.clean()

                else:
                    prefix = prefix + '!= '
                    smithy.adjustElements(modifiedElements)
                    # Remove not working attempt
                    response.clean()

                logging.getLogger("SmartGrazer").info(prefix + str(tries) + " : " + str(response.getPayload()))
                tries = tries + 1

            payloads = smithy.generate()

        requestExecutor.close()

        if len(resultpayloads) == 0:
            print("#\t SmartGrazer: Could not find a working payload!")
            return 1

        working = ""
        if enabledWebdriver:
            working = "working "

        print("#\t SmartGrazer: Found " + str(len(resultpayloads)) + " reflected " + working + "attack(s)!")
        logging.getLogger("SmartGrazer").info(
            "#\t SmartGrazer: Found " + str(len(resultpayloads)) + " reflected " + working + "attack(s)!")
        for payload in resultpayloads:
            print("# " + str(tries) + ":\t" + str(payload))
            logging.getLogger("SmartGrazer").info("# " + str(tries) + ":\t" + str(payload))

        return 0


if __name__ == "__main__":
    sys.exit((SmartGrazer()).run())
