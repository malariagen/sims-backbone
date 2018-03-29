import six
import logging

from swagger_server.models.studies import Studies  # noqa: E501
from swagger_server import util

from backbone_server.controllers.report_controller import ReportController

from local.base_local_api import BaseLocalApi

class LocalReportApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.report_controller = ReportController()

    def missing_locations(self, include_country=False):  # noqa: E501
        """fetches studies with sampling events with missing locations

         # noqa: E501

        :param includeCountry: include studies where only a country level location is set
        :type includeCountry: bool

        :rtype: Studies
        """
        (ret, retcode) = self.report_controller.missing_locations(include_country, self._user,
                                                   self.auth_tokens())

        return self.create_response(ret, retcode, 'Studies')


    def missing_taxon(self):  # noqa: E501
        """fetches studies with uncurated taxon

         # noqa: E501


        :rtype: Studies
        """
        (ret, retcode) = self.report_controller.missing_taxon(self._user,
                                                   self.auth_tokens())

        return self.create_response(ret, retcode, 'Studies')


    def uncurated_locations(self):  # noqa: E501
        """fetches studies with uncurated locations

         # noqa: E501


        :rtype: Studies
        """
        (ret, retcode) = self.report_controller.uncurated_locations(self._user,
                                                   self.auth_tokens())

        return self.create_response(ret, retcode, 'Studies')

