import logging
import urllib

from decimal import Decimal, InvalidOperation

from backbone_server.individual.post import IndividualPost
from backbone_server.individual.put import IndividualPut
from backbone_server.individual.get import IndividualGetById
from backbone_server.individual.gets import IndividualsGet
from backbone_server.individual.delete import IndividualDelete
from backbone_server.individual.merge import IndividualMerge
from backbone_server.individual.get_by_attr import IndividualGetByAttr

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.incompatible_exception import IncompatibleException

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
            logging.getLogger(__name__).debug(
                "create_individual: {}".format(repr(dke)))
            retcode = 422
            loc = str(dke)

        return loc, retcode

    def delete_individual(self, individual_id, user=None, auths=None):
        """
        deletes an individual

        :param individualId: ID of individual to fetch
        :type individualId: str

        :rtype: None
        """

        delete = IndividualDelete(self.get_connection())

        retcode = 200

        try:
            delete.delete(individual_id)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "delete_individual: {}".format(repr(dme)))
            retcode = 404

        return None, retcode

    def download_individual(self, individual_id, user=None, auths=None):
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
            loc = get.get(individual_id)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_individual: {}".format(repr(dme)))
            retcode = 404
            loc = str(dme)

        return loc, retcode

    def download_individuals(self, study_name=None, start=None, count=None, orderby=None, user=None,
                             auths=None):
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

        get = IndividualsGet(self.get_connection())

        retcode = 200
        loc = None

        loc = get.get(study_name, start, count, orderby)

        return loc, retcode

    def download_individuals_by_attr(self, prop_name, prop_value, study_name=None, user=None, auths=None):
        """
        fetches a individual by property value

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: Individual
        """

        get = IndividualGetByAttr(self.get_connection())

        retcode = 200
        samp = None

        try:
            prop_value = urllib.parse.unquote_plus(prop_value)
            samp = get.get(prop_name, prop_value, study_name)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_individual_by_attr: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def merge_individuals(self, into, merged, user=None, auths=None):  # noqa: E501
        """merges two Individuals

        merges individuals with compatible properties # noqa: E501

        :param into: id of individual
        :type into: str
        :param merged: matching value of property to search
        :type merged: str

        :rtype: Individual
        """

        retcode = 200
        samp = None

        try:
            merge = IndividualMerge(self.get_connection())

            samp = merge.merge(into, merged)
        except IncompatibleException as dke:
            logging.getLogger(__name__).debug(
                "merge_individual: {}".format(repr(dke)))
            retcode = 422
            samp = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "merge_individual: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def update_individual(self, individual_id, individual, user=None, auths=None):
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

            loc = put.put(individual_id, individual)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_individual: {}".format(repr(dke)))
            retcode = 422
            loc = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "update_individual: {}".format(repr(dme)))
            retcode = 404
            loc = str(dme)

        return loc, retcode
