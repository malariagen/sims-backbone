
from test_base import TestBase

import datetime
import json
import pytest

from upload_roma import Upload_ROMA

import openapi_client
from openapi_client.rest import ApiException

"""
"""
@pytest.fixture(scope="module")
def roma_03():

    el = Upload_ROMA(TestBase._config_file)
    el.use_message_buffer = True
    el.load_data_file('roma3_dump.201903.json')
    yield el.message_buffer

    locations = []

    TestBase.removeManifestItems(['MNF00004'])
    TestBase.deleteEventSets(['roma3_dump', 'MNF00004'],
                             locations)
    TestBase.deleteStudies(['3030'], locations)

    TestBase.tearDownLocations(locations)

"""
"""
#@pytest.fixture(scope="module")
#def roma_2018():
#    el = Upload_ROMA(None)
#    el.use_message_buffer = True
#    el.load_data_file('roma_dump.20180116103346.json')
#
#    yield el.message_buffer
#
#    locations = []
#    TestBase.deleteStudies(['9030','9032','9033'], locations)
#    TestBase.deleteEventSets(['roma_dump'],
#                                 TestROMADelete._locations)
