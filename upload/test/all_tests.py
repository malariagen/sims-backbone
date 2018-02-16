import unittest

from test_sampling_event import TestSampling_Event
from test_date import TestDate
from test_roma import TestROMA
from test_location import TestLocation
from test_country import TestCountry
from test_merge import TestMerge



def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestSampling_Event))
    suite.addTest(unittest.makeSuite(TestDate))
    suite.addTest(unittest.makeSuite(TestROMA))
    suite.addTest(unittest.makeSuite(TestLocation))
    suite.addTest(unittest.makeSuite(TestCountry))
    suite.addTest(unittest.makeSuite(TestMerge))

    runner = unittest.TextTestRunner()
    print(runner.run(suite))

my_suite()
