
from swagger_server.models.derived_sample import DerivedSample  # noqa: E501
from swagger_server.models.derived_samples import DerivedSamples  # noqa: E501
from swagger_server import util

import logging

import urllib

from backbone_server.derived_sample.post import DerivedSamplePost
from backbone_server.derived_sample.put import DerivedSamplePut
from backbone_server.derived_sample.get import DerivedSampleGetById
from backbone_server.derived_sample.delete import DerivedSampleDelete
from backbone_server.derived_sample.get_by_attr import DerivedSampleGetByAttr
from backbone_server.derived_sample.get_by_os_attr import DerivedSampleGetByOsAttr

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException
from backbone_server.errors.nested_edit_exception import NestedEditException
from backbone_server.errors.incompatible_exception import IncompatibleException

from backbone_server.controllers.decorators  import apply_decorators

@apply_decorators
class DerivedSampleController(BaseController):


    def create_derived_sample(self, derivedSample, user=None, token_info=None):  # noqa: E501
        """create_derived_sample

        Create a DerivedSample # noqa: E501

        :param derivedSample: The derived sample to create
        :type derivedSample: dict | bytes

        :rtype: DerivedSample
        """
        retcode = 201
        samp = None

        try:
            post = DerivedSamplePost(self.get_connection())

            samp = post.post(derivedSample)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("create_derivedSample: {}".format(repr(dke)))
            retcode = 422
        except NestedEditException as nee:
            logging.getLogger(__name__).error("create_derivedSample: {}".format(repr(nee)))
            retcode = 422

        return samp, retcode


    def delete_derived_sample(self, derivedSampleId, user=None, token_info=None):  # noqa: E501
        """deletes an DerivedSample

         # noqa: E501

        :param derivedSampleId: ID of DerivedSample to fetch
        :type derivedSampleId: str

        :rtype: None
        """
        delete = DerivedSampleDelete(self.get_connection())

        retcode = 200
        samp = None

        try:
            delete.delete(derivedSampleId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("delete_derivedSample: {}".format(repr(dme)))
            retcode = 404

        return None, retcode


    def download_derived_sample(self, derivedSampleId, user=None, token_info=None):  # noqa: E501
        """fetches an DerivedSample

         # noqa: E501

        :param derivedSampleId: ID of DerivedSample to fetch
        :type derivedSampleId: str

        :rtype: DerivedSample
        """

        get = DerivedSampleGetById(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(derivedSampleId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_derivedSample: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode


    def download_derived_samples_by_attr(self, propName, propValue, studyName=None, user=None, token_info=None):  # noqa: E501
        """fetches one or more DerivedSample by property value

         # noqa: E501

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str
        :param studyName: if you want to restrict the search to a study e.g. for partner_id
        :type studyName: str

        :rtype: DerivedSamples
        """

        get = DerivedSampleGetByAttr(self.get_connection())

        retcode = 200
        samp = None

        try:
            propValue = urllib.parse.unquote_plus(propValue)
            samp = get.get(propName, propValue)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_derivedSample: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode


    def download_derived_samples_by_os_attr(self, propName, propValue, studyName=None, user=None, token_info=None):  # noqa: E501
        """fetches one or more derivedSamples by property value of associated derived samples

         # noqa: E501

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str
        :param studyName: if you want to restrict the search to a study e.g. for partner_id
        :type studyName: str

        :rtype: DerivedSamples
        """

        get = DerivedSampleGetByOsAttr(self.get_connection())

        retcode = 200
        samp = None

        try:
            propValue = urllib.parse.unquote_plus(propValue)
            samp = get.get(propName, propValue)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_derivedSample: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode


    def update_derived_sample(self, derivedSampleId, derivedSample, user=None, token_info=None):  # noqa: E501
        """updates an DerivedSample

         # noqa: E501

        :param derivedSampleId: ID of DerivedSample to update
        :type derivedSampleId: str
        :param derivedSample: 
        :type derivedSample: dict | bytes

        :rtype: DerivedSample
        """

        retcode = 200
        samp = None

        try:
            put = DerivedSamplePut(self.get_connection())

            samp = put.put(derivedSampleId, derivedSample)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("update_derivedSample: {}".format(repr(dke)))
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_derivedSample: {}".format(repr(dme)))
            retcode = 404
        except NestedEditException as nee:
            logging.getLogger(__name__).error("update_derivedSample: {}".format(repr(nee)))
            retcode = 422

        return samp, retcode
