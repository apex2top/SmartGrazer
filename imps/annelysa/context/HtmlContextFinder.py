from imps.annelysa.AnalyzerPlugin import AnalyzerPlugin


class HtmlContextFinder(AnalyzerPlugin):
    _root = None

    def __init__(self, root, tree, needle):
        self._root = root
        self._tree = tree
        self._needle = needle

    def find(self):
        results = {}

        results['comments'] = []
        for f in self._searchComments():
            results['comments'].append(f)

        results['html'] = []
        for f in self._searchHtml():
            results['html'].append(f)

        return results

    def _searchHtml(self):
        htmlcon = self._root.xpath('.//*[contains(text(),"' + self._needle + '")]')

        results = []
        for elem in htmlcon:
            results.append(self._tree.getpath(elem))

        return results

    def _searchComments(self):

        htmlcommentcon = self._root.xpath('.//comment()[contains(.,"' + self._needle + '")]')

        results = []
        for elem in htmlcommentcon:
            results.append(self._tree.getpath(elem))

        return results
