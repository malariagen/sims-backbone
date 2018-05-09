
import logging

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.report.missing_locations import MissingLocations
from backbone_server.report.missing_taxon import MissingTaxon
from backbone_server.report.uncurated_locations import UncuratedLocations
from backbone_server.report.multiple_location_names import MultipleLocationNames
from backbone_server.report.multiple_location_gps import MultipleLocationGPS

from backbone_server.errors.permission_exception import PermissionException

from backbone_server.controllers.decorators  import apply_decorators

@apply_decorators
class ReportController(BaseController):

    def missing_locations(self, include_country, user, auths):  # noqa: E501
        """fetches studies with sampling events with missing locations

         # noqa: E501

        :param includeCountry: include studies where only a country level location is set
        :type includeCountry: bool


        :rtype: Studies
        """
        get = MissingLocations(self.get_connection())

        retcode = 200
        country = None

        studies = get.get(include_country)

        return studies, retcode


    def missing_taxon(self, user, auths):  # noqa: E501
        """fetches studies with uncurated taxon

         # noqa: E501


        :rtype: Studies
        """
        get = MissingTaxon(self.get_connection())

        retcode = 200
        country = None

        studies = get.get()

        return studies, retcode

    def multiple_location_gps(self, user=None, token_info=None):  # noqa: E501
        """fetches studies with multiple locations with the same GPS

         # noqa: E501


        :rtype: Studies
        """
        get = MultipleLocationGPS(self.get_connection())

        retcode = 200
        country = None

        studies = get.get()

        return studies, retcode


    def multiple_location_names(self, user=None, token_info=None):  # noqa: E501
        """fetches studies with multiple locations with the same name

         # noqa: E501


        :rtype: Studies
        """
        get = MultipleLocationNames(self.get_connection())

        retcode = 200
        country = None

        studies = get.get()

        return studies, retcode

    def uncurated_locations(self, user, auths):  # noqa: E501
        """fetches studies with uncurated locations

         # noqa: E501


        :rtype: Studies
        """

        get = UncuratedLocations(self.get_connection())

        retcode = 200
        country = None

        studies = get.get()

        return studies, retcode
