import unittest
from unittest import TestLoader
from TestCurrencyClientNegative import TestCurrencyClientNegative
from TestCurrencyClientPositive import TestCurrencyClientPositive


class TestRunner:

    @staticmethod
    def suite():
        suite = unittest.TestSuite()
        loader = TestLoader()
        suite.addTests(loader.loadTestsFromTestCase(TestCurrencyClientNegative))
        suite.addTests(loader.loadTestsFromTestCase(TestCurrencyClientPositive))
        return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(TestRunner.suite())
