
import logging

import urllib

from backbone_server.sampling_event.post import SamplingEventPost
from backbone_server.sampling_event.put import SamplingEventPut
from backbone_server.sampling_event.get import SamplingEventGetById
from backbone_server.sampling_event.delete import SamplingEventDelete
from backbone_server.sampling_event.get_by_attr import SamplingEventGetByAttr
from backbone_server.sampling_event.get_by_location import SamplingEventsGetByLocation
from backbone_server.sampling_event.get_by_study import SamplingEventsGetByStudy
from backbone_server.sampling_event.get_by_taxa import SamplingEventsGetByTaxa

from backbone_server.event_set.get import EventSetGetById

from swagger_server.models.sampling_events import SamplingEvents

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException
from backbone_server.errors.nested_edit_exception import NestedEditException

from backbone_server.controllers.decorators  import apply_decorators

@apply_decorators
class SamplingEventController(BaseController):

    def create_sampling_event(self, samplingEvent, user = None, auths = None):
        """
        create_sampling_event
        Create a samplingEvent
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: SamplingEvent
        """

        retcode = 201
        samp = None

        try:
            post = SamplingEventPost(self.get_connection())

            samp = post.post(samplingEvent)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("create_samplingEvent: {}".format(repr(dke)))
            retcode = 422
        except NestedEditException as nee:
            logging.getLogger(__name__).error("create_samplingEvent: {}".format(repr(nee)))
            retcode = 422

        return samp, retcode


    def delete_sampling_event(self, samplingEventId, user = None, auths = None):
        """
        deletes an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: None
        """

        delete = SamplingEventDelete(self.get_connection())

        retcode = 200
        samp = None

        try:
            delete.delete(samplingEventId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("delete_samplingEvent: {}".format(repr(dme)))
            retcode = 404

        return None, retcode


    def download_sampling_event(self, samplingEventId, user = None, auths = None):
        """
        fetches an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: SamplingEvent
        """

        get = SamplingEventGetById(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(samplingEventId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_samplingEvent: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_sampling_events(self, search_filter, start, count, user = None, auths = None):
        """
        fetches samplingEvents for a event_set
        
        :param event_set_id: event_set
        :type event_set_id: str

        :rtype: SamplingEvents
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
                return self.download_sampling_events_by_attr(options[1],
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

    def download_sampling_events_by_event_set(self, event_set_id, start, count, user = None, auths = None):
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
            evntSt = get.get(event_set_id, start, count)

            samp = evntSt.members

        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_sampling_events_by_event_set: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_sampling_events_by_attr(self, propName, propValue, study_name=None, user=None, auths=None):
        """
        fetches a samplingEvent by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: SamplingEvent
        """

        get = SamplingEventGetByAttr(self.get_connection())

        retcode = 200
        samp = None

        try:
            propValue = urllib.parse.unquote_plus(propValue)
            samp = get.get(propName, propValue, study_name)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_samplingEvent: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_sampling_events_by_location(self, locationId, start, count, user = None, auths = None):
        """
        fetches samplingEvents for a location
        
        :param locationId: location
        :type locationId: str

        :rtype: SamplingEvents
        """

        get = SamplingEventsGetByLocation(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(locationId, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_samplingEvent: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_sampling_events_by_study(self, studyName, start, count, user = None, auths = None):
        """
        fetches samplingEvents for a study
        
        :param studyName: location
        :type studyName: str

        :rtype: SamplingEvents
        """

        get = SamplingEventsGetByStudy(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(studyName, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_samplingEvent: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_sampling_events_by_taxa(self, taxaId, start, count, user = None, auths = None):
        """
        fetches samplingEvents for a taxa
        
        :param taxaId: taxa
        :type taxaId: str

        :rtype: SamplingEvents
        """

        get = SamplingEventsGetByTaxa(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(taxaId, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_sampling_events_by_taxa: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def update_sampling_event(self, samplingEventId, samplingEvent, user = None, auths = None):
        """
        updates an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to update
        :type samplingEventId: str
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: SamplingEvent
        """

        retcode = 200
        samp = None

        try:
            put = SamplingEventPut(self.get_connection())

            samp = put.put(samplingEventId, samplingEvent)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("update_samplingEvent: {}".format(repr(dke)))
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_samplingEvent: {}".format(repr(dme)))
            retcode = 404
        except NestedEditException as nee:
            logging.getLogger(__name__).error("create_samplingEvent: {}".format(repr(nee)))
            retcode = 422

        return samp, retcode

