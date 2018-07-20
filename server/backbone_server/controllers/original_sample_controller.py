
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

from backbone_server.event_set.get import EventSetGetById

from swagger_server.models.original_samples import OriginalSamples

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException
from backbone_server.errors.nested_edit_exception import NestedEditException
from backbone_server.errors.incompatible_exception import IncompatibleException

from backbone_server.controllers.decorators  import apply_decorators

@apply_decorators
class OriginalSampleController(BaseController):

    def create_original_sample(self, originalSample, user = None, auths = None):
        """
        create_original_sample
        Create a originalSample
        :param originalSample: 
        :type originalSample: dict | bytes

        :rtype: OriginalSample
        """

        retcode = 201
        samp = None

        try:
            post = OriginalSamplePost(self.get_connection())

            samp = post.post(originalSample)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("create_originalSample: {}".format(repr(dke)))
            retcode = 422
        except NestedEditException as nee:
            logging.getLogger(__name__).error("create_originalSample: {}".format(repr(nee)))
            retcode = 422

        return samp, retcode


    def delete_original_sample(self, originalSampleId, user = None, auths = None):
        """
        deletes an originalSample
        
        :param originalSampleId: ID of originalSample to fetch
        :type originalSampleId: str

        :rtype: None
        """

        delete = OriginalSampleDelete(self.get_connection())

        retcode = 200
        samp = None

        try:
            delete.delete(originalSampleId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("delete_originalSample: {}".format(repr(dme)))
            retcode = 404

        return None, retcode


    def download_original_sample(self, originalSampleId, user = None, auths = None):
        """
        fetches an originalSample
        
        :param originalSampleId: ID of originalSample to fetch
        :type originalSampleId: str

        :rtype: OriginalSample
        """

        get = OriginalSampleGetById(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(originalSampleId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_originalSample: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_original_samples(self, search_filter, start, count, user = None, auths = None):
        """
        fetches originalSamples for a event_set
        
        :param event_set_id: event_set
        :type event_set_id: str

        :rtype: OriginalSamples
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
                return self.download_original_samples_by_attr(options[1],
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

    def download_original_samples_by_event_set(self, event_set_id, start, count, user = None, auths = None):
        """
        fetches originalSamples for a event_set
        
        :param event_set_id: event_set
        :type event_set_id: str

        :rtype: OriginalSamples
        """

        retcode = 200
        samp = None

        try:
            get = EventSetGetById(self.get_connection())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            evntSt = get.get(event_set_id, start, count)

            samp = evntSt.members

        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_original_samples_by_event_set: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_original_samples_by_attr(self, propName, propValue, study_name=None, user=None, auths=None):
        """
        fetches a originalSample by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: OriginalSample
        """

        get = OriginalSampleGetByAttr(self.get_connection())

        retcode = 200
        samp = None

        try:
            propValue = urllib.parse.unquote_plus(propValue)
            samp = get.get(propName, propValue, study_name)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_originalSample: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_original_samples_by_location(self, locationId, start, count, user = None, auths = None):
        """
        fetches originalSamples for a location
        
        :param locationId: location
        :type locationId: str

        :rtype: OriginalSamples
        """

        get = OriginalSamplesGetByLocation(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(locationId, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_originalSample: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_original_samples_by_study(self, studyName, start, count, user = None, auths = None):
        """
        fetches originalSamples for a study
        
        :param studyName: location
        :type studyName: str

        :rtype: OriginalSamples
        """

        get = OriginalSamplesGetByStudy(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(studyName, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_originalSample: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_original_samples_by_taxa(self, taxaId, start, count, user = None, auths = None):
        """
        fetches originalSamples for a taxa
        
        :param taxaId: taxa
        :type taxaId: str

        :rtype: OriginalSamples
        """

        get = OriginalSamplesGetByTaxa(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(taxaId, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_original_samples_by_taxa: {}".format(repr(dme)))
            retcode = 404

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
            logging.getLogger(__name__).error("merge_originalSample: {}".format(repr(dke)))
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("merge_originalSample: {}".format(repr(dme)))
            retcode = 404
        except NestedEditException as nee:
            logging.getLogger(__name__).error("merge_originalSample: {}".format(repr(nee)))
            retcode = 422

        return samp, retcode

    def update_original_sample(self, originalSampleId, originalSample, user = None, auths = None):
        """
        updates an originalSample
        
        :param originalSampleId: ID of originalSample to update
        :type originalSampleId: str
        :param originalSample: 
        :type originalSample: dict | bytes

        :rtype: OriginalSample
        """

        retcode = 200
        samp = None

        try:
            put = OriginalSamplePut(self.get_connection())

            samp = put.put(originalSampleId, originalSample)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("update_originalSample: {}".format(repr(dke)))
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_originalSample: {}".format(repr(dme)))
            retcode = 404
        except NestedEditException as nee:
            logging.getLogger(__name__).error("update_originalSample: {}".format(repr(nee)))
            retcode = 422

        return samp, retcode

