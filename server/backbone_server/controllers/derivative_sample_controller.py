
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
