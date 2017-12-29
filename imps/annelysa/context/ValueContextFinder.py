from imps.annelysa.AnalyzerPlugin import AnalyzerPlugin


class ValueContextFinder(AnalyzerPlugin):
    _root = None

    def __init__(self, root, tree, needle):
        self._root = root
        self._tree = tree
        self._needle = needle

    def find(self):
        results = {}

        results['namevalue'] = []
        for f in self._searchNameValue():
            results['namevalue'].append(f)

        results['value'] = []
        for f in self._searchValues():
            results['value'].append(f)

        results['sourcevalue'] = []
        for f in self._searchSourceValues():
            results['sourcevalue'].append(f)

        return results

    def _searchSourceValues(self):
        context = self._root.xpath('//*[contains(@src, "' + self._needle + '")]')

        results = []
        for elem in context:
            results.append(self._tree.getpath(elem))

        return results

    def _searchValues(self):
        context = self._root.xpath('//*[contains(@value, "' + self._needle + '")]')

        results = []
        for elem in context:
            results.append(self._tree.getpath(elem))

        return results

    def _searchNameValue(self):
        context = self._root.xpath('//*[contains(@name, "' + self._needle + '")]')

        results = []
        for elem in context:
            results.append(self._tree.getpath(elem))

        return results