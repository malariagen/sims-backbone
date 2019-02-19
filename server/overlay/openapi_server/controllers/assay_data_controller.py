import connexion
import six

from openapi_server.models.assay_datum import AssayDatum  # noqa: E501
from openapi_server.models.assay_data import AssayData  # noqa: E501
from openapi_server import util

import logging

from backbone_server.controllers.assay_datum_controller  import AssayDatumController

assay_datum_controller = AssayDatumController()

def create_assay_datum(assayDatum, user=None, token_info=None):  # noqa: E501
    """create_assay_datum

    Create a AssayDatum # noqa: E501

    :param assayDatum: The original sample to create
    :type assayDatum: dict | bytes

    :rtype: AssayDatum
    """
    if connexion.request.is_json:
        assayDatum = AssayDatum.from_dict(connexion.request.get_json())  # noqa: E501
    return assay_datum_controller.create_assay_datum(assayDatum, user,
                                                           assay_datum_controller.token_info(token_info))


def delete_assay_datum(assayDatumId, user=None, token_info=None):  # noqa: E501
    """deletes an AssayDatum

     # noqa: E501

    :param assayDatumId: ID of AssayDatum to fetch
    :type assayDatumId: str

    :rtype: None
    """
    return assay_datum_controller.delete_assay_datum(assayDatumId, user,
                                                           assay_datum_controller.token_info(token_info))


def download_assay_datum(assayDatumId, user=None, token_info=None):  # noqa: E501
    """fetches an AssayDatum

     # noqa: E501

    :param assayDatumId: ID of AssayDatum to fetch
    :type assayDatumId: str

    :rtype: AssayDatum
    """
    return assay_datum_controller.download_assay_datum(assayDatumId, user,
                                                           assay_datum_controller.token_info(token_info))


def download_assay_data_by_attr(propName, propValue, studyName=None, user=None, token_info=None):  # noqa: E501
    """fetches one or more AssayDatum by property value

     # noqa: E501

    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str
    :param studyName: if you want to restrict the search to a study e.g. for partner_id
    :type studyName: str

    :rtype: AssayData
    """
    return assay_datum_controller.download_assay_data_by_attr(propName, propValue, studyName, user,
                                                           assay_datum_controller.token_info(token_info))


def download_assay_data_by_os_attr(propName, propValue, studyName=None, user=None, token_info=None):  # noqa: E501
    """fetches one or more assayData by property value of associated original samples

     # noqa: E501

    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str
    :param studyName: if you want to restrict the search to a study e.g. for partner_id
    :type studyName: str

    :rtype: AssayData
    """
    return assay_datum_controller.download_assay_data_by_os_attr(propName, propValue, studyName, user,
                                                           assay_datum_controller.token_info(token_info))


def update_assay_datum(assayDatumId, assayDatum, user=None, token_info=None):  # noqa: E501
    """updates an AssayDatum

     # noqa: E501

    :param assayDatumId: ID of AssayDatum to update
    :type assayDatumId: str
    :param assayDatum: 
    :type assayDatum: dict | bytes

    :rtype: AssayDatum
    """
    if connexion.request.is_json:
        assayDatum = AssayDatum.from_dict(connexion.request.get_json())  # noqa: E501
    return assay_datum_controller.update_assay_datum(assayDatumId, assayDatum, user,
                                                           assay_datum_controller.token_info(token_info))
