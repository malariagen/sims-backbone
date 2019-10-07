
import logging

import urllib

from backbone_server.original_sample.post import OriginalSamplePost
from backbone_server.original_sample.put import OriginalSamplePut
from backbone_server.original_sample.merge import OriginalSampleMerge
from backbone_server.original_sample.get import OriginalSampleGetById
from backbone_server.original_sample.delete import OriginalSampleDelete
from backbone_server.original_sample.get_by_attr import OriginalSampleGetByAttr
from backbone_server.original_sample.get_by_location import OriginalSamplesGetByLocation
from backbone_server.original_sample.get_by_study import OriginalSamplesGetByStudy
from backbone_server.original_sample.get_by_taxa import OriginalSamplesGetByTaxa
from backbone_server.original_sample.get_by_event_set import OriginalSamplesGetByEventSet

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.incompatible_exception import IncompatibleException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class OriginalSampleController(BaseController):

    def create_original_sample(self, original_sample, uuid_val=None, user=None, auths=None):
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
            post = OriginalSamplePost(self.get_connection())

            samp = post.post(original_sample, uuid_val=uuid_val)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_originalSample: {}".format(repr(dke)))
            retcode = 422
            samp = str(dke)

        return samp, retcode

    def delete_original_sample(self, original_sample_id, user=None, auths=None):
        """
        deletes an originalSample

        :param original_sample_id: ID of originalSample to fetch
        :type original_sample_id: str

        :rtype: None
        """

        delete = OriginalSampleDelete(self.get_connection())

        retcode = 200

        try:
            delete.delete(original_sample_id)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "delete_originalSample: {}".format(repr(dme)))
            retcode = 404

        return None, retcode

    def download_original_sample(self, original_sample_id, user=None, auths=None):
        """
        fetches an originalSample

        :param original_sample_id: ID of originalSample to fetch
        :type original_sample_id: str

        :rtype: OriginalSample
        """

        get = OriginalSampleGetById(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(original_sample_id)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_originalSample: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def download_original_samples(self, search_filter, start, count, user=None, auths=None):
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
            return func(options[1], start, count, user, auths)
        elif options[0] == 'attr':
            study_name = None
            if len(options) > 3 and options[3]:
                study_name = options[3]
            if len(options) < 3:
                return 'attr filter must have name and value', 422
            return self.download_original_samples_by_attr(options[1],
                                                          options[2],
                                                          study_name,
                                                          user,
                                                          auths)
        else:
            samp = 'Invalid filter option'
            retcode = 422

        return samp, retcode

    def download_original_samples_by_event_set(self, event_set_id, start, count, user=None, auths=None):
        """
        fetches originalSamples for a event_set

        :param event_set_id: event_set
        :type event_set_id: str

        :rtype: OriginalSamples
        """

        retcode = 200
        samp = None

        try:
            get = OriginalSamplesGetByEventSet(self.get_connection())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            samp = get.get(event_set_id, start, count)

        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_original_samples_by_event_set: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_original_samples_by_attr(self, prop_name, prop_value, study_name=None, user=None, auths=None):
        """
        fetches a originalSample by property value

        :param prop_name: name of property to search
        :type prop_name: str
        :param prop_value: matching value of property to search
        :type prop_value: str

        :rtype: OriginalSample
        """

        get = OriginalSampleGetByAttr(self.get_connection())

        retcode = 200
        samp = None

        prop_value = urllib.parse.unquote_plus(prop_value)
        samp = get.get(prop_name, prop_value, study_name)

        return samp, retcode

    def download_original_samples_by_location(self, location_id, start, count, user=None, auths=None):
        """
        fetches originalSamples for a location

        :param location_id: location
        :type location_id: str

        :rtype: OriginalSamples
        """

        get = OriginalSamplesGetByLocation(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(location_id, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_originalSample: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def download_original_samples_by_study(self, study_name, start, count, user=None, auths=None):
        """
        fetches originalSamples for a study

        :param study_name: location
        :type study_name: str

        :rtype: OriginalSamples
        """

        get = OriginalSamplesGetByStudy(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(study_name, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_originalSample: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def download_original_samples_by_taxa(self, taxa_id, start, count, user=None, auths=None):
        """
        fetches originalSamples for a taxa

        :param taxa_id: taxa
        :type taxa_id: str

        :rtype: OriginalSamples
        """

        get = OriginalSamplesGetByTaxa(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(taxa_id, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_original_samples_by_taxa: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def merge_original_samples(self, into, merged, user=None, auths=None):  # noqa: E501
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
            merge = OriginalSampleMerge(self.get_connection())

            samp = merge.merge(into, merged)
        except IncompatibleException as dke:
            logging.getLogger(__name__).debug(
                "merge_originalSample: {}".format(repr(dke)))
            retcode = 422
            samp = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "merge_originalSample: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def update_original_sample(self, original_sample_id, original_sample, user=None, auths=None):
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
            put = OriginalSamplePut(self.get_connection())

            samp = put.put(original_sample_id, original_sample)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_originalSample: {}".format(repr(dke)))
            retcode = 422
            samp = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "update_originalSample: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode
