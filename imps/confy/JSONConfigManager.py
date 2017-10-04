import json
import os

from jsonmerge import merge


class JSONConfigManager(object):
    """
    .. todo::

        DocMe!

    """

    configfile = "config.json"
    config = {}

    def __init__(self, name=None, path=None):
        if path is None:
            path = "/../../config/"
        if name is None:
            name = self.configfile

        file = os.path.dirname(__file__) + path + name
        with open(file) as datafile:
            self.config = json.load(datafile)

    def getConfig(self, name=None, overwrites=None):
        if name is None and overwrites is None:
            return self.config

        self._merge(name)
        self._overwrite(overwrites)

        return self.config

    def _loadRunconfig(self, name):
        runConfig = JSONConfigManager(name, self.config["smartgrazer"]["directories"]["runconfigs"])
        return runConfig.getConfig()

    def _merge(self, name):
        if name is None:
            return self.config

        self.config = merge(self.config, self._loadRunconfig(name))

    def _overwrite(self, overwrites):
        self.config = merge(self.config, overwrites)
