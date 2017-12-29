class AnalyzerPlugin(object):
    def __init__(self, root, tree, needle):
        self._root = root
        self._tree = tree
        self._needle = needle
