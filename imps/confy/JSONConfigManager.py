import json
import os

from jsonmerge import merge


class JSONConfigManager(object):
    """
        This class stores parses, merges and stores the configuration for SmartGrazer.

        :param name: the configuration to load
        :param path: str -- An alternative path to a configuration path - e.g. config/targets/
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
        """
            This method loads the configuration if already initiated.
            Otherwise the configuration is loaded and merged.

            :param name: the configuration to load
            :param overwrites: dict -- the parameters to overwrite.

            :return: dict -- the loaded configuration
        """
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
