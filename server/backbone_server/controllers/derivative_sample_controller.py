
from swagger_server.models.derivative_sample import DerivativeSample  # noqa: E501
from swagger_server.models.derivative_samples import DerivativeSamples  # noqa: E501
from swagger_server import util

import logging

import urllib

from backbone_server.derivative_sample.post import DerivativeSamplePost
from backbone_server.derivative_sample.put import DerivativeSamplePut
from backbone_server.derivative_sample.get import DerivativeSampleGetById
from backbone_server.derivative_sample.delete import DerivativeSampleDelete
from backbone_server.derivative_sample.get_by_attr import DerivativeSampleGetByAttr
from backbone_server.derivative_sample.get_by_taxa import DerivativeSampleGetByTaxa
from backbone_server.derivative_sample.get_by_os_attr import DerivativeSampleGetByOsAttr

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException
from backbone_server.errors.nested_edit_exception import NestedEditException
from backbone_server.errors.incompatible_exception import IncompatibleException

from backbone_server.controllers.decorators  import apply_decorators

@apply_decorators
class DerivativeSampleController(BaseController):


    def create_derivative_sample(self, derivativeSample, user=None, auths=None):  # noqa: E501
        """create_derivative_sample

        Create a DerivativeSample # noqa: E501

        :param derivativeSample: The derivative sample to create
        :type derivativeSample: dict | bytes

        :rtype: DerivativeSample
        """
        retcode = 201
        samp = None

        try:
            post = DerivativeSamplePost(self.get_connection())

            samp = post.post(derivativeSample)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("create_derivativeSample: {}".format(repr(dke)))
            retcode = 422
        except NestedEditException as nee:
            logging.getLogger(__name__).error("create_derivativeSample: {}".format(repr(nee)))
            retcode = 422

        return samp, retcode


    def delete_derivative_sample(self, derivativeSampleId, user=None, auths=None):  # noqa: E501
        """deletes an DerivativeSample

         # noqa: E501

        :param derivativeSampleId: ID of DerivativeSample to fetch
        :type derivativeSampleId: str

        :rtype: None
        """
        delete = DerivativeSampleDelete(self.get_connection())

        retcode = 200
        samp = None

        try:
            delete.delete(derivativeSampleId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("delete_derivativeSample: {}".format(repr(dme)))
            retcode = 404

        return None, retcode


    def download_derivative_sample(self, derivativeSampleId, user=None, auths=None):  # noqa: E501
        """fetches an DerivativeSample

         # noqa: E501

        :param derivativeSampleId: ID of DerivativeSample to fetch
        :type derivativeSampleId: str

        :rtype: DerivativeSample
        """

        get = DerivativeSampleGetById(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(derivativeSampleId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_derivativeSample: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode


    def download_derivative_samples(self, search_filter, start, count, user = None, auths = None):
        """
        fetches derivativeSamples for a event_set
        
        :param event_set_id: event_set
        :type event_set_id: str

        :rtype: DerivativeSamples
        """

        retcode = 200
        samp = None

        if search_filter:
            search_filter = urllib.parse.unquote_plus(search_filter)
            options = search_filter.split(':')
            if len(options) < 2:
                samp = 'Filter must be of the form type:arg(s)'
                retcode = 422
                return samp, retcode
            search_funcs = {
                "taxa": self.download_derivative_samples_by_taxa,
            }
            func = search_funcs.get(options[0])
            if func:
                return func(options[1], start, count, user, auths)
            elif options[0] == 'attr':
                study_name = None
                if len(options) > 3 and options[3]:
                    study_name = options[3]
                return self.download_derivative_samples_by_attr(options[1],
                                                             options[2],
                                                             study_name,
                                                             user,
                                                             auths)
            else:
                samp = 'Invalid filter option'
                retcode = 422
        else:
            samp = 'filter is required'
            retcode = 422

        return samp, retcode

    def download_derivative_samples_by_attr(self, propName, propValue, studyName=None, user=None, auths=None):  # noqa: E501
        """fetches one or more DerivativeSample by property value

         # noqa: E501

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str
        :param studyName: if you want to restrict the search to a study e.g. for partner_id
        :type studyName: str

        :rtype: DerivativeSamples
        """

        get = DerivativeSampleGetByAttr(self.get_connection())

        retcode = 200
        samp = None

        try:
            propValue = urllib.parse.unquote_plus(propValue)
            samp = get.get(propName, propValue)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_derivativeSample: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode


    def download_derivative_samples_by_os_attr(self, propName, propValue, studyName=None, user=None, auths=None):  # noqa: E501
        """fetches one or more derivativeSamples by property value of associated derivative samples

         # noqa: E501

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str
        :param studyName: if you want to restrict the search to a study e.g. for partner_id
        :type studyName: str

        :rtype: DerivativeSamples
        """

        get = DerivativeSampleGetByOsAttr(self.get_connection())

        retcode = 200
        samp = None

        try:
            propValue = urllib.parse.unquote_plus(propValue)
            samp = get.get(propName, propValue)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_derivativeSample: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode


    def download_derivative_samples_by_taxa(self, taxaId, start, count, user = None, auths = None):
        """
        fetches derivativeSamples for a taxa
        
        :param taxaId: taxa
        :type taxaId: str

        :rtype: DerivativeSamples
        """

        get = DerivativeSampleGetByTaxa(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(taxaId, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_derivative_samples_by_taxa: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode


    def update_derivative_sample(self, derivativeSampleId, derivativeSample, user=None, auths=None):  # noqa: E501
        """updates an DerivativeSample

         # noqa: E501

        :param derivativeSampleId: ID of DerivativeSample to update
        :type derivativeSampleId: str
        :param derivativeSample: 
        :type derivativeSample: dict | bytes

        :rtype: DerivativeSample
        """

        retcode = 200
        samp = None

        try:
            put = DerivativeSamplePut(self.get_connection())

            samp = put.put(derivativeSampleId, derivativeSample)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("update_derivativeSample: {}".format(repr(dke)))
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_derivativeSample: {}".format(repr(dme)))
            retcode = 404
        except NestedEditException as nee:
            logging.getLogger(__name__).error("update_derivativeSample: {}".format(repr(nee)))
            retcode = 422

        return samp, retcode
