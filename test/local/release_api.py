import logging

from openapi_server.models.release import Release
from openapi_server.models.release_note import ReleaseNote

from backbone_server.controllers.release_controller import ReleaseController

from local.base_local_api import BaseLocalApi


class LocalReleaseApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.release_controller = ReleaseController()

    def create_release(self, release_id, studies=None):
        """
        creates an release

        :param release:
        :type release: dict | bytes

        :rtype: Release
        """
        (ret, retcode) = self.release_controller.create_release(release_id, studies=studies,
                                                                user=self._user,
                                                                auths=self.release_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Release')

    def create_release_item(self, release_id, release_item_id,
                              studies=None):
        """
        Adds a samplingEvent to an release

        :param release_id: ID of release to modify
        :type release_id: str
        :param release_item_id: ID of samplingEvent to add to the set
        :type release_item_id: str

        :rtype: Release
        """
        (ret, retcode) = self.release_controller.create_release_item(release_id,
                                                                     release_item_id,
                                                                     studies=studies,
                                                                     user=self._user,
                                                                     auths=self.release_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'Release')

    def create_release_note(self, release_id, note_id, note, studies=None):
        """
        Adds a note to an release

        :param release_id: ID of release to modify
        :type release_id: str
        :param note_id: ID of note to modify in the set
        :type note_id: str
        :param note:
        :type note: dict | bytes

        :rtype: None
        """
        (ret, retcode) = self.release_controller.create_release_note(release_id, note_id,
                                                                     note, studies=studies,
                                                                     user=self._user,
                                                                     auths=self.release_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def delete_release(self, release_id, studies=None):
        """
        deletes an release

        :param releaseId: ID of release to delete
        :type releaseId: str

        :rtype: None
        """
        (ret, retcode) = self.release_controller.delete_release(
            release_id, studies=studies,
            user=self._user, auths=self.release_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def delete_release_item(self, release_id, release_item_id, studies=None):
        """
        deletes a release item from an release

        :param releaseId: ID of release to modify
        :type releaseId: str
        :param release_item_id: ID of samplingEvent to remove from the set
        :type release_item_id: str

        :rtype: None
        """
        (ret, retcode) = self.release_controller.delete_release_item(release_id,
                                                                     release_item_id,
                                                                     studies=studies,
                                                                     user=self._user,
                                                                     auths=self.release_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode)

    def delete_release_note(self, release_id, note_id, studies=None):
        """
        deletes an release note

        :param release_id: ID of release to modify
        :type release_id: str
        :param note_id: ID of note to remove from the set
        :type note_id: str

        :rtype: None
        """
        (ret, retcode) = self.release_controller.delete_release_note(release_id, note_id,
                                                                     studies=studies,
                                                                     user=self._user,
                                                                     auths=self.release_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def download_release(self, release_id, studies=None, start=None, count=None):
        """
        fetches an release

        :param releaseId: ID of release to fetch
        :type releaseId: str

        :rtype: Release
        """
        (ret, retcode) = self.release_controller.download_release(release_id, start=start,
                                                                  count=count, studies=studies,
                                                                  user=self._user,
                                                                  auths=self.release_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Release')

    def download_releases(self, studies=None):
        """
        fetches releases


        :rtype: Releases
        """
        (ret, retcode) = self.release_controller.download_releases(studies=studies,
                                                                   user=self._user,
                                                                   auths=self.release_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'Releases')

    def update_release(self, release_id, release, update_studies=None, studies=None):
        """
        updates an release

        :param release_id: ID of release to update
        :type release_id: str
        :param release:
        :type release: dict | bytes

        :rtype: Release
        """
        (ret, retcode) = self.release_controller.update_release(release_id, release,
                                                                update_studies=update_studies,
                                                                studies=studies,
                                                                user=self._user,
                                                                auths=self.release_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'Release')

    def update_release_note(self, release_id, note_id, note, studies=None):
        """
        Adds a note to an release

        :param release_id: ID of release to modify
        :type release_id: str
        :param note_id: ID of note to modify in the set
        :type note_id: str
        :param note:
        :type note: dict | bytes

        :rtype: None
        """

        (ret, retcode) = self.release_controller.update_release_note(release_id, note_id,
                                                                     note, studies=studies,
                                                                     user=self._user,
                                                                     auths=self.release_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode)
