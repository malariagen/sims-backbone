from __future__ import print_function
import openapi_client
import json
import requests
import os

import sys
import pytest


class TestBase():

    def check_api_exception(self, api_factory, called, error):
        message = ("{}:"
                   "Exception when calling"
                   "{}: {}").format(
                       sys._getframe(1).f_code.co_name,
                       called,
                       error)
        if api_factory.is_authorized(None):
            pytest.fail(message)
        else:
            if not (error.status == 403 or error.status == 401):
                pytest.fail(message)

    def compare_attrs(self, obj1, obj2):
        """ Because attrs are not necessarily returned in the same order"""

        if (not obj1.attrs and obj2.attrs) or (obj1.attrs and not obj2.attrs):
            assert obj1 == obj2

        assert len(obj1.attrs) == len(obj2.attrs)

        for attr1 in obj1.attrs:
            found = False
            for attr2 in obj2.attrs:
                if attr1 == attr2:
                    found = True
            if not found:
                assert obj1 == obj2
        obj1.attrs = None
        obj2.attrs = None
