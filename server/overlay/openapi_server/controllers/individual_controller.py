import connexion
import six

from openapi_server.models.individual import Individual  # noqa: E501
from openapi_server.models.individuals import Individuals  # noqa: E501
from openapi_server import util

import logging


from backbone_server.controllers.individual_controller import IndividualController


individual_controller = IndividualController()


def create_individual(body, user=None, token_info=None):
    """
    create_individual
    Create a individual
    :param individual:
    :type individual: dict | bytes

    :rtype: Individual
    """
    if connexion.request.is_json:
        individual = Individual.from_dict(connexion.request.get_json())

    return individual_controller.create_individual(individual, studies=None,
                                                   user=user,
                                                   auths=individual_controller.token_info(token_info))


def delete_individual(individual_id, user=None, token_info=None):
    """
    deletes an individual

    :param individualId: ID of individual to fetch
    :type individualId: str

    :rtype: None
    """
    return individual_controller.delete_individual(individual_id, studies=None, user=user,
                                                   auths=individual_controller.token_info(token_info))


def download_individual(individual_id, user=None, token_info=None):
    """
    fetches an individual

    :param individualId: ID of individual to fetch
    :type individualId: str

    :rtype: Individual
    """
    return individual_controller.download_individual(individual_id,
                                                     studies=None, user=user,
                                                     auths=individual_controller.token_info(token_info))


def download_individuals(search_filter,
                         study_name=None,
                         start=None,
                         count=None,
                         orderby=None,
                         user=None,
                         token_info=None):  # noqa: E501
    """fetches individuals

     # noqa: E501

    :param studyName: restrict to a particular study
    :type studyName: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int
    :param orderby: how to order the result set
    :type orderby: str

    :rtype: Individuals
    """
    return individual_controller.download_individuals(search_filter,
                                                      study_name=study_name, start=start,
                                                      count=count,
                                                      orderby=orderby, studies=None, user=user,
                                                      auths=individual_controller.token_info(token_info))


def download_individuals_by_attr(prop_name, prop_value, study_name=None, user=None, token_info=None):  # noqa: E501
    """fetches one or more individuals by property value

     # noqa: E501

    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str
    :param studyName: if you want to restrict the search to a study e.g. for patient_id
    :type studyName: str

    :rtype: Individuals
    """
    return individual_controller.download_individuals_by_attr(prop_name,
                                                              prop_value,
                                                              study_name,
                                                              studies=None, user=user,
                                                              auths=individual_controller.token_info(token_info))


def merge_individuals(into, merged, user=None, token_info=None):
    """merges two Individuals

    merges individuals # noqa: E501

    :param into: name of property to search
    :type into: str
    :param merged: matching value of property to search
    :type merged: str

    :rtype: Individual
    """
    return individual_controller.merge_individuals(into, merged, studies=None, user=user,
                                                   auths=individual_controller.token_info(token_info))


def update_individual(individual_id, body, user=None, token_info=None):
    """
    updates an individual

    :param individualId: ID of individual to update
    :type individualId: str
    :param individual:
    :type individual: dict | bytes

    :rtype: Individual
    """
    if connexion.request.is_json:
        individual = Individual.from_dict(connexion.request.get_json())

    return individual_controller.update_individual(individual_id, individual,
                                                   studies=None, user=user,
                                                   auths=individual_controller.token_info(token_info))
