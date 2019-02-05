import six

from swagger_server.models.individual import Individual  # noqa: E501
from swagger_server.models.individuals import Individuals  # noqa: E501
from swagger_server import util

import logging

from local.base_local_api import BaseLocalApi

from backbone_server.controllers.individual_controller  import IndividualController

class LocalIndividualApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.individual_controller = IndividualController()

    def create_individual(self, individual):
        """
        create_individual
        Create a individual
        :param individual:
        :type individual: dict | bytes

        :rtype: Individual
        """

        (ret, retcode) = self.individual_controller.create_individual(individual, self._user,
                                                   self.auth_tokens())

        return self.create_response(ret, retcode, 'Individual')

    def delete_individual(self, individualId):
        """
        deletes an individual

        :param individualId: ID of individual to fetch
        :type individualId: str

        :rtype: None
        """
        (ret, retcode) = self.individual_controller.delete_individual(individualId, self._user,
                                                   self.auth_tokens())

        return self.create_response(ret, retcode)

    def download_individual(self, individualId):
        """
        fetches an individual

        :param individualId: ID of individual to fetch
        :type individualId: str

        :rtype: Individual
        """
        (ret, retcode) = self.individual_controller.download_individual(individualId, self._user,
                                                     self.auth_tokens())

        return self.create_response(ret, retcode, 'Individual')

    def download_individuals(self, studyName=None, start=None, count=None, orderby=None):
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
        (ret, retcode) = self.individual_controller.download_individuals(studyName, start, count, orderby, self._user,
                                                      self.auth_tokens())

        return self.create_response(ret, retcode, 'Individuals')


    def update_individual(self, individualId, individual):
        """
        updates an individual

        :param individualId: ID of individual to update
        :type individualId: str
        :param individual:
        :type individual: dict | bytes

        :rtype: Individual
        """

        (ret, retcode) = self.individual_controller.update_individual(individualId, individual, self._user,
                                                   self.auth_tokens())

        return self.create_response(ret, retcode, 'Individual')
