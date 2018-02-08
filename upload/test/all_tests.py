import unittest

from test_sampling_event import TestSampling_Event
from test_date import TestDate
from test_roma import TestROMA



def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestSampling_Event))
    suite.addTest(unittest.makeSuite(TestDate))
    suite.addTest(unittest.makeSuite(TestROMA))

    runner = unittest.TextTestRunner()
    print(runner.run(suite))

my_suite()
