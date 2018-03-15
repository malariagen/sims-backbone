
import logging

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.report.missing_locations import MissingLocations
from backbone_server.report.missing_taxon import MissingTaxon
from backbone_server.report.uncurated_locations import UncuratedLocations

from backbone_server.errors.permission_exception import PermissionException


class ReportController(BaseController):

    def missing_locations(self, include_country, user, auths):  # noqa: E501
        """fetches studies with sampling events with missing locations

         # noqa: E501

        :param includeCountry: include studies where only a country level location is set
        :type includeCountry: bool


        :rtype: Studies
        """
        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'missing_locations', None, None, None, 403)
            return pe.message, 403

        get = MissingLocations(self.get_connection())

        retcode = 200
        country = None

        studies = get.get(include_country)

        self.log_action(user, 'missing_locations', None, None, studies, retcode)

        return studies, retcode


    def missing_taxon(self, user, auths):  # noqa: E501
        """fetches studies with uncurated taxon

         # noqa: E501


        :rtype: Studies
        """
        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'missing_taxon', None, None, None, 403)
            return pe.message, 403

        get = MissingTaxon(self.get_connection())

        retcode = 200
        country = None

        studies = get.get()

        self.log_action(user, 'missing_taxon', None, None, studies, retcode)

        return studies, retcode


    def uncurated_locations(self, user, auths):  # noqa: E501
        """fetches studies with uncurated locations

         # noqa: E501


        :rtype: Studies
        """
        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'uncurated_locations', None, None, None, 403)
            return pe.message, 403

        get = UncuratedLocations(self.get_connection())

        retcode = 200
        country = None

        studies = get.get()

        self.log_action(user, 'uncurated_locations', None, None, studies, retcode)

        return studies, retcode
