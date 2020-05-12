import unittest

from test_location import TestLocation
from test_metadata import TestMetadata
from test_sample import TestSample
from test_taxa import TestTaxa
from test_studies import TestStudies
from test_event_sets import TestEventSets
from test_report import TestReport
from test_individual import TestIndividual
from test_document import TestDocument
from test_identity import TestIdentity



def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestLocation))
    suite.addTest(unittest.makeSuite(TestMetadata))
    suite.addTest(unittest.makeSuite(TestSample))
    suite.addTest(unittest.makeSuite(TestTaxa))
    suite.addTest(unittest.makeSuite(TestStudies))
    suite.addTest(unittest.makeSuite(TestEventSets))
    suite.addTest(unittest.makeSuite(TestReport))
    suite.addTest(unittest.makeSuite(TestIndividual))
    suite.addTest(unittest.makeSuite(TestDocument))
    suite.addTest(unittest.makeSuite(TestIdentity))

    runner = unittest.TextTestRunner()
    print(runner.run(suite))

my_suite()
