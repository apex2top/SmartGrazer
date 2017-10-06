import logging
import os
import shutil

from imps.smithy.elements.Element import Element
from imps.smithy.smarty.grammar.attacks.Attack import Attack
from imps.webber.sandy.Request import Request
from imps.webber.sandy.RequestExecutor import RequestExecutor as Sandy
from imps.webber.sandy.Response import Response


class PayloadTester(object):
    _sandy = None
    _payloads = []
    _logger = logging.getLogger("SmartGrazer")

    def __init__(self, sandyconfig):
        self._sandy = Sandy(sandyconfig)

    def setPayloads(self, payloads):
        self._payloads = payloads

    def _saveRunConfig(self, file, runConfig):
        renamed = file.replace(".html", ".json")
        if os.path.exists(renamed):
            os.remove(renamed)

        file = open(renamed, "w")
        file.write(str(runConfig))
        file.close()

    def cleanUp(self):
        folder = self._sandy.getFilePath()
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    def run(self, params):
        if not self._payloads:
            raise ValueError("Payload is not set!")

        if "PAYLOAD" in params.keys():
            self._logger.debug("Replacing with fixed payload! Should be a valid run!")
            element = Element("VALID")
            element.setValue(params["PAYLOAD"])
            attack = Attack([element])

            self._payloads = [attack]
            del (params["PAYLOAD"])

        responses = []

        # Create a Request for each payload
        for payload in self._payloads:
            self._logger.info("\t\t\t\tStart Request with payload: %s " % payload)
            request = Request()
            request.setPayload(payload)
            request.setRunConfig(params)

            resultHTMLFile = self._sandy.request(request) + ".html"

            response = Response()
            response.setResponseFile(resultHTMLFile)
            response.setPayload(payload)

            responses.append(response)

        return responses
