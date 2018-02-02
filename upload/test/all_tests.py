import unittest

from test_sampling_event import TestSampling_Event



def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestSampling_Event))

    runner = unittest.TextTestRunner()
    print(runner.run(suite))

my_suite()
