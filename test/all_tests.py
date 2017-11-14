import unittest

from test_location import TestLocation
from test_sample import TestSample
from test_taxa import TestTaxa
from test_studies import TestStudies


def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestLocation))
    suite.addTest(unittest.makeSuite(TestSample))
    suite.addTest(unittest.makeSuite(TestTaxa))
    suite.addTest(unittest.makeSuite(TestStudies))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

my_suite()
