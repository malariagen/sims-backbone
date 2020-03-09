import connexion
import six
import logging

from openapi_server.models.studies import Studies  # noqa: E501
from openapi_server import util

from backbone_server.controllers.report_controller import ReportController

report_controller = ReportController()


def missing_locations(include_country=False, studies=None, user=None, token_info=None):  # noqa: E501
    """fetches studies with sampling events with missing locations

     # noqa: E501

    :param includeCountry: include studies where only a country level location is set
    :type includeCountry: bool

    :rtype: Studies
    """
    return report_controller.missing_locations(include_country, studies=studies, user=user,
                                               auths=report_controller.token_info(token_info))


def missing_taxon(studies=None, user=None, token_info=None):  # noqa: E501
    """fetches studies with uncurated taxon

     # noqa: E501


    :rtype: Studies
    """
    return report_controller.missing_taxon(studies=studies, user=user,
                                           auths=report_controller.token_info(token_info))


def multiple_location_gps(studies=None, user=None, token_info=None):  # noqa: E501
    """fetches studies with multiple locations with the same GPS

     # noqa: E501


    :rtype: Studies
    """
    return report_controller.multiple_location_gps(studies=studies, user=user,
                                                   auths=report_controller.token_info(token_info))


def multiple_location_names(studies=None, user=None, token_info=None):  # noqa: E501
    """fetches studies with multiple locations with the same name

     # noqa: E501


    :rtype: Studies
    """
    return report_controller.multiple_location_names(studies=studies, user=user,
                                                     auths=report_controller.token_info(token_info))


def uncurated_locations(studies=None, user=None, token_info=None):  # noqa: E501
    """fetches studies with uncurated locations

     # noqa: E501


    :rtype: Studies
    """
    return report_controller.uncurated_locations(studies=studies, user=user,
                                                 auths=report_controller.token_info(token_info))
