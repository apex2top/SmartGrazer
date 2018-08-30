import unittest

from test.core.emulator.element.filter.TagFilterTest import TagFilterTest
from test.core.emulator.element.filter.WordFilterTest import WordFilterTest


def suite():
    suite = unittest.TestSuite()

    suite.addTest(TagFilterTest())
    suite.addTest(WordFilterTest())

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
