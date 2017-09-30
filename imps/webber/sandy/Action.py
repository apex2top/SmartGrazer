class Action(object):
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
