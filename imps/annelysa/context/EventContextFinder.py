from imps.annelysa.AnalyzerPlugin import AnalyzerPlugin


class EventContextFinder(AnalyzerPlugin):
    def find(self):
        results = {'onclick': []}

        for f in self._searchOnClick():
            results['onclick'].append(f)

        results['onerror'] = []
        for f in self._searchOnError():
            results['onerror'].append(f)

        results['onload'] = []
        for f in self._searchOnLoad():
            results['onload'].append(f)

        return results

    def _searchOnClick(self):
        context = self._root.xpath('//*[contains(@onclick, "'+self._needle+'")]')

        results = []
        for elem in context:
            results.append(self._tree.getpath(elem))

        return results

    def _searchOnError(self):
        context = self._root.xpath('//*[contains(@onerror, "'+self._needle+'")]')

        results = []
        for elem in context:
            results.append(self._tree.getpath(elem))

        return results

    def _searchOnLoad(self):
        context = self._root.xpath('//*[contains(@onload, "'+self._needle+'")]')

        results = []
        for elem in context:
            results.append(self._tree.getpath(elem))

        return results