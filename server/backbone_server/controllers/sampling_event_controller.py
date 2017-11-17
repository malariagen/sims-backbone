
import logging

from backbone_server.sampling_event.post import SamplingEventPost
from backbone_server.sampling_event.put import SamplingEventPut
from backbone_server.sampling_event.get import SamplingEventGetById
from backbone_server.sampling_event.delete import SamplingEventDelete
from backbone_server.sampling_event.get_by_identifier import SamplingEventGetByIdentifier
from backbone_server.sampling_event.get_by_location import SamplingEventsGetByLocation
from backbone_server.sampling_event.get_by_study import SamplingEventsGetByStudy

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

class SamplingEventController(BaseController):

    def create_sampling_event(self, samplingEvent, user = None):
        """
        create_sampling_event
        Create a samplingEvent
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: SamplingEvent
        """
        retcode = 200
        samp = None

        try:
            post = SamplingEventPost(self.get_connection())

            samp = post.post(samplingEvent)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("create_samplingEvent: {}".format(repr(dke)))
            retcode = 422

        return samp, retcode


    def delete_sampling_event(self, samplingEventId, user = None):
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


    def download_sampling_event(self, samplingEventId, user = None):
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


    def download_sampling_event_by_identifier(self, propName, propValue, user = None):
        """
        fetches a samplingEvent by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: SamplingEvent
        """
        get = SamplingEventGetByIdentifier(self.get_connection())

        retcode = 200
        samp = None

        try:
            samp = get.get(propName, propValue)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_samplingEvent: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_sampling_events_by_location(self, locationId, user = None):
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
            samp = get.get(locationId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_samplingEvent: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def download_sampling_events_by_study(self, studyName, user = None):
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
            samp = get.get(studyName)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_samplingEvent: {}".format(repr(dme)))
            retcode = 404

        return samp, retcode

    def update_sampling_event(self, samplingEventId, samplingEvent, user = None):
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

        return samp, retcode

