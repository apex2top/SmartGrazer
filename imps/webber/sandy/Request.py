from imps.webber.sandy.Action import Action


class Request(object):
    _payload = "I'm no payload! I swear!"
    _runConfig = {}

    def prepareActions(self):
        actions = []

        # creating precondition and action actions:
        for type in self.getRunConfig():
            actionConfig = self._insertPayload(self.getRunConfig()[type])

            action = Action()

            action.setFileSuffix(actionConfig["filesuffix"])
            action.setTarget(actionConfig["target"])

            if "post" in actionConfig["params"]:
                action.setPost(actionConfig["params"]["post"])

            if "get" in actionConfig["params"]:
                action.setPost(actionConfig["params"]["get"])

            if "cookies" in actionConfig["params"]:
                action.setPost(actionConfig["params"]["cookies"])

            actions.append(action)

    def _insertPayload(self, actionConfig):
        for type in actionConfig['params']:
            for params in actionConfig['params'][type]:
                if actionConfig['params'][type][params] == 'PAYLOAD':
                    actionConfig['params'][type][params] = self.getPayload()

        return actionConfig

    def setPayload(self, payload):
        self._payload = payload

    def setRunConfig(self, runConfig):
        self._runConfig = runConfig

    def getPayload(self):
        return self._payload

    def getRunConfig(self):
        return self._runConfig

    def setResponseFile(self, file):
        config = self.getRunConfig()
        config["responseFile"] = file

    def getResponseFile(self):
        return self.getRunConfig()["responseFile"]

    def saveRequest(self):
        pass
