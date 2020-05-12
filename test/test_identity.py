import os
from datetime import date

import urllib
import pytest

import openapi_client
from openapi_client.rest import ApiException

from test_base import TestBase

class TestIdentity(TestBase):


    """
    """
    def test_get_people(self, api_factory):

        if os.getenv('TRAVIS'):
            return

        api_instance = api_factory.IdentityApi()

        try:

            people = api_instance.download_people('cn:pwmTestUser')

            print(people)

        except ApiException as error:
            self.check_api_exception(api_factory, "IdentityApi->test_get_people", error)

    """
    """
    def test_get_groups(self, api_factory):

        if os.getenv('TRAVIS'):
            return

        api_instance = api_factory.IdentityApi()

        try:

            groups = api_instance.download_groups('study:1000')

            print(groups)

        except ApiException as error:
            self.check_api_exception(api_factory, "IdentityApi->test_get_groups", error)

    """
    """
    def test_get_group_by_name(self, api_factory):

        if os.getenv('TRAVIS'):
            return

        api_instance = api_factory.IdentityApi()

        try:

            groups = api_instance.download_groups('group:websitePeople')

            print(groups)

        except ApiException as error:
            self.check_api_exception(api_factory, "IdentityApi->test_get_groups", error)

    """
    """
    def test_get_group_by_name_base(self, api_factory):

        if os.getenv('TRAVIS'):
            return

        api_instance = api_factory.IdentityApi()

        try:

            groups = api_instance.download_groups('group:coordinator;base:ou=all,ou=roma,ou=projects,ou=groups,dc=malariagen,dc=net')

            print(groups)

        except ApiException as error:
            self.check_api_exception(api_factory, "IdentityApi->test_get_groups", error)

