import unittest

from core.emulator.element.filter.WordFilter import WordFilter


class WordFilterTest(unittest.TestCase):

    def runTest(self):
        self.test_single_char()
        self.test_single_word()
        self.test_multiple_word()
        self.test_single_needle()
        self.test_inherit_needle()

    def test_single_char(self):
        filter = WordFilter("a")

        result = filter.process("a")

        self.assertEqual(result, "")

    def test_single_word(self):
        filter = WordFilter("script")

        result = filter.process("script")

        self.assertEqual(result, "")

    def test_multiple_word(self):
        filter = WordFilter("script")

        result = filter.process("scriptscript")

        self.assertEqual(result, "")

    def test_single_needle(self):
        filter = WordFilter("script")

        result = filter.process("aaaascriptaaaa")

        self.assertEqual(result, "aaaaaaaa")

    def test_inherit_needle(self):
        filter = WordFilter("script")

        result = filter.process("<scriscriptpt>")

        self.assertEqual(result, "<script>")