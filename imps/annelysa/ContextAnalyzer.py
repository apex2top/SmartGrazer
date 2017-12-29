import logging

from lxml import html

from imps.annelysa.context.EventContextFinder import EventContextFinder
from imps.annelysa.context.HtmlContextFinder import HtmlContextFinder
from imps.annelysa.context.ValueContextFinder import ValueContextFinder


class ContextAnalyzer(object):
    _logger = None
    _plugins = []

    def __init__(self):
        self._logger= logging.getLogger("SmartGrazer")
        self.file = ''
        self.needle = ''

    def _loadPlugins(self):
        root = html.fromstring(open(self.file).read())
        tree = root.getroottree()

        self._plugins.append(HtmlContextFinder(root, tree, self.needle))
        self._plugins.append(ValueContextFinder(root, tree, self.needle))
        self._plugins.append(EventContextFinder(root, tree, self.needle))

    def setFile(self, file):
        self.file = file

    def setNeedle(self, needle):
        self.needle = needle

    def search(self):
        self._loadPlugins()

        results = []

        for finder in self._plugins:
            findings = finder.find()
            for context in findings:
                if len(findings[context]) > 0:
                    results.append(context)

        return results