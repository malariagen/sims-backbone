import connexion
import six

from swagger_server.models.individual import Individual  # noqa: E501
from swagger_server.models.individuals import Individuals  # noqa: E501
from swagger_server import util

import logging


from backbone_server.controllers.individual_controller  import IndividualController


individual_controller = IndividualController()

def create_individual(individual, user = None, token_info = None):
    """
    create_individual
    Create a individual
    :param individual:
    :type individual: dict | bytes

    :rtype: Individual
    """
    if connexion.request.is_json:
        individual = Individual.from_dict(connexion.request.get_json())

    return individual_controller.create_individual(individual, user,
                                               individual_controller.token_info(token_info))


def delete_individual(individualId, user = None, token_info = None):
    """
    deletes an individual

    :param individualId: ID of individual to fetch
    :type individualId: str

    :rtype: None
    """
    return individual_controller.delete_individual(individualId, user,
                                               individual_controller.token_info(token_info))



def download_individual(individualId, user = None, token_info = None):
    """
    fetches an individual

    :param individualId: ID of individual to fetch
    :type individualId: str

    :rtype: Individual
    """
    return individual_controller.download_individual(individualId, user,
                                                 individual_controller.token_info(token_info))


def download_individuals(studyName=None, start=None, count=None, orderby=None, user = None,
                       token_info = None):
    """
    fetches individuals

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
    return individual_controller.download_individuals(studyName, start, count, orderby, user,
                                                  individual_controller.token_info(token_info))



def update_individual(individualId, individual, user = None, token_info = None):
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

    return individual_controller.update_individual(individualId, individual, user,
                                               individual_controller.token_info(token_info))

