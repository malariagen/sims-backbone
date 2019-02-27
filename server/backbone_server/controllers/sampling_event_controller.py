
import logging

import urllib

from backbone_server.sampling_event.post import SamplingEventPost
from backbone_server.sampling_event.put import SamplingEventPut
from backbone_server.sampling_event.merge import SamplingEventMerge
from backbone_server.sampling_event.get import SamplingEventGetById
from backbone_server.sampling_event.delete import SamplingEventDelete
from backbone_server.sampling_event.get_by_attr import SamplingEventGetByAttr
from backbone_server.sampling_event.get_by_os_attr import SamplingEventGetByOsAttr
from backbone_server.sampling_event.get_by_location import SamplingEventsGetByLocation
from backbone_server.sampling_event.get_by_study import SamplingEventsGetByStudy
from backbone_server.sampling_event.get_by_taxa import SamplingEventsGetByTaxa

from backbone_server.event_set.get import EventSetGetById

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.nested_edit_exception import NestedEditException
from backbone_server.errors.incompatible_exception import IncompatibleException
from backbone_server.errors.invalid_date_exception import InvalidDateException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class SamplingEventController(BaseController):

    def create_sampling_event(self, sampling_event, user=None, auths=None):
        """
        create_sampling_event
        Create a samplingEvent
        :param sampling_event:
        :type sampling_event: dict | bytes

        :rtype: SamplingEvent
        """

        retcode = 201
        samp = None

        try:
            post = SamplingEventPost(self.get_connection())

            samp = post.post(sampling_event)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_samplingEvent: {}".format(repr(dke)))
            samp = str(dke)
            retcode = 422
        except NestedEditException as nee:
            logging.getLogger(__name__).debug(
                "create_samplingEvent: {}".format(repr(nee)))
            samp = str(nee)
            retcode = 422
        except InvalidDateException as ide:
            logging.getLogger(__name__).debug(
                "create_samplingEvent: {}".format(repr(ide)))
            samp = str(ide)
            retcode = 422

        return samp, retcode

    def delete_sampling_event(self, sampling_event_id, user=None, auths=None):
        """
        deletes an samplingEvent

        :param sampling_event_id: ID of samplingEvent to fetch
        :type sampling_event_id: str

        :rtype: None
        """

        delete = SamplingEventDelete(self.get_connection())

        retcode = 200

        try:
            delete.delete(sampling_event_id)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "delete_samplingEvent: {}".format(repr(dme)))
            retcode = 404

        return None, retcode

    def download_sampling_event(self, sampling_event_id, user=None, auths=None):
        """
        fetches an samplingEvent

        :param sampling_event_id: ID of samplingEvent to fetch
        :type sampling_event_id: str

        :rtype: SamplingEvent
        """

        get = SamplingEventGetById(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(sampling_event_id)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_samplingEvent: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def download_sampling_events(self, search_filter, start, count, user=None, auths=None):
        """
        fetches samplingEvents for a event_set

        :param event_set_id: event_set
        :type event_set_id: str

        :rtype: SamplingEvents
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
            "studyId": self.download_sampling_events_by_study,
            "location": self.download_sampling_events_by_location,
            "taxa": self.download_sampling_events_by_taxa,
            "eventSet": self.download_sampling_events_by_event_set,
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
            return self.download_sampling_events_by_attr(options[1],
                                                         options[2],
                                                         study_name,
                                                         user,
                                                         auths)
        elif options[0] == 'os_attr':
            study_name = None
            if len(options) > 3 and options[3]:
                study_name = options[3]
            if len(options) < 3:
                return 'os_attr filter must have name and value', 422
            return self.download_sampling_events_by_os_attr(options[1],
                                                            options[2],
                                                            study_name,
                                                            user,
                                                            auths)
        else:
            samp = 'Invalid filter option'
            retcode = 422

        return samp, retcode

    def download_sampling_events_by_event_set(self, event_set_id, start, count, user=None, auths=None):
        """
        fetches samplingEvents for a event_set

        :param event_set_id: event_set
        :type event_set_id: str

        :rtype: SamplingEvents
        """

        retcode = 200
        samp = None

        try:
            get = EventSetGetById(self.get_connection())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            evnt_st = get.get(event_set_id, start, count)

            samp = evnt_st.members

        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_sampling_events_by_event_set: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_sampling_events_by_attr(self, prop_name, prop_value, study_name=None, user=None, auths=None):
        """
        fetches a samplingEvent by property value

        :param prop_name: name of property to search
        :type prop_name: str
        :param prop_value: matching value of property to search
        :type prop_value: str

        :rtype: SamplingEvent
        """

        get = SamplingEventGetByAttr(self.get_connection())

        retcode = 200
        samp = None

        prop_value = urllib.parse.unquote_plus(prop_value)
        samp = get.get(prop_name, prop_value, study_name)

        return samp, retcode

    def download_sampling_events_by_os_attr(self, prop_name, prop_value, study_name=None, user=None, auths=None):
        """
        fetches a samplingEvent by property value of associated original sample

        :param prop_name: name of property to search
        :type prop_name: str
        :param prop_value: matching value of property to search
        :type prop_value: str

        :rtype: SamplingEvent
        """

        get = SamplingEventGetByOsAttr(self.get_connection())

        retcode = 200
        samp = None

        prop_value = urllib.parse.unquote_plus(prop_value)
        samp = get.get(prop_name, prop_value, study_name)

        return samp, retcode

    def download_sampling_events_by_location(self, location_id, start, count, user=None, auths=None):
        """
        fetches samplingEvents for a location

        :param location_id: location
        :type location_id: str

        :rtype: SamplingEvents
        """

        get = SamplingEventsGetByLocation(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(location_id, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_samplingEvent: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def download_sampling_events_by_study(self, study_name, start, count, user=None, auths=None):
        """
        fetches samplingEvents for a study

        :param study_name: location
        :type study_name: str

        :rtype: SamplingEvents
        """

        get = SamplingEventsGetByStudy(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(study_name, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_samplingEvent: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def download_sampling_events_by_taxa(self, taxa_id, start, count, user=None, auths=None):
        """
        fetches samplingEvents for a taxa

        :param taxa_id: taxa
        :type taxa_id: str

        :rtype: SamplingEvents
        """

        get = SamplingEventsGetByTaxa(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(taxa_id, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_sampling_events_by_taxa: {}".format(repr(dme)))
            retcode = 404
            samp = str(dme)

        return samp, retcode

    def merge_sampling_events(self, into, merged, user=None, auths=None):  # noqa: E501
        """merges two samplingEvents

        merges sampling events with compatible properties updating references # noqa: E501

        :param into: name of property to search
        :type into: str
        :param merged: matching value of property to search
        :type merged: str

        :rtype: SamplingEvent
        """
        retcode = 200
        samp = None

        try:
            merge = SamplingEventMerge(self.get_connection())

            samp = merge.merge(into, merged)
        except IncompatibleException as dke:
            logging.getLogger(__name__).debug(
                "merge_samplingEvent: {}".format(repr(dke)))
            samp = str(dke)
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "merge_samplingEvent: {}".format(repr(dme)))
            samp = str(dme)
            retcode = 404

        return samp, retcode

    def update_sampling_event(self, sampling_event_id, sampling_event, user=None, auths=None):
        """
        updates an samplingEvent

        :param sampling_event_id: ID of samplingEvent to update
        :type sampling_event_id: str
        :param sampling_event:
        :type sampling_event: dict | bytes

        :rtype: SamplingEvent
        """

        retcode = 200
        samp = None

        try:
            put = SamplingEventPut(self.get_connection())

            samp = put.put(sampling_event_id, sampling_event)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_samplingEvent: {}".format(repr(dke)))
            samp = str(dke)
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "update_samplingEvent: {}".format(repr(dme)))
            retcode = 404
        except NestedEditException as nee:
            logging.getLogger(__name__).debug(
                "update_samplingEvent: {}".format(repr(nee)))
            samp = str(nee)
            retcode = 422
        except InvalidDateException as ide:
            logging.getLogger(__name__).debug(
                "create_samplingEvent: {}".format(repr(ide)))
            samp = str(ide)
            retcode = 422

        return samp, retcode
