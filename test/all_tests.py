import unittest

from test_location import TestLocation


def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestLocation))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

my_suite()
