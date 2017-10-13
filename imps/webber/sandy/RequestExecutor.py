import json
import logging
import os
import urllib
from urllib.parse import urlparse

import requests


class RequestExecutor(object):
    config = {}
    session = None

    _logger = logging.getLogger("SmartGrazer")

    def __init__(self, config):
        self.config = config
        self.session = requests.Session()

    def request(self, request):
        actionFile = ''

        for action in request.getActions():
            requeststring = action.getTarget()

            if action.getGet():
                query = urllib.parse.urlencode(action.getGet())
                requeststring = '?'.join([requeststring, query])

            if action.getPost():
                r = self.session.post(requeststring, action.getPost())
                self._logger.info("POST-Request:\t" + requeststring)
                self._logger.debug("POST-Params:\t" + str(action.getParams()))
            else:
                r = self.session.get(requeststring)
                self._logger.info("GET-Request:\t" + requeststring)

            filePath = request.getFilePath(action)
            fileName = request.getFileName(action)

            if not fileName is None:
                # save the response html
                self._save(filePath, fileName + ".html", r.text)

                # save the request file
                actionFile = self._save(filePath, fileName, json.dumps(action.getParams(), indent=4))

        return actionFile

    def getFilePath(self, filePath='', fileName=''):
        dir = self.config["response"]["savedir"] + filePath

        if not os.path.exists(dir):
            os.makedirs(dir)

        return dir + fileName

    def _save(self, filePath, fileName, data):
        save = self.getFilePath(filePath, fileName)

        file = open(save, "w")
        file.write(data)
        file.close()

        return save
