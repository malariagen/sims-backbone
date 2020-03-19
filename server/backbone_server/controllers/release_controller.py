import urllib
import logging

from openapi_server.models.release import Release  # noqa: E501
from openapi_server.models.release_item import ReleaseItem  # noqa: E501
from openapi_server.models.release_note import ReleaseNote  # noqa: E501
from openapi_server.models.releases import Releases  # noqa: E501
from openapi_server import util

from backbone_server.controllers.base_controller import BaseController

from backbone_server.model.scope import session_scope

from backbone_server.model.release import BaseRelease, BaseReleaseItem
from backbone_server.model.release_note import BaseReleaseNote

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.controllers.decorators import apply_decorators

@apply_decorators
class ReleaseController(BaseController):

    def create_release(self, release_id, studies=None, user=None, auths=None):  # noqa: E501
        """creates an release

         # noqa: E501

        :param release_id: ID of release to create
        :type release_id: str

        :rtype: Release
        """
        retcode = 201
        rel = None

        try:
            post = BaseRelease(self.get_engine(), self.get_session())
            release_id = urllib.parse.unquote_plus(release_id)

            rel = post.post(release_id, None, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_release: %s", repr(dke))
            rel = str(dke)
            retcode = 422

        return rel, retcode


    def create_release_item(self, release_id, original_sample_id, studies=None, user=None, auths=None):  # noqa: E501
        """Adds an item  to a release

         # noqa: E501

        :param release_id: ID of release to modify
        :type release_id: str
        :param release_item:
        :type release_item: dict | bytes

        :rtype: None
        """

        retcode = 201
        rel_item = None

        try:
            post = BaseRelease(self.get_engine(), self.get_session())
            release_id = urllib.parse.unquote_plus(release_id)

            rel_item = post.post_member(release_id, original_sample_id, user, studies)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_release_item: %s", repr(dke))
            retcode = 422
            rel_item = str(dke)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_release_item: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode


    def create_release_note(self, release_id, note_id, release_note, studies=None, user=None, auths=None):  # noqa: E501
        """Adds a note to an release

         # noqa: E501

        :param release_id: ID of release to modify
        :type release_id: str
        :param note_id: ID of note to modify in the set
        :type note_id: str
        :param release_note:
        :type release_note: dict | bytes

        :rtype: None
        """
        retcode = 201
        rel_item = None

        try:
            post = BaseReleaseNote(self.get_engine(), self.get_session())
            release_id = urllib.parse.unquote_plus(release_id)
            note_id = urllib.parse.unquote_plus(note_id)
            release_note.note_id = note_id
            release = BaseRelease(self.get_engine(), self.get_session())
            rel_id = None
            with session_scope(self.get_session()) as db:
                rel_id = release.convert_to_id(db, release_id)
            rel_item = post.post(rel_id, release_note, None, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_release_note: %s", repr(dke))
            retcode = 422
            rel_item = str(dke)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_release_note: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode

    def delete_release(self, release_id, studies=None, user=None, auths=None):  # noqa: E501
        """deletes an release

         # noqa: E501

        :param release_id: ID of release to delete
        :type release_id: str

        :rtype: None
        """
        retcode = 200
        rel_item = None

        try:
            delete = BaseRelease(self.get_engine(), self.get_session())
            release_id = urllib.parse.unquote_plus(release_id)

            rel_item = delete.delete(release_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "delete_release: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode

    def delete_release_item(self, release_id, original_sample_id, studies=None, user=None, auths=None):  # noqa: E501
        """deletes a release_item from an release

         # noqa: E501

        :param release_id: ID of release to modify
        :type release_id: str
        :param release_item_id: ID of release_item to remove from the set
        :type release_item_id: str

        :rtype: None
        """

        retcode = 200
        rel_item = None

        try:
            delete = BaseRelease(self.get_engine(), self.get_session())
            release_id = urllib.parse.unquote_plus(release_id)

            delete.delete_member(release_id, original_sample_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "delete_release_item: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode


    def delete_release_note(self, release_id, note_id, studies=None, user=None, auths=None):  # noqa: E501
        """deletes an release note

         # noqa: E501

        :param release_id: ID of release to modify
        :type release_id: str
        :param note_id: ID of note to remove from the set
        :type note_id: str

        :rtype: None
        """

        retcode = 200
        rel = None

        try:
            delete = BaseReleaseNote(self.get_engine(), self.get_session())
            release_id = urllib.parse.unquote_plus(release_id)
            note_id = urllib.parse.unquote_plus(note_id)
            release = BaseRelease(self.get_engine(), self.get_session())
            rel_id = None
            with session_scope(self.get_session()) as db:
                rel_id = release.convert_to_id(db, release_id)

            delete.delete(rel_id, note_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug("delete_event_set_note: %s", repr(dke))
            retcode = 404
            rel = str(dke)

        return rel, retcode


    def download_release(self, release_id, start=None, count=None, studies=None, user=None, auths=None):  # noqa: E501
        """fetches an release

         # noqa: E501

        :param release_id: ID of release to fetch
        :type release_id: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Release
        """

        retcode = 200
        rel_item = None

        if not release_id:
            rel_item = 'No release specified to download'
            logging.getLogger(__name__).debug("download_release: %s", rel_item)
            retcode = 404
        else:
            try:
                get = BaseRelease(self.get_engine(), self.get_session())
                release_id = urllib.parse.unquote_plus(release_id)
                rel_item = get.get_with_members(release_id, start=start, count=count, studies=studies)

            except MissingKeyException as dke:
                logging.getLogger(__name__).debug(
                    "download_release: %s", repr(dke))
                rel_item = str(dke)
                retcode = 404

        return rel_item, retcode

    def download_release_item(self, release_item_id, release_id=None,
                              original_sample_id=None, studies=None, user=None, auths=None):  # noqa: E501
        """fetches a release item

         # noqa: E501

        :param release_item_id: ID of release_item to fetch
        :type release_item_id: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Release
        """

        retcode = 200
        rel_item = None

        if not release_item_id:
            rel_item = 'No release item specified to download'
            logging.getLogger(__name__).debug("download_release_item: %s", rel_item)
            retcode = 404
        else:
            try:
                get = BaseReleaseItem(self.get_engine(), self.get_session())
                if release_id:
                    release_id = urllib.parse.unquote_plus(release_id)
                rel_item = get.get(release_item_id,
                                   release_id=release_id,
                                   original_sample_id=original_sample_id,
                                   studies=studies)

            except MissingKeyException as dke:
                logging.getLogger(__name__).debug(
                    "download_release_item: %s", repr(dke))
                rel_item = str(dke)
                retcode = 404

        return rel_item, retcode


    def download_releases(self, studies=None, user=None, auths=None):  # noqa: E501
        """fetches releases

         # noqa: E501


        :rtype: Releases
        """

        retcode = 200
        rel_items = None

        get = BaseRelease(self.get_engine(), self.get_session())
        start = None
        count = None
        rel_items = get.gets(studies, start, count)

        return rel_items, retcode


    def update_release(self, release_id, release, update_studies=None, studies=None, user=None, auths=None):  # noqa: E501
        """updates an release

         # noqa: E501

        :param release_id: ID of release to update
        :type release_id: str
        :param release:
        :type release: dict | bytes

        :rtype: Release
        """

        retcode = 200
        rel_item = None

        try:
            put = BaseRelease(self.get_engine(), self.get_session())
            release_id = urllib.parse.unquote_plus(release_id)
            rel_item = put.put(release_id, release, None,
                               update_studies=update_studies, studies=studies,
                               user=user)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_release: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode

    def update_release_item(self, release_item_id, release_item, update_samples=None, studies=None, user=None, auths=None):  # noqa: E501
        """updates an release

         # noqa: E501

        :param release_item_id: ID of release to update
        :type release_item_id: str
        :param release_item:
        :type release_item: dict | bytes

        :rtype: Release
        """

        retcode = 200
        rel_item = None

        try:
            put = BaseReleaseItem(self.get_engine(), self.get_session())
            release_item_id = urllib.parse.unquote_plus(release_item_id)
            rel_item = put.put(release_item_id, release_item, None,
                               update_samples=update_samples, studies=studies,
                               user=user)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_release_item: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode


    def update_release_note(self, release_id, note_id, release_note, studies=None, user=None, auths=None):  # noqa: E501
        """Adds a note to an release

         # noqa: E501

        :param release_id: ID of release to modify
        :type release_id: str
        :param note_id: ID of note to modify in the set
        :type note_id: str
        :param release_note:
        :type release_note: dict | bytes

        :rtype: None
        """

        retcode = 200
        rel = None

        try:
            put = BaseReleaseNote(self.get_engine(), self.get_session())
            release_id = urllib.parse.unquote_plus(release_id)
            note_id = urllib.parse.unquote_plus(note_id)
            release = BaseRelease(self.get_engine(), self.get_session())
            rel_id = None
            with session_scope(self.get_session()) as db:
                rel_id = release.convert_to_id(db, release_id)
            rel = put.put(rel_id, note_id, release_note, studies, user)
            rel = release.get(release_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_release_note: %s", repr(dke))
            retcode = 404
            rel = str(dke)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_release_note: %s", repr(dke))
            retcode = 422
            rel = str(dke)

        return rel, retcode
