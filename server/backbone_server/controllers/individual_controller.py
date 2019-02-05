import logging

from decimal import Decimal, InvalidOperation

from backbone_server.individual.post import IndividualPost
from backbone_server.individual.put import IndividualPut
from backbone_server.individual.get import IndividualGetById
from backbone_server.individual.gets import IndividualsGet
from backbone_server.individual.delete import IndividualDelete

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class IndividualController(BaseController):

    def create_individual(self, individual, user=None, auths=None):
        """
        create_individual
        Create a individual
        :param individual:
        :type individual: dict | bytes

        :rtype: Individual
        """

        retcode = 200
        loc = None

        try:
            post = IndividualPost(self.get_connection())

            loc = post.post(individual)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_individual: {}".format(repr(dke)))
            retcode = 422

        return loc, retcode

    def delete_individual(self, individualId, user=None, auths=None):
        """
        deletes an individual

        :param individualId: ID of individual to fetch
        :type individualId: str

        :rtype: None
        """

        delete = IndividualDelete(self.get_connection())

        retcode = 200

        try:
            delete.delete(individualId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("delete_individual: {}".format(repr(dme)))
            retcode = 404

        return None, retcode

    def download_individual(self, individualId, user=None, auths=None):
        """
        fetches an individual

        :param individualId: ID of individual to fetch
        :type individualId: str

        :rtype: Individual
        """

        get = IndividualGetById(self.get_connection())

        retcode = 200
        loc = None

        try:
            loc = get.get(individualId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("download_individual: {}".format(repr(dme)))
            retcode = 404

        return loc, retcode

    def download_individuals(self, studyName=None, start=None, count=None, orderby=None, user=None,
                           auths=None):
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

        get = IndividualsGet(self.get_connection())

        retcode = 200
        loc = None

        loc = get.get(studyName, start, count, orderby)

        return loc, retcode

    def update_individual(self, individualId, individual, user=None, auths=None):
        """
        updates an individual

        :param individualId: ID of individual to update
        :type individualId: str
        :param individual:
        :type individual: dict | bytes

        :rtype: Individual
        """

        retcode = 200
        loc = None

        try:
            put = IndividualPut(self.get_connection())

            loc = put.put(individualId, individual)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("update_individual: {}".format(repr(dke)))
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("update_individual: {}".format(repr(dme)))
            retcode = 404

        return loc, retcode
