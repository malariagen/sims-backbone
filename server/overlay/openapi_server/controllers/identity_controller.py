import connexion
import six

from openapi_server.models.groups import Groups  # noqa: E501
from openapi_server.models.people import People  # noqa: E501
from openapi_server import util

from backbone_server.controllers.identity_controller import IdentityController
import logging

identity_controller = IdentityController()

def download_groups(search_filter, start=None, count=None, user=None, token_info=None):  # noqa: E501
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
    return identity_controller.download_groups(search_filter, start, count,
                                               user,
                                               identity_controller.token_info(token_info))


def download_people(search_filter, start=None, count=None, user=None, token_info=None):  # noqa: E501
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
    return identity_controller.download_people(search_filter, start, count, user,
                                               identity_controller.token_info(token_info))
