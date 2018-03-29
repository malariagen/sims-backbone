from __future__ import print_function
import swagger_client
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

