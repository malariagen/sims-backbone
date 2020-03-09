import logging
import urllib

from decimal import Decimal, InvalidOperation

from backbone_server.model.individual import BaseIndividual

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.permission_exception import PermissionException
from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.incompatible_exception import IncompatibleException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class IndividualController(BaseController):

    def create_individual(self, individual, studies=None, user=None, auths=None):
        """
        create_individual
        Create a individual
        :param individual:
        :type individual: dict | bytes

        :rtype: Individual
        """

        retcode = 200
        indiv = None

        try:
            post = BaseIndividual(self.get_engine(), self.get_session())

            indiv = post.post(individual, None, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_individual: %s", repr(dke))
            retcode = 422
            indiv = str(dke)

        return indiv, retcode

    def delete_individual(self, individual_id, studies=None, user=None, auths=None):
        """
        deletes an individual

        :param individualId: ID of individual to fetch
        :type individualId: str

        :rtype: None
        """

        delete = BaseIndividual(self.get_engine(), self.get_session())

        retcode = 200

        try:
            delete.delete(individual_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("delete_individual: %s", repr(dme))
            retcode = 404

        return None, retcode

    def download_individual(self, individual_id, studies=None, user=None, auths=None):
        """
        fetches an individual

        :param individualId: ID of individual to fetch
        :type individualId: str

        :rtype: Individual
        """

        get = BaseIndividual(self.get_engine(), self.get_session())

        retcode = 200
        loc = None

        try:
            loc = get.get(individual_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("download_individual: %s", repr(dme))
            retcode = 404
            loc = str(dme)

        return loc, retcode

    def download_individuals_by_study(self, study_name=None,
                                      start=None, count=None, orderby=None,
                                      studies=None, user=None,
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

        get = BaseIndividual(self.get_engine(), self.get_session())

        retcode = 200
        loc = None

        try:
            loc = get.get_by_study(study_name, start=start, count=count,
                                   studies=studies)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("download_individuals_by_study: %s", repr(pme))
            retcode = 403

        return loc, retcode

    def download_individuals(self, search_filter, study_name=None,
                             studies=None, start=None, count=None, orderby=None, user=None,
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

        indiv = None
        retcode = 200

        search_filter = urllib.parse.unquote_plus(search_filter)
        options = search_filter.split(':')
        if len(options) < 2:
            samp = 'Filter must be of the form type:arg(s)'
            retcode = 422
            return samp, retcode
        search_funcs = {
            "studyId": self.download_individuals_by_study
        }
        func = search_funcs.get(options[0])
        if func:
            return func(options[1], studies=studies, start=start, count=count,
                        orderby=orderby, user=user, auths=auths)
        elif options[0] == 'attr':
            return self.download_individuals_by_attr(options[1],
                                                     options[2],
                                                     study_name,
                                                     studies,
                                                     user,
                                                     auths)
        else:
            indiv = 'Invalid filter option'
            retcode = 422

        return indiv, retcode

    def download_individuals_by_attr(self, prop_name, prop_value,
                                     study_name=None, studies=None, user=None, auths=None):
        """
        fetches a individual by property value

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: Individual
        """

        get = BaseIndividual(self.get_engine(), self.get_session())

        retcode = 200
        samp = None
        start = None
        count = None
        prop_value = urllib.parse.unquote_plus(prop_value)
        samp = get.get_by_attr(prop_name, prop_value, study_name, studies,
                               start, count)

        return samp, retcode

    def merge_individuals(self, into, merged, studies=None, user=None, auths=None):  # noqa: E501
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
            merge = BaseIndividual(self.get_engine(), self.get_session())

            samp = merge.merge(into, merged, studies)
        except IncompatibleException as dke:
            logging.getLogger(__name__).debug("merge_individual: %s", repr(dke))
            retcode = 422
            samp = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("merge_individual: %s", repr(dme))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def update_individual(self, individual_id, individual, studies=None, user=None, auths=None):
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
            put = BaseIndividual(self.get_engine(), self.get_session())

            loc = put.put(individual_id, individual, None, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("update_individual: %s", repr(dke))
            retcode = 422
            loc = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("update_individual: %s", repr(dme))
            retcode = 404
            loc = str(dme)

        return loc, retcode
