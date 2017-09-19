import json
import os


class Settings(object):
    """
    .. todo::

        DocMe!

    """
    generator_settings_file = "generator.json"
    settings = {}

    def __init__(self):
        file = os.path.dirname(__file__) + "/../../config/" + self.generator_settings_file
        with open(file) as data_file:
            self.settings = json.load(data_file)

    def getSettings(self):
        return self.settings
