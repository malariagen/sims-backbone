import logging

from openapi_server.models.manifest import Manifest
from openapi_server.models.manifest_note import ManifestNote

from backbone_server.controllers.manifest_controller import ManifestController

from local.base_local_api import BaseLocalApi


class LocalManifestApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.manifest_controller = ManifestController()

    def create_manifest(self, manifest_id, studies=None):
        """
        creates an manifest

        :param manifest:
        :type manifest: dict | bytes

        :rtype: Manifest
        """
        (ret, retcode) = self.manifest_controller.create_manifest(manifest_id, studies=studies,
                                                                  user=self._user,
                                                                  auths=self.manifest_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Manifest')

    def create_manifest_item(self, manifest_id, manifest_item_id,
                             studies=None):
        """
        Adds a samplingEvent to an manifest

        :param manifest_id: ID of manifest to modify
        :type manifest_id: str
        :param manifest_item_id: ID of samplingEvent to add to the set
        :type manifest_item_id: str

        :rtype: Manifest
        """
        (ret, retcode) = self.manifest_controller.create_manifest_item(manifest_id,
                                                                       manifest_item_id,
                                                                       studies=studies,
                                                                       user=self._user,
                                                                       auths=self.manifest_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'ManifestItem')

    def create_manifest_note(self, manifest_id, note_id, note, studies=None):
        """
        Adds a note to an manifest

        :param manifest_id: ID of manifest to modify
        :type manifest_id: str
        :param note_id: ID of note to modify in the set
        :type note_id: str
        :param note:
        :type note: dict | bytes

        :rtype: None
        """
        (ret, retcode) = self.manifest_controller.create_manifest_note(manifest_id, note_id,
                                                                       note, studies=studies,
                                                                       user=self._user,
                                                                       auths=self.manifest_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def delete_manifest(self, manifest_id, studies=None):
        """
        deletes an manifest

        :param manifestId: ID of manifest to delete
        :type manifestId: str

        :rtype: None
        """
        (ret, retcode) = self.manifest_controller.delete_manifest(
            manifest_id, studies=studies,
            user=self._user, auths=self.manifest_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def delete_manifest_item(self, manifest_id, manifest_item_id, studies=None):
        """
        deletes a manifest item from an manifest

        :param manifestId: ID of manifest to modify
        :type manifestId: str
        :param manifest_item_id: ID of samplingEvent to remove from the set
        :type manifest_item_id: str

        :rtype: None
        """
        (ret, retcode) = self.manifest_controller.delete_manifest_item(manifest_id,
                                                                       manifest_item_id,
                                                                       studies=studies,
                                                                       user=self._user,
                                                                       auths=self.manifest_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode)

    def delete_manifest_note(self, manifest_id, note_id, studies=None):
        """
        deletes an manifest note

        :param manifest_id: ID of manifest to modify
        :type manifest_id: str
        :param note_id: ID of note to remove from the set
        :type note_id: str

        :rtype: None
        """
        (ret, retcode) = self.manifest_controller.delete_manifest_note(manifest_id, note_id,
                                                                       studies=studies,
                                                                       user=self._user,
                                                                       auths=self.manifest_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def download_manifest(self, manifest_id, studies=None, start=None, count=None):
        """
        fetches an manifest

        :param manifestId: ID of manifest to fetch
        :type manifestId: str

        :rtype: Manifest
        """
        (ret, retcode) = self.manifest_controller.download_manifest(manifest_id, start=start,
                                                                    count=count, studies=studies,
                                                                    user=self._user,
                                                                    auths=self.manifest_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Manifest')

    def download_manifest_item(self, manifest_item_id, manifest_id=None,
                               original_sample_id=None,
                               studies=None):
        """
        fetches an manifest

        :param manifestId: ID of manifest to fetch
        :type manifestId: str

        :rtype: Manifest
        """
        (ret, retcode) = self.manifest_controller.download_manifest_item(manifest_item_id, manifest_id=manifest_id,
                                                                         original_sample_id=original_sample_id, studies=studies,
                                                                         user=self._user,
                                                                         auths=self.manifest_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'ManifestItem')

    def download_manifests(self, studies=None):
        """
        fetches manifests


        :rtype: Manifests
        """
        (ret, retcode) = self.manifest_controller.download_manifests(studies=studies,
                                                                     user=self._user,
                                                                     auths=self.manifest_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'Manifests')


    def update_manifest(self, manifest_id, manifest, update_studies=None, studies=None):
        """
        updates an manifest

        :param manifest_id: ID of manifest to update
        :type manifest_id: str
        :param manifest:
        :type manifest: dict | bytes

        :rtype: Manifest
        """
        (ret, retcode) = self.manifest_controller.update_manifest(manifest_id, manifest,
                                                                  update_studies=update_studies,
                                                                  studies=studies,
                                                                  user=self._user,
                                                                  auths=self.manifest_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'Manifest')

    def update_manifest_item(self, manifest_item_id, manifest_item, update_samples=None, studies=None):
        """
        updates an manifest

        :param manifest_id: ID of manifest to update
        :type manifest_id: str
        :param manifest:
        :type manifest: dict | bytes

        :rtype: Manifest
        """
        (ret, retcode) = self.manifest_controller.update_manifest_item(manifest_item_id, manifest_item,
                                                                       update_samples=update_samples,
                                                                       studies=studies,
                                                                       user=self._user,
                                                                       auths=self.manifest_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'ManifestItem')

    def update_manifest_note(self, manifest_id, note_id, note, studies=None):
        """
        Adds a note to an manifest

        :param manifest_id: ID of manifest to modify
        :type manifest_id: str
        :param note_id: ID of note to modify in the set
        :type note_id: str
        :param note:
        :type note: dict | bytes

        :rtype: None
        """

        (ret, retcode) = self.manifest_controller.update_manifest_note(manifest_id, note_id,
                                                                       note, studies=studies,
                                                                       user=self._user,
                                                                       auths=self.manifest_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode)
