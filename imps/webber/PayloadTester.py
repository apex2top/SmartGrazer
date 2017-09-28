import copy
import os

from imps.annelysa import ResponseAnalyser as Annelysa
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
        renamed = save.replace(".html", ".valid.html")

        if os.path.exists(renamed):
            os.remove(renamed)

        os.rename(save, save.replace(".html", ".valid.html"))
        saves.append(renamed)

        self._saveRunConfig(renamed, params)

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

            self._saveRunConfig(save, params)

        return saves

    def _saveRunConfig(self, file, runConfig):
        renamed = file.replace(".html", ".json")
        if os.path.exists(renamed):
            os.remove(renamed)

        file = open(renamed, "w")
        file.write(str(runConfig))
        file.close()

    def run(self, valid=False):
        saves = []
        if valid is True:
            saves = self._validRun()
        else:
            saves = self._attackRun()

        return saves

    def validRun(self):
        return self.run(True)

    def _analyze(self, files):
        reports = []
        for file in files:
            self._annelysa.loadResponse(file)
            self._annelysa.loadRunConfig(file)

            reports.append(self._annelysa.analyze())
        return reports
