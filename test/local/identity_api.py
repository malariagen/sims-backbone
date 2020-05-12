import connexion
import six

from openapi_server.models.groups import Groups  # noqa: E501
from openapi_server.models.people import People  # noqa: E501
from openapi_server import util

from backbone_server.controllers.identity_controller import IdentityController
import logging

from local.base_local_api import BaseLocalApi


class LocalIdentityApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.identity_controller = IdentityController()

    def download_groups(self, search_filter, start=None, count=None):  # noqa: E501
        """fetches groups

         # noqa: E501

        :param search_filter: search filter e.g. studyId:0000, attr:name:value,
        :type search_filter: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Groups
        """
        (ret, retcode) = self.identity_controller.download_groups(search_filter, start=start,
                                                                  count=count, user=self._user,
                                                                  auths=self.identity_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'Groups')


    def download_people(self, search_filter, start=None, count=None):  # noqa: E501
        """fetches people

         # noqa: E501

        :param search_filter: search filter e.g. studyId:0000, attr:name:value, location:locationId, taxa:taxId, eventSet:setName
        :type search_filter: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: People
        """
        (ret, retcode) = self.identity_controller.download_people(search_filter, start=start,
                                                                  count=count, user=self._user,
                                                                  auths=self.identity_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'People')
