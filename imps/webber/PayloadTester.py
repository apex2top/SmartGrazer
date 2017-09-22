import copy
import os

from imps.webber.annelysa.ResponseAnalyser import ResponseAnalyser as Annelysa
from imps.webber.sandy.RequestExecutor import RequestExecutor as Sandy


class PayloadTester(object):
    _confy = None
    _sandy = None
    _annelysa = None

    _payloads = []

    def __init__(self, confy):
        self._confy = confy

        sandyconfig = self._confy.getConfig()["smartgrazer"]["imps"]["sandy"]
        annelysaconfig = self._confy.getConfig()["smartgrazer"]["imps"]["annelysa"]

        self._sandy = Sandy(sandyconfig)
        self._annelysa = Annelysa(annelysaconfig)

    def setPayloads(self, payloads):
        self._payloads = payloads

    def _validRun(self):
        saves = []
        params = self._confy.getConfig()["runconfig"]["valid"]
        save = self._sandy.request(params)
        os.rename(save, save.replace(".html", ".valid.html"))
        saves.append(save)
        return saves

    def _attackRun(self):
        if not self._payloads:
            raise ValueError("Payload is not set!")

        saves = []

        for payload in self._payloads:
            params = copy.deepcopy(self._confy.getConfig()["runconfig"]["attack"])
            for type in params["action"]['params']:
                for param in params["action"]['params'][type]:
                    if params["action"]['params'][type][param] == 'PAYLOAD':
                        params["action"]['params'][type][param] = payload

            save = self._sandy.request(params)
            saves.append(save)

        return saves

    def run(self, valid):
        saves = []
        if valid is True:
            saves = self._validRun()
        else:
            saves = self._attackRun()

        self._analyze(saves)

    def _analyze(self, file):
        self._annelysa.loadResponse(file)
        self._annelysa.analyze()
