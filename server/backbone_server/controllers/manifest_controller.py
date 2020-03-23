import urllib
import logging

from openapi_server.models.manifest import Manifest  # noqa: E501
from openapi_server.models.manifest_item import ManifestItem  # noqa: E501
from openapi_server.models.manifest_note import ManifestNote  # noqa: E501
from openapi_server.models.manifests import Manifests  # noqa: E501
from openapi_server import util

from backbone_server.controllers.base_controller import BaseController

from backbone_server.model.scope import session_scope

from backbone_server.model.manifest import BaseManifest, BaseManifestItem
from backbone_server.model.manifest_note import BaseManifestNote

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.controllers.decorators import apply_decorators

@apply_decorators
class ManifestController(BaseController):

    def create_manifest(self, manifest_id, studies=None, user=None, auths=None):  # noqa: E501
        """creates an manifest

         # noqa: E501

        :param manifest_id: ID of manifest to create
        :type manifest_id: str

        :rtype: Manifest
        """
        retcode = 201
        rel = None

        try:
            post = BaseManifest(self.get_engine(), self.get_session())
            manifest_id = urllib.parse.unquote_plus(manifest_id)

            rel = post.post(manifest_id, None, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_manifest: %s", repr(dke))
            rel = str(dke)
            retcode = 422

        return rel, retcode


    def create_manifest_item(self, manifest_id, original_sample_id, studies=None, user=None, auths=None):  # noqa: E501
        """Adds an item  to a manifest

         # noqa: E501

        :param manifest_id: ID of manifest to modify
        :type manifest_id: str
        :param manifest_item:
        :type manifest_item: dict | bytes

        :rtype: None
        """

        retcode = 201
        rel_item = None

        try:
            post = BaseManifest(self.get_engine(), self.get_session())
            manifest_id = urllib.parse.unquote_plus(manifest_id)

            rel_item = post.post_member(manifest_id, original_sample_id, user, studies)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_manifest_item: %s", repr(dke))
            retcode = 422
            rel_item = str(dke)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_manifest_item: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode


    def create_manifest_note(self, manifest_id, note_id, manifest_note, studies=None, user=None, auths=None):  # noqa: E501
        """Adds a note to an manifest

         # noqa: E501

        :param manifest_id: ID of manifest to modify
        :type manifest_id: str
        :param note_id: ID of note to modify in the set
        :type note_id: str
        :param manifest_note:
        :type manifest_note: dict | bytes

        :rtype: None
        """
        retcode = 201
        rel_item = None

        try:
            post = BaseManifestNote(self.get_engine(), self.get_session())
            manifest_id = urllib.parse.unquote_plus(manifest_id)
            note_id = urllib.parse.unquote_plus(note_id)
            manifest_note.note_id = note_id
            manifest = BaseManifest(self.get_engine(), self.get_session())
            rel_id = None
            with session_scope(self.get_session()) as db:
                rel_id = manifest.convert_to_id(db, manifest_id)
            rel_item = post.post(rel_id, manifest_note, None, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_manifest_note: %s", repr(dke))
            retcode = 422
            rel_item = str(dke)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_manifest_note: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode

    def delete_manifest(self, manifest_id, studies=None, user=None, auths=None):  # noqa: E501
        """deletes an manifest

         # noqa: E501

        :param manifest_id: ID of manifest to delete
        :type manifest_id: str

        :rtype: None
        """
        retcode = 200
        rel_item = None

        try:
            delete = BaseManifest(self.get_engine(), self.get_session())
            manifest_id = urllib.parse.unquote_plus(manifest_id)

            rel_item = delete.delete(manifest_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "delete_manifest: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode

    def delete_manifest_item(self, manifest_id, original_sample_id, studies=None, user=None, auths=None):  # noqa: E501
        """deletes a manifest_item from an manifest

         # noqa: E501

        :param manifest_id: ID of manifest to modify
        :type manifest_id: str
        :param manifest_item_id: ID of manifest_item to remove from the set
        :type manifest_item_id: str

        :rtype: None
        """

        retcode = 200
        rel_item = None

        try:
            delete = BaseManifest(self.get_engine(), self.get_session())
            manifest_id = urllib.parse.unquote_plus(manifest_id)

            delete.delete_member(manifest_id, original_sample_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "delete_manifest_item: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode


    def delete_manifest_note(self, manifest_id, note_id, studies=None, user=None, auths=None):  # noqa: E501
        """deletes an manifest note

         # noqa: E501

        :param manifest_id: ID of manifest to modify
        :type manifest_id: str
        :param note_id: ID of note to remove from the set
        :type note_id: str

        :rtype: None
        """

        retcode = 200
        rel = None

        try:
            delete = BaseManifestNote(self.get_engine(), self.get_session())
            manifest_id = urllib.parse.unquote_plus(manifest_id)
            note_id = urllib.parse.unquote_plus(note_id)
            manifest = BaseManifest(self.get_engine(), self.get_session())
            rel_id = None
            with session_scope(self.get_session()) as db:
                rel_id = manifest.convert_to_id(db, manifest_id)

            delete.delete(rel_id, note_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug("delete_event_set_note: %s", repr(dke))
            retcode = 404
            rel = str(dke)

        return rel, retcode


    def download_manifest(self, manifest_id, start=None, count=None, studies=None, user=None, auths=None):  # noqa: E501
        """fetches an manifest

         # noqa: E501

        :param manifest_id: ID of manifest to fetch
        :type manifest_id: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Manifest
        """

        retcode = 200
        rel_item = None

        if not manifest_id:
            rel_item = 'No manifest specified to download'
            logging.getLogger(__name__).debug("download_manifest: %s", rel_item)
            retcode = 404
        else:
            try:
                get = BaseManifest(self.get_engine(), self.get_session())
                manifest_id = urllib.parse.unquote_plus(manifest_id)
                rel_item = get.get_with_members(manifest_id, start=start, count=count, studies=studies)

            except MissingKeyException as dke:
                logging.getLogger(__name__).debug(
                    "download_manifest: %s", repr(dke))
                rel_item = str(dke)
                retcode = 404

        return rel_item, retcode

    def download_manifest_item(self, manifest_item_id, manifest_id=None,
                              original_sample_id=None, studies=None, user=None, auths=None):  # noqa: E501
        """fetches a manifest item

         # noqa: E501

        :param manifest_item_id: ID of manifest_item to fetch
        :type manifest_item_id: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Manifest
        """

        retcode = 200
        rel_item = None

        if not manifest_item_id:
            rel_item = 'No manifest item specified to download'
            logging.getLogger(__name__).debug("download_manifest_item: %s", rel_item)
            retcode = 404
        else:
            try:
                get = BaseManifestItem(self.get_engine(), self.get_session())
                if manifest_id:
                    manifest_id = urllib.parse.unquote_plus(manifest_id)
                rel_item = get.get(manifest_item_id,
                                   manifest_id=manifest_id,
                                   original_sample_id=original_sample_id,
                                   studies=studies)

            except MissingKeyException as dke:
                logging.getLogger(__name__).debug(
                    "download_manifest_item: %s", repr(dke))
                rel_item = str(dke)
                retcode = 404

        return rel_item, retcode


    def download_manifests(self, studies=None, user=None, auths=None):  # noqa: E501
        """fetches manifests

         # noqa: E501


        :rtype: Manifests
        """

        retcode = 200
        rel_items = None

        get = BaseManifest(self.get_engine(), self.get_session())
        start = None
        count = None
        rel_items = get.gets(studies, start, count)

        return rel_items, retcode


    def update_manifest(self, manifest_id, manifest, update_studies=None, studies=None, user=None, auths=None):  # noqa: E501
        """updates an manifest

         # noqa: E501

        :param manifest_id: ID of manifest to update
        :type manifest_id: str
        :param manifest:
        :type manifest: dict | bytes

        :rtype: Manifest
        """

        retcode = 200
        rel_item = None

        try:
            put = BaseManifest(self.get_engine(), self.get_session())
            manifest_id = urllib.parse.unquote_plus(manifest_id)
            rel_item = put.put(manifest_id, manifest, None,
                               update_studies=update_studies, studies=studies,
                               user=user)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_manifest: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode

    def update_manifest_item(self, manifest_item_id, manifest_item, update_samples=None, studies=None, user=None, auths=None):  # noqa: E501
        """updates an manifest

         # noqa: E501

        :param manifest_item_id: ID of manifest to update
        :type manifest_item_id: str
        :param manifest_item:
        :type manifest_item: dict | bytes

        :rtype: Manifest
        """

        retcode = 200
        rel_item = None

        try:
            put = BaseManifestItem(self.get_engine(), self.get_session())
            manifest_item_id = urllib.parse.unquote_plus(manifest_item_id)
            rel_item = put.put(manifest_item_id, manifest_item, None,
                               update_samples=update_samples, studies=studies,
                               user=user)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_manifest_item: %s", repr(dke))
            retcode = 404
            rel_item = str(dke)

        return rel_item, retcode


    def update_manifest_note(self, manifest_id, note_id, manifest_note, studies=None, user=None, auths=None):  # noqa: E501
        """Adds a note to an manifest

         # noqa: E501

        :param manifest_id: ID of manifest to modify
        :type manifest_id: str
        :param note_id: ID of note to modify in the set
        :type note_id: str
        :param manifest_note:
        :type manifest_note: dict | bytes

        :rtype: None
        """

        retcode = 200
        rel = None

        try:
            put = BaseManifestNote(self.get_engine(), self.get_session())
            manifest_id = urllib.parse.unquote_plus(manifest_id)
            note_id = urllib.parse.unquote_plus(note_id)
            manifest = BaseManifest(self.get_engine(), self.get_session())
            rel_id = None
            with session_scope(self.get_session()) as db:
                rel_id = manifest.convert_to_id(db, manifest_id)
            rel = put.put(rel_id, note_id, manifest_note, studies, user)
            rel = manifest.get(manifest_id, studies)
        except MissingKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_manifest_note: %s", repr(dke))
            retcode = 404
            rel = str(dke)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_manifest_note: %s", repr(dke))
            retcode = 422
            rel = str(dke)

        return rel, retcode
