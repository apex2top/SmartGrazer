class Action(object):
    """
    This class represents a single website request.

    An `imps.webber.sandy.Request.Request` can contain more than one Action,
    due the fact of dependancies of website states, like e.g. login and sessions.
    """
    _filesuffix = ""
    _target = ""
    _post = {}
    _get = {}
    _cookies = {}

    def setFileSuffix(self, suffix):
        self._filesuffix = suffix

    def getFileSuffix(self):
        return self._filesuffix

    def setTarget(self, target):
        self._target = target

    def getTarget(self):
        return self._target

    def setPost(self, post):
        self._post = post

    def getPost(self):
        return self._post

    def setGet(self, get):
        self._get = get

    def getGet(self):
        return self._get

    def setCookies(self, cookies):
        self._cookies = cookies

    def getCookies(self):
        return self._cookies

    def getParams(self):
        return {
            "target": self.getTarget(),
            "filesuffix": self.getFileSuffix(),
            "get": self.getGet(),
            "post": self.getPost(),
            "cookies": self.getPost()
        }
