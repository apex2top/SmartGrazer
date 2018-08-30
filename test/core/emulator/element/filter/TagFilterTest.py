import unittest

from core.emulator.element.filter.TagFilter import TagFilter


class TagFilterTest(unittest.TestCase):

    def runTest(self):
        self.test_single_opener()
        self.test_opener_and_closer()
        self.test_opener_and_closer_content()
        self.test_opener_opener_and_closer_content()
        self.test_inherit_opener()

    def test_single_opener(self):
        filter = TagFilter("script")

        result = filter.process("<script>")

        self.assertEqual(result, "")

    def test_opener_and_closer(self):
        filter = TagFilter("script")

        result = filter.process("<script></script>")

        self.assertEqual(result, "")

    def test_opener_and_closer_content(self):
        filter = TagFilter("script")

        result = filter.process("<script>aaa</script>")

        self.assertEqual(result, "aaa")

    def test_opener_opener_and_closer_content(self):
        filter = TagFilter("script")

        result = filter.process("<script><script>aaa</script>")

        self.assertEqual(result, "aaa")

    def test_inherit_opener(self):
        filter = TagFilter("script")

        result = filter.process("<scr<script>ipt>")

        self.assertEqual(result, "<script>")

    def test_inherit_closer(self):
        filter = TagFilter("script")

        result = filter.process("</scr</script>ipt>")

        self.assertEqual(result, "</script>")
