
from swagger_server.models.assay_datum import AssayDatum  # noqa: E501
from swagger_server.models.assay_data import AssayData  # noqa: E501
from swagger_server import util

import logging

import urllib

from backbone_server.assay_datum.post import AssayDatumPost
from backbone_server.assay_datum.put import AssayDatumPut
from backbone_server.assay_datum.get import AssayDatumGetById
from backbone_server.assay_datum.delete import AssayDatumDelete
from backbone_server.assay_datum.get_by_attr import AssayDatumGetByAttr
from backbone_server.assay_datum.get_by_os_attr import AssayDatumGetByOsAttr

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException
from backbone_server.errors.nested_edit_exception import NestedEditException
from backbone_server.errors.incompatible_exception import IncompatibleException

from backbone_server.controllers.decorators  import apply_decorators

@apply_decorators
class AssayDatumController(BaseController):


    def create_assay_datum(self, assayDatum, user=None, auths=None):  # noqa: E501
        """create_assay_datum

        Create a AssayDatum # noqa: E501

        :param assayDatum: The assay datum to create
        :type assayDatum: dict | bytes

        :rtype: AssayDatum
        """
        retcode = 201
        samp = None

        try:
            post = AssayDatumPost(self.get_connection())

            samp = post.post(assayDatum)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("create_assayDatum: {}".format(repr(dke)))
            retcode = 422
        except NestedEditException as nee:
            logging.getLogger(__name__).error("create_assayDatum: {}".format(repr(nee)))
            retcode = 422

        return samp, retcode


    def delete_assay_datum(self, assayDatumId, user=None, auths=None):  # noqa: E501
        """deletes an AssayDatum

         # noqa: E501

        :param assayDatumId: ID of AssayDatum to fetch
        :type assayDatumId: str

        :rtype: None
        """
        delete = AssayDatumDelete(self.get_connection())

        retcode = 200
        samp = None

        try:
            delete.delete(assayDatumId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("delete_assayDatum: {}".format(repr(dme)))
            retcode = 404

        return None, retcode


    def download_assay_datum(self, assayDatumId, user=None, auths=None):  # noqa: E501
        """fetches an AssayDatum

         # noqa: E501

        :param assayDatumId: ID of AssayDatum to fetch
        :type assayDatumId: str

        :rtype: AssayDatum
        """

        get = AssayDatumGetById(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(assayDatumId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_assayDatum: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode


    def download_assay_data_by_attr(self, propName, propValue, studyName=None, user=None, auths=None):  # noqa: E501
        """fetches one or more AssayDatum by property value

         # noqa: E501

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str
        :param studyName: if you want to restrict the search to a study e.g. for partner_id
        :type studyName: str

        :rtype: AssayData
        """

        get = AssayDatumGetByAttr(self.get_connection())

        retcode = 200
        samp = None

        try:
            propValue = urllib.parse.unquote_plus(propValue)
            samp = get.get(propName, propValue)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_assayDatum: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode


    def download_assay_data_by_os_attr(self, propName, propValue, studyName=None, user=None, auths=None):  # noqa: E501
        """fetches one or more assayData by property value of associated original samples

         # noqa: E501

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str
        :param studyName: if you want to restrict the search to a study e.g. for partner_id
        :type studyName: str

        :rtype: AssayData
        """

        get = AssayDatumGetByOsAttr(self.get_connection())

        retcode = 200
        samp = None

        try:
            propValue = urllib.parse.unquote_plus(propValue)
            samp = get.get(propName, propValue)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_assayDatum: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode


    def update_assay_datum(self, assayDatumId, assayDatum, user=None, auths=None):  # noqa: E501
        """updates an AssayDatum

         # noqa: E501

        :param assayDatumId: ID of AssayDatum to update
        :type assayDatumId: str
        :param assayDatum: 
        :type assayDatum: dict | bytes

        :rtype: AssayDatum
        """

        retcode = 200
        samp = None

        try:
            put = AssayDatumPut(self.get_connection())

            samp = put.put(assayDatumId, assayDatum)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("update_assayDatum: {}".format(repr(dke)))
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_assayDatum: {}".format(repr(dme)))
            retcode = 404
        except NestedEditException as nee:
            logging.getLogger(__name__).error("update_assayDatum: {}".format(repr(nee)))
            retcode = 422

        return samp, retcode
