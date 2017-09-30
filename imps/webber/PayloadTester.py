import os

from imps.webber.sandy.Request import Request
from imps.webber.sandy.RequestExecutor import RequestExecutor as Sandy


class PayloadTester(object):
    _sandy = None
    _payloads = []

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

    def run(self, params):
        if not self._payloads:
            raise ValueError("Payload is not set!")

        requests = []

        if "PAYLOAD" in params.keys():
            self._payloads = [params["PAYLOAD"]]
            del (params["PAYLOAD"])

        # Create a Request for each payload
        for payload in self._payloads:
            request = Request()
            request.setPayload(payload)
            request.setRunConfig(params)
            request.prepareActions()

            # self._sandy.request(request)
            # self._saveRunConfig(save, params)
            # requests.append(request)

        return requests
