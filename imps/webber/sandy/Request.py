import copy
import datetime
import hashlib
from urllib.parse import urlparse

from imps.webber.sandy.Action import Action


class Request(object):
    _payload = "I'm no payload! I swear!"
    _runConfig = {}
    _actions = []

    def getActions(self):
        # creating precondition and action actions:
        for type in self.getRunConfig():
            print("Type: " + type)
            actionConfig = self._insertPayload(self.getRunConfig()[type])

            action = Action()

            if "filesuffix" in actionConfig:
                action.setFileSuffix(actionConfig["filesuffix"])

            action.setTarget(actionConfig["target"])

            if "post" in actionConfig["params"]:
                action.setPost(actionConfig["params"]["post"])

            if "get" in actionConfig["params"]:
                action.setGet(actionConfig["params"]["get"])

            if "cookies" in actionConfig["params"]:
                action.setCookies(actionConfig["params"]["cookies"])

            self._actions.append(action)

        return self._actions

    def _insertPayload(self, originalActionConfig):
        actionConfig = copy.deepcopy(originalActionConfig)
        for type in actionConfig['params']:
            for params in actionConfig['params'][type]:
                if actionConfig['params'][type][params] == 'PAYLOAD':
                    print("\t\t => Replacing: PAYLOAD with: " + self.getPayloadString())
                    actionConfig['params'][type][params] = self.getPayloadString()

        return actionConfig

    def setPayload(self, payload):
        self._payload = payload

    def getPayloadString(self):
        return str(self.getPayload())

    def getPayload(self):
        return self._payload

    def getRunConfig(self):
        return self._runConfig

    def setRunConfig(self, runConfig):
        self._runConfig = runConfig

    def getFilePath(self, action):
        url = urlparse(action.getTarget())
        return url.netloc + "/"

    def getFileName(self, action):
        if action.getFileSuffix():
            m = hashlib.md5()
            m.update(str(action.getParams()).encode())
            hex = m.hexdigest()[:8]
            now = datetime.datetime.now().strftime("%Y-%m-%d")

            return "{0}-{1}-{2}.{3}".format(now, hex, action.getFileSuffix(), "action")

        return None
