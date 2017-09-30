import datetime
import hashlib
import os
import urllib
from urllib.parse import urlparse

import requests


class RequestExecutor(object):
    config = {}
    response = ''
    session = None
    action = ""
    skipPreCondition = False

    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.skipPreCondition = False

    def request(self, runconfig):
        if runconfig["precondition"] and not self.skipPreCondition:
            self._request(runconfig["precondition"])

        file = self._request(runconfig["action"])
        self._saveResponse(file)

        return file

    def _request(self, runconfig):
        params = runconfig["params"]

        if not "get" in params:
            params['get'] = {}

        if not "post" in params:
            params['post'] = {}

        if not "cookies" in params:
            params['cookies'] = {}

        requeststring = runconfig["target"]

        if params['get']:
            query = urllib.parse.urlencode(params['get'])

            requeststring = '?'.join([runconfig["target"], query])

        if params['post']:
            r = self.session.post(requeststring, params['post'])
        else:
            r = self.session.get(requeststring)

        self.response = r.text
        return self._getFilePath(runconfig)

    def _getFilePath(self, params):
        m = hashlib.md5()
        m.update(str(params).encode())
        hex = m.hexdigest()[:8]
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        url = urlparse(params["target"])

        dir = self.config["response"]["savedir"] + url.netloc + "/"

        if not os.path.exists(dir):
            os.makedirs(dir)

        return dir + now + " - " + hex + "." + params["filesuffix"] + ".html"

    def _saveResponse(self, save):
        file = open(save, "w")
        file.write(self.response)
        file.close()
