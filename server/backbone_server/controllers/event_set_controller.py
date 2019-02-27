import logging

import urllib

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

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class EventSetController(BaseController):

    def create_event_set(self, event_set_id, user=None, auths=None):
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
            event_set_id = urllib.parse.unquote_plus(event_set_id)

            evntSt = post.post(event_set_id)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_event_set: {}".format(repr(dke)))
            evntSt = str(dke)
            retcode = 422

        return evntSt, retcode

    def create_event_set_item(self, event_set_id, sampling_event_id, user=None, auths=None):
        """
        Adds a samplingEvent to an eventSet

        :param eventSetId: ID of eventSet to modify
        :type eventSetId: str
        :param samplingEventId: ID of samplingEvent to add to the set
        :type samplingEventId: str

        :rtype: None
        """

        retcode = 201
        evnt_st = None

        try:
            post = EventSetPostSamplingEvent(self.get_connection())
            event_set_id = urllib.parse.unquote_plus(event_set_id)

            evnt_st = post.post(event_set_id, sampling_event_id)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_event_set_item: {}".format(repr(dke)))
            retcode = 422
            evntSt = str(dke)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_event_set_item: {}".format(repr(dke)))
            retcode = 404
            evntSt = str(dke)

        return evnt_st, retcode

    def create_event_set_note(self, event_set_id, note_id, note, user=None, auths=None):
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
        evnt_st = None

        try:
            post = EventSetPostNote(self.get_connection())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            note_id = urllib.parse.unquote_plus(note_id)

            evnt_st = post.post(event_set_id, note_id, note)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_event_set_note: {}".format(repr(dke)))
            retcode = 422
            evntSt = str(dke)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_event_set_note: {}".format(repr(dke)))
            retcode = 404
            evntSt = str(dke)

        return evnt_st, retcode

    def delete_event_set(self, event_set_id, user=None, auths=None):
        """
        deletes an eventSet

        :param eventSetId: ID of eventSet to delete
        :type eventSetId: str

        :rtype: None
        """

        retcode = 200
        evnt_st = None

        try:
            delete = EventSetDelete(self.get_connection())
            event_set_id = urllib.parse.unquote_plus(event_set_id)

            evnt_st = delete.delete(event_set_id)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "delete_event_set: {}".format(repr(dke)))
            retcode = 404
            evntSt = str(dke)

        return evnt_st, retcode

    def delete_event_set_item(self, event_set_id, sampling_event_id, user=None, auths=None):
        """
        deletes a samplingEvent from an eventSet

        :param eventSetId: ID of eventSet to modify
        :type eventSetId: str
        :param samplingEventId: ID of samplingEvent to remove from the set
        :type samplingEventId: str

        :rtype: None
        """

        retcode = 200
        evnt_st = None

        try:
            delete = EventSetDeleteSamplingEvent(self.get_connection())
            event_set_id = urllib.parse.unquote_plus(event_set_id)

            evnt_st = delete.delete(event_set_id, sampling_event_id)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "delete_event_set_item: {}".format(repr(dke)))
            retcode = 404
            evnt_st = str(dke)

        return evnt_st, retcode

    def delete_event_set_note(self, event_set_id, note_id, user=None, auths=None):
        """
        deletes an eventSet note

        :param eventSetId: ID of eventSet to modify
        :type eventSetId: str
        :param noteId: ID of note to remove from the set
        :type noteId: str

        :rtype: None
        """

        retcode = 200
        evnt_st = None

        try:
            delete = EventSetDeleteNote(self.get_connection())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            note_id = urllib.parse.unquote_plus(note_id)

            evnt_st = delete.delete(event_set_id, note_id)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "delete_event_set_note: {}".format(repr(dke)))
            retcode = 404
            evnt_st = str(dke)

        return evnt_st, retcode

    def download_event_set(self, event_set_id, start=None, count=None, user=None, auths=None):
        """
        fetches an eventSet

        :param eventSetId: ID of eventSet to fetch
        :type eventSetId: str

        :rtype: EventSet
        """

        retcode = 200
        evnt_st = None

        if not event_set_id:
            evnt_st = 'No event set specified to download'
            logging.getLogger(__name__).debug(
                "download_event_set: {}".format(evnt_st))
            retcode = 404
        else:
            try:
                get = EventSetGetById(self.get_connection())
                event_set_id = urllib.parse.unquote_plus(event_set_id)
                evnt_st = get.get(event_set_id, start, count)
            except MissingKeyException as dke:
                logging.getLogger(__name__).debug(
                    "download_event_set: {}".format(repr(dke)))
                evnt_st = str(dke)
                retcode = 404

        return evnt_st, retcode

    def download_event_sets(self, user=None, auths=None):
        """
        fetches an eventSet

        :rtype: EventSets
        """

        retcode = 200
        evnt_sts = None

        get = EventSetsGet(self.get_connection())
        evnt_sts = get.get()

        return evnt_sts, retcode

    def update_event_set(self, event_set_id, event_set, user=None, auths=None):
        """
        updates an eventSet

        :param eventSetId: ID of eventSet to update
        :type eventSetId: str
        :param eventSet:
        :type eventSet: dict | bytes

        :rtype: EventSet
        """

        retcode = 200
        evnt_st = None

        try:
            put = EventSetPut(self.get_connection())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            evnt_st = put.put(event_set_id, event_set)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_event_set: {}".format(repr(dke)))
            retcode = 404
            evnt_st = str(dke)

        return evnt_st, retcode

    def update_event_set_note(self, event_set_id, note_id, note, user=None, auths=None):
        """
        Adds a note to an eventSet

        :param event_set_id: ID of eventSet to modify
        :type event_set_id: str
        :param note_id: ID of note to modify in the set
        :type note_id: str
        :param note:
        :type note: dict | bytes

        :rtype: None
        """

        retcode = 200
        evnt_set = None

        try:
            put = EventSetPutNote(self.get_connection())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            note_id = urllib.parse.unquote_plus(note_id)
            evnt_set = put.put(event_set_id, note_id, note)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_event_set_note: {}".format(repr(dke)))
            retcode = 404
            evnt_set = str(dke)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_event_set_note: {}".format(repr(dke)))
            retcode = 422
            evnt_set = str(dke)

        return evnt_set, retcode
