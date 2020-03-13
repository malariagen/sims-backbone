import six

from openapi_server.models.individual import Individual  # noqa: E501
from openapi_server.models.individuals import Individuals  # noqa: E501
from openapi_server import util

import logging

from local.base_local_api import BaseLocalApi

from backbone_server.controllers.individual_controller import IndividualController


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

        (ret, retcode) = self.individual_controller.create_individual(individual, user=self._user,
                                                                      auths=self.individual_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Individual')

    def delete_individual(self, individual_id):
        """
        deletes an individual

        :param individual_id: ID of individual to fetch
        :type individual_id: str

        :rtype: None
        """
        (ret, retcode) = self.individual_controller.delete_individual(individual_id, user=self._user,
                                                                      auths=self.individual_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def download_individual(self, individual_id):
        """
        fetches an individual

        :param individualId: ID of individual to fetch
        :type individualId: str

        :rtype: Individual
        """
        (ret, retcode) = self.individual_controller.download_individual(individual_id, user=self._user,
                                                                        auths=self.individual_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Individual')

    def download_individuals(self, search_filter, study_name=None,
                             studies=None, start=None, count=None, orderby=None):
        """
        fetches individuals

        :param study_name: restrict to a particular study
        :type study_name: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int
        :param orderby: how to order the result set
        :type orderby: str

        :rtype: Individuals
        """
        (ret, retcode) = self.individual_controller.download_individuals(search_filter,
                                                                         study_name,
                                                                         studies=studies,
                                                                         start=start,
                                                                         count=count, orderby=orderby, user=self._user,
                                                                         auths=self.individual_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Individuals')

    def download_individuals_by_attr(self, attr_name, attr_value,
                                     study_name=None, value_type=None,
                                     start=None, count=None):
        """
        fetches individuals

        :param study_name: restrict to a particular study
        :type study_name: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int
        :param orderby: how to order the result set
        :type orderby: str

        :rtype: Individuals
        """
        (ret, retcode) = self.individual_controller.download_individuals_by_attr(attr_name,
                                                                                 attr_value,
                                                                                 study_name,
                                                                                 value_type=value_type,
                                                                                 start=start,
                                                                                 count=count,
                                                                                 user=self._user,
                                                                                 auths=self.individual_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Individuals')

    def merge_individuals(self, individual1, individual2):

        (ret, retcode) = self.individual_controller.merge_individuals(individual1, individual2, user=self._user,
                                                                      auths=self.individual_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Individual')

    def update_individual(self, individual_id, individual):
        """
        updates an individual

        :param individual_id: ID of individual to update
        :type individual_id: str
        :param individual:
        :type individual: dict | bytes

        :rtype: Individual
        """

        (ret, retcode) = self.individual_controller.update_individual(individual_id, individual, user=self._user,
                                                                      auths=self.individual_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Individual')
