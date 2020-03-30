import logging

import urllib

from openapi_server.models.event_set_note import EventSetNote

from backbone_server.model.event_set import BaseEventSet
from backbone_server.model.event_set_note import BaseEventSetNote
from backbone_server.model.scope import session_scope

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class EventSetController(BaseController):

    def create_event_set(self, event_set_id, studies=None, user=None, auths=None):
        """
        creates an eventSet

        :param eventSetId: ID of eventSet to create
        :type eventSetId: str
        :param eventSet:
        :type eventSet: dict | bytes

        :rtype: EventSet
        """

        retcode = 201
        evnt_st = None

        try:
            post = BaseEventSet(self.get_engine(), self.get_session())
            event_set_id = urllib.parse.unquote_plus(event_set_id)

            evnt_st = post.post(event_set_id, None, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_event_set: %s", repr(dke))
            evnt_st = str(dke)
            retcode = 422

        return evnt_st, retcode

    def create_event_set_item(self, event_set_id, sampling_event_id,
                              studies=None, user=None, auths=None):
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
            post = BaseEventSet(self.get_engine(), self.get_session())
            event_set_id = urllib.parse.unquote_plus(event_set_id)

            evnt_st = post.post_member(event_set_id, sampling_event_id, studies)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_event_set_item: %s", repr(dke))
            retcode = 422
            evnt_st = str(dke)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_event_set_item: %s", repr(dke))
            retcode = 404
            evnt_st = str(dke)

        return evnt_st, retcode

    def create_event_set_note(self, event_set_id, note_id, note, studies=None, user=None, auths=None):
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
            post = BaseEventSetNote(self.get_engine(), self.get_session())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            note_id = urllib.parse.unquote_plus(note_id)
            note.note_id = note_id
            event_set = BaseEventSet(self.get_engine(), self.get_session())
            evnt_set_id = None
            with session_scope(self.get_session()) as db:
                evnt_set_id = event_set.convert_to_id(db, event_set_id)
            evnt_st = post.post(evnt_set_id, note, None, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_event_set_note: %s", repr(dke))
            retcode = 422
            evnt_st = str(dke)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_event_set_note: %s", repr(dke))
            retcode = 404
            evnt_st = str(dke)

        return evnt_st, retcode

    def delete_event_set(self, event_set_id, studies=None, user=None, auths=None):
        """
        deletes an eventSet

        :param eventSetId: ID of eventSet to delete
        :type eventSetId: str

        :rtype: None
        """

        retcode = 200
        evnt_st = None

        try:
            delete = BaseEventSet(self.get_engine(), self.get_session())
            event_set_id = urllib.parse.unquote_plus(event_set_id)

            evnt_st = delete.delete(event_set_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "delete_event_set: %s", repr(dke))
            retcode = 404
            evnt_st = str(dke)

        return evnt_st, retcode

    def delete_event_set_item(self, event_set_id, sampling_event_id,
                              studies=None, user=None, auths=None):
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
            delete = BaseEventSet(self.get_engine(), self.get_session())
            event_set_id = urllib.parse.unquote_plus(event_set_id)

            evnt_st = delete.delete_member(event_set_id, sampling_event_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "delete_event_set_item: %s", repr(dke))
            retcode = 404
            evnt_st = str(dke)

        return evnt_st, retcode

    def delete_event_set_note(self, event_set_id, note_id, studies=None, user=None, auths=None):
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
            delete = BaseEventSetNote(self.get_engine(), self.get_session())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            note_id = urllib.parse.unquote_plus(note_id)
            event_set = BaseEventSet(self.get_engine(), self.get_session())
            evnt_set_id = None
            with session_scope(self.get_session()) as db:
                evnt_set_id = event_set.convert_to_id(db, event_set_id)

            delete.delete(evnt_set_id, note_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug("delete_event_set_note: %s", repr(dke))
            retcode = 404
            evnt_st = str(dke)

        return evnt_st, retcode

    def download_event_set(self, event_set_id, start=None,
                           count=None, studies=None, user=None, auths=None):
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
            logging.getLogger(__name__).debug("download_event_set: %s", evnt_st)
            retcode = 404
        else:
            try:
                get = BaseEventSet(self.get_engine(), self.get_session())
                event_set_id = urllib.parse.unquote_plus(event_set_id)
                evnt_st = get.get_with_members(event_set_id, studies, start, count)

            except MissingKeyException as dke:
                logging.getLogger(__name__).debug(
                    "download_event_set: %s", repr(dke))
                evnt_st = str(dke)
                retcode = 404

        return evnt_st, retcode

    def download_event_sets(self, studies=None, user=None, auths=None):
        """
        fetches an eventSet

        :rtype: EventSets
        """

        retcode = 200
        evnt_sts = None

        get = BaseEventSet(self.get_engine(), self.get_session())
        start = None
        count = None
        evnt_sts = get.gets(studies, start, count)

        return evnt_sts, retcode

    def update_event_set(self, event_set_id, event_set, studies=None, user=None, auths=None):
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
            put = BaseEventSet(self.get_engine(), self.get_session())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            evnt_st = put.put(event_set_id, event_set, None, studies, user)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_event_set: %s", repr(dke))
            retcode = 404
            evnt_st = str(dke)

        return evnt_st, retcode

    def update_event_set_note(self, event_set_id, note_id, note, studies=None, user=None, auths=None):
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
            put = BaseEventSetNote(self.get_engine(), self.get_session())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            note_id = urllib.parse.unquote_plus(note_id)
            event_set = BaseEventSet(self.get_engine(), self.get_session())
            evnt_set_id = None
            with session_scope(self.get_session()) as db:
                evnt_set_id = event_set.convert_to_id(db, event_set_id)
            evnt_set = put.put(evnt_set_id, note_id, note, studies, user)
            evnt_set = event_set.get(event_set_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_event_set_note: %s", repr(dke))
            retcode = 404
            evnt_set = str(dke)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_event_set_note: %s", repr(dke))
            retcode = 422
            evnt_set = str(dke)

        return evnt_set, retcode
