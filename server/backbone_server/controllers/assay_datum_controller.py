
import logging

import urllib

from backbone_server.model.assay_data import BaseAssayDatum

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class AssayDatumController(BaseController):

    def create_assay_datum(self, assay_datum, studies=None, user=None, auths=None):  # noqa: E501
        """create_assay_datum

        Create a AssayDatum # noqa: E501

        :param assayDatum: The assay datum to create
        :type assayDatum: dict | bytes

        :rtype: AssayDatum
        """
        retcode = 201
        samp = None

        try:
            post = BaseAssayDatum(self.get_engine(), self.get_session())
            study_name = None
            samp = post.post(assay_datum, study_name, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_assayDatum: %s", repr(dke))
            retcode = 422
            samp = str(dke)

        return samp, retcode

    def delete_assay_datum(self, assay_datum_id, studies=None, user=None, auths=None):  # noqa: E501
        """deletes an AssayDatum

         # noqa: E501

        :param assayDatumId: ID of AssayDatum to fetch
        :type assayDatumId: str

        :rtype: None
        """
        delete = BaseAssayDatum(self.get_engine(), self.get_session())

        retcode = 200

        try:
            delete.delete(assay_datum_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("delete_assayDatum: %s", repr(dme))
            retcode = 404

        return None, retcode

    def download_assay_datum(self, assay_datum_id, studies=None, user=None, auths=None):  # noqa: E501
        """fetches an AssayDatum

         # noqa: E501

        :param assayDatumId: ID of AssayDatum to fetch
        :type assayDatumId: str

        :rtype: AssayDatum
        """

        get = BaseAssayDatum(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        try:
            samp = get.get(assay_datum_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("download_assayDatum: %s", repr(dme))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def download_assay_data_by_attr(self, prop_name, prop_value, study_name=None, studies=None, user=None, auths=None):  # noqa: E501
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

        get = BaseAssayDatum(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        prop_value = urllib.parse.unquote_plus(prop_value)
        start = None
        count = None
        samp = get.get_by_attr(prop_name, prop_value, study_name, studies, start, count)

        return samp, retcode

    def download_assay_data_by_os_attr(self, prop_name, prop_value, study_name=None, studies=None, user=None, auths=None):  # noqa: E501
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

        get = BaseAssayDatum(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        prop_value = urllib.parse.unquote_plus(prop_value)
        start = None
        count = None
        samp = get.get_by_os_attr(prop_name, prop_value, study_name, studies, start, count)

        return samp, retcode

    def update_assay_datum(self, assay_datum_id, assay_datum, studies=None, user=None, auths=None):  # noqa: E501
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
            put = BaseAssayDatum(self.get_engine(), self.get_session())
            study_name = None
            samp = put.put(assay_datum_id, assay_datum, study_name, studies,
                           user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("update_assayDatum: %s", repr(dke))
            retcode = 422
            samp = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("update_assayDatum: %s", repr(dme))
            retcode = 404
            samp = str(dme)

        return samp, retcode
