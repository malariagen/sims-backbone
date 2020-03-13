
import logging

import urllib

from backbone_server.model.original_sample import BaseOriginalSample

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.incompatible_exception import IncompatibleException
from backbone_server.errors.permission_exception import PermissionException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class OriginalSampleController(BaseController):

    def create_original_sample(self, original_sample, uuid_val=None,
                               studies=None, user=None, auths=None):
        """
        create_original_sample
        Create a originalSample
        :param original_sample:
        :type original_sample: dict | bytes

        :rtype: OriginalSample
        """

        retcode = 201
        samp = None

        try:
            post = BaseOriginalSample(self.get_engine(), self.get_session())

            samp = post.post(original_sample, original_sample.study_name, studies, user)

        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_originalSample: %s", repr(dke))
            retcode = 422
            samp = str(dke)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("create_original_sample: %s, %s", repr(pme), user)
            retcode = 403
            samp = str(pme)

        return samp, retcode

    def delete_original_sample(self, original_sample_id, studies=None, user=None, auths=None):
        """
        deletes an originalSample

        :param original_sample_id: ID of originalSample to fetch
        :type original_sample_id: str

        :rtype: None
        """

        delete = BaseOriginalSample(self.get_engine(), self.get_session())

        retcode = 200
        resp = None

        try:
            delete.delete(original_sample_id, studies=studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("delete_originalSample: %s", repr(dme))
            retcode = 404
        except PermissionException as pme:
            logging.getLogger(__name__).debug("delete_original_sample: %s, %s", repr(pme), user)
            retcode = 403
            resp = str(pme)

        return resp, retcode

    def download_original_sample(self, original_sample_id, studies=None, user=None, auths=None):
        """
        fetches an originalSample

        :param original_sample_id: ID of originalSample to fetch
        :type original_sample_id: str

        :rtype: OriginalSample
        """

        get = BaseOriginalSample(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        try:
            samp = get.get(original_sample_id, studies=studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("download_originalSample: %s", repr(dme))
            retcode = 404
            samp = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("download_original_sample: %s, %s", repr(pme), user)
            retcode = 403
            samp = str(pme)

        return samp, retcode

    def download_original_samples(self, search_filter, value_type=None,
                                  start=None, count=None,
                                  studies=None, user=None, auths=None):
        """
        fetches originalSamples for a event_set

        :param event_set_id: event_set
        :type event_set_id: str

        :rtype: OriginalSamples
        """

        retcode = 200
        samp = None

        search_filter = urllib.parse.unquote_plus(search_filter)
        options = search_filter.split(':')
        if len(options) < 2:
            samp = 'Filter must be of the form type:arg(s)'
            retcode = 422
            return samp, retcode
        search_funcs = {
            "studyId": self.download_original_samples_by_study,
            "location": self.download_original_samples_by_location,
            "taxa": self.download_original_samples_by_taxa,
            "eventSet": self.download_original_samples_by_event_set,
        }
        func = search_funcs.get(options[0])
        if func:
            return func(options[1], start, count, studies=studies, user=user, auths=auths)
        elif options[0] == 'attr':
            study_name = None
            if len(options) > 3 and options[3]:
                study_name = options[3]
            if len(options) < 3:
                return 'attr filter must have name and value', 422
            return self.download_original_samples_by_attr(options[1],
                                                          options[2],
                                                          study_name,
                                                          value_type=value_type,
                                                          start=start,
                                                          count=count,
                                                          studies=studies, user=user,
                                                          auths=auths)
        else:
            samp = 'Invalid filter option'
            retcode = 422

        return samp, retcode

    def download_original_samples_by_event_set(self, event_set_id, start,
                                               count, studies=None, user=None, auths=None):
        """
        fetches originalSamples for a event_set

        :param event_set_id: event_set
        :type event_set_id: str

        :rtype: OriginalSamples
        """

        retcode = 200
        samp = None

        try:
            get = BaseOriginalSample(self.get_engine(), self.get_session())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            samp = get.get_by_event_set(event_set_id, studies, start, count)

        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("download_original_samples_by_event_set: %s", repr(dme))
            retcode = 404
        except PermissionException as pme:
            logging.getLogger(__name__).debug("download_original_samples_by_event_set: %s, %s", repr(pme), user)
            retcode = 403
            samp = str(pme)

        return samp, retcode

    def download_original_samples_by_attr(self, prop_name, prop_value,
                                          study_name=None,
                                          value_type=None, start=None, count=None,
                                          studies=None, user=None, auths=None):
        """
        fetches a originalSample by property value

        :param prop_name: name of property to search
        :type prop_name: str
        :param prop_value: matching value of property to search
        :type prop_value: str

        :rtype: OriginalSample
        """

        get = BaseOriginalSample(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        samp = get.get_by_attr(prop_name, prop_value, study_name, value_type,
                               start, count, studies)

        return samp, retcode

    def download_original_samples_by_location(self, location_id, start, count,
                                              studies=None, user=None, auths=None):
        """
        fetches originalSamples for a location

        :param location_id: location
        :type location_id: str

        :rtype: OriginalSamples
        """

        get = BaseOriginalSample(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        try:
            samp = get.get_by_location(location_id, studies, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("download_originalSample: %s", repr(dme))
            retcode = 404
            samp = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("download_original_samples_by_location: %s, %s", repr(pme), user)
            retcode = 403
            samp = str(pme)

        return samp, retcode

    def download_original_samples_by_study(self, study_name, start, count,
                                           studies=None, user=None, auths=None):
        """
        fetches originalSamples for a study

        :param study_name: location
        :type study_name: str

        :rtype: OriginalSamples
        """

        get = BaseOriginalSample(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        try:
            samp = get.get_by_study(study_name, start, count, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("download_originalSample: %s", repr(dme))
            retcode = 404
            samp = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("download_original_samples_by_study: %s, %s", repr(pme), user)
            retcode = 403
            samp = str(pme)

        return samp, retcode

    def download_original_samples_by_taxa(self, taxa_id, start, count,
                                          studies=None, user=None, auths=None):
        """
        fetches originalSamples for a taxa

        :param taxa_id: taxa
        :type taxa_id: str

        :rtype: OriginalSamples
        """

        get = BaseOriginalSample(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        try:
            samp = get.get_by_taxa(taxa_id, studies, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("download_original_samples_by_taxa: %s", repr(dme))
            retcode = 404
            samp = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("download_original_samples_by_taxa: %s, %s", repr(pme), user)
            retcode = 403
            samp = str(pme)

        return samp, retcode

    def merge_original_samples(self, into, merged, studies=None, user=None, auths=None):  # noqa: E501
        """merges two OriginalSamples

        merges original samples with compatible properties updating references and merging sampling events # noqa: E501

        :param into: name of property to search
        :type into: str
        :param merged: matching value of property to search
        :type merged: str

        :rtype: OriginalSample
        """

        retcode = 200
        samp = None

        try:
            merge = BaseOriginalSample(self.get_engine(), self.get_session())

            samp = merge.merge(into, merged, studies=studies)
        except IncompatibleException as dke:
            logging.getLogger(__name__).debug("merge_originalSample: %s", repr(dke))
            retcode = 422
            samp = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("merge_originalSample: %s", repr(dme))
            retcode = 404
            samp = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("merge_original_samples: %s, %s", repr(pme), user)
            retcode = 403
            samp = str(pme)

        return samp, retcode

    def update_original_sample(self, original_sample_id, original_sample,
                               studies=None, user=None, auths=None):
        """
        updates an originalSample

        :param original_sample_id: ID of originalSample to update
        :type original_sample_id: str
        :param original_sample:
        :type original_sample: dict | bytes

        :rtype: OriginalSample
        """

        retcode = 200
        samp = None

        try:
            put = BaseOriginalSample(self.get_engine(), self.get_session())

            samp = put.put(original_sample_id, original_sample,
                           original_sample.study_name,
                           studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("update_originalSample: %s", repr(dke))
            retcode = 422
            samp = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("update_originalSample: %s", repr(dme))
            retcode = 404
            samp = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("update_original_sample: %s, %s", repr(pme), user)
            retcode = 403
            samp = str(pme)

        return samp, retcode
