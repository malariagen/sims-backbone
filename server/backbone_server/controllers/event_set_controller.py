from swagger_server.models.event_set import EventSet
from swagger_server.models.event_set_note import EventSetNote

import logging

from backbone_server.event_set.post import EventSetPost
from backbone_server.event_set.post_sampling_event import EventSetPostSamplingEvent
from backbone_server.event_set.post_note import EventSetPostNote
from backbone_server.event_set.put_note import EventSetPutNote
from backbone_server.event_set.delete_sampling_event import EventSetDeleteSamplingEvent
from backbone_server.event_set.delete_note import EventSetDeleteNote
from backbone_server.event_set.put import EventSetPut
from backbone_server.event_set.get import EventSetGetById
from backbone_server.event_set.gets import EventSetsGet
from backbone_server.event_set.delete import EventSetDelete

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException

from backbone_server.controllers.decorators  import apply_decorators

@apply_decorators
class EventSetController(BaseController):

    def create_event_set(self, eventSetId, user = None, auths = None):
        """
        creates an eventSet
        
        :param eventSetId: ID of eventSet to create
        :type eventSetId: str
        :param eventSet: 
        :type eventSet: dict | bytes

        :rtype: EventSet
        """

        retcode = 201
        evntSt = None

        try:
            post = EventSetPost(self.get_connection())

            evntSt = post.post(eventSetId)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("create_event_set: {}".format(repr(dke)))
            retcode = 422

        return evntSt, retcode


    def create_event_set_item(self, eventSetId, samplingEventId, user = None, auths = None):
        """
        Adds a samplingEvent to an eventSet
        
        :param eventSetId: ID of eventSet to modify
        :type eventSetId: str
        :param samplingEventId: ID of samplingEvent to add to the set
        :type samplingEventId: str

        :rtype: None
        """

        retcode = 201
        evntSt = None

        try:
            post = EventSetPostSamplingEvent(self.get_connection())

            evntSt = post.post(eventSetId, samplingEventId)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("create_event_set_item: {}".format(repr(dke)))
            retcode = 422
        except MissingKeyException as dke:
            logging.getLogger(__name__).error("create_event_set_item: {}".format(repr(dke)))
            retcode = 404

        return evntSt, retcode


    def create_event_set_note(self, eventSetId, noteId, note, user = None, auths = None):
        """
        Adds a note to an eventSet
        
        :param eventSetId: ID of eventSet to modify
        :type eventSetId: str
        :param noteId: ID of note to modify in the set
        :type noteId: str
        :param note: 
        :type note: dict | bytes

        :rtype: None
        """

        retcode = 201
        evntSt = None

        try:
            post = EventSetPostNote(self.get_connection())

            evntSt = post.post(eventSetId, noteId, note)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("create_event_set_note: {}".format(repr(dke)))
            retcode = 422
        except MissingKeyException as dke:
            logging.getLogger(__name__).error("create_event_set_note: {}".format(repr(dke)))
            retcode = 404

        return evntSt, retcode


    def delete_event_set(self, eventSetId, user = None, auths = None):
        """
        deletes an eventSet
        
        :param eventSetId: ID of eventSet to delete
        :type eventSetId: str

        :rtype: None
        """

        retcode = 200
        evntSt = None

        try:
            delete = EventSetDelete(self.get_connection())

            evntSt = delete.delete(eventSetId)
        except MissingKeyException as mke:
            logging.getLogger(__name__).error("delete_event_set: {}".format(repr(mke)))
            retcode = 404

        return evntSt, retcode


    def delete_event_set_item(self, eventSetId, samplingEventId, user = None, auths = None):
        """
        deletes a samplingEvent from an eventSet
        
        :param eventSetId: ID of eventSet to modify
        :type eventSetId: str
        :param samplingEventId: ID of samplingEvent to remove from the set
        :type samplingEventId: str

        :rtype: None
        """

        retcode = 200
        evntSt = None

        try:
            delete = EventSetDeleteSamplingEvent(self.get_connection())

            evntSt = delete.delete(eventSetId, samplingEventId)
        except MissingKeyException as dke:
            logging.getLogger(__name__).error("delete_event_set_item: {}".format(repr(dke)))
            retcode = 404

        return evntSt, retcode


    def delete_event_set_note(self, eventSetId, noteId, user = None, auths = None):
        """
        deletes an eventSet note
        
        :param eventSetId: ID of eventSet to modify
        :type eventSetId: str
        :param noteId: ID of note to remove from the set
        :type noteId: str

        :rtype: None
        """

        retcode = 200
        evntSt = None

        try:
            delete = EventSetDeleteNote(self.get_connection())

            evntSt = delete.delete(eventSetId, noteId)
        except MissingKeyException as dke:
            logging.getLogger(__name__).error("delete_event_set_note: {}".format(repr(dke)))
            retcode = 404

        return evntSt, retcode


    def download_event_set(self, eventSetId, start=None, count=None, user = None, auths = None):
        """
        fetches an eventSet
        
        :param eventSetId: ID of eventSet to fetch
        :type eventSetId: str

        :rtype: EventSet
        """

        retcode = 200
        evntSt = None

        try:
            get = EventSetGetById(self.get_connection())
            evntSt = get.get(eventSetId, start, count)
        except MissingKeyException as dke:
            logging.getLogger(__name__).error("download_event_set: {}".format(repr(dke)))
            retcode = 404

        return evntSt, retcode


    def download_event_sets(self, user = None, auths = None):
        """
        fetches an eventSet
        
        :rtype: EventSets
        """

        retcode = 200
        evntSts = None

        get = EventSetsGet(self.get_connection())
        evntSts = get.get()

        return evntSts, retcode


    def update_event_set(self, eventSetId, eventSet, user = None, auths = None):
        """
        updates an eventSet
        
        :param eventSetId: ID of eventSet to update
        :type eventSetId: str
        :param eventSet: 
        :type eventSet: dict | bytes

        :rtype: EventSet
        """

        retcode = 200
        evntSt = None

        try:
            put = EventSetPut(self.get_connection())
            evntSt = put.put(eventSetId, eventSet)
        except MissingKeyException as dke:
            logging.getLogger(__name__).error("update_event_set: {}".format(repr(dke)))
            retcode = 404

        return evntSt, retcode


    def update_event_set_note(self, eventSetId, noteId, note, user = None, auths = None):
        """
        Adds a note to an eventSet
        
        :param eventSetId: ID of eventSet to modify
        :type eventSetId: str
        :param noteId: ID of note to modify in the set
        :type noteId: str
        :param note: 
        :type note: dict | bytes

        :rtype: None
        """

        retcode = 200
        evnt_set = None

        try:
            put = EventSetPutNote(self.get_connection())
            evnt_set = put.put(eventSetId, noteId, note)
        except MissingKeyException as dke:
            logging.getLogger(__name__).error("update_event_set_note: {}".format(repr(dke)))
            retcode = 404
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("update_event_set_note: {}".format(repr(dke)))
            retcode = 422

        return evnt_set, retcode
