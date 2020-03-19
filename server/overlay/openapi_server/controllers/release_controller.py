import connexion
import six

from openapi_server.models.release import Release  # noqa: E501
from openapi_server.models.release_item import ReleaseItem  # noqa: E501
from openapi_server.models.release_note import ReleaseNote  # noqa: E501
from openapi_server.models.releases import Releases  # noqa: E501
from openapi_server import util

from backbone_server.controllers.release_controller import ReleaseController

release_controller = ReleaseController()

def create_release(release_id, studies=None, user=None, token_info=None):  # noqa: E501
    """creates an release

     # noqa: E501

    :param release_id: ID of release to create
    :type release_id: str

    :rtype: Release
    """
    return release_controller.create_release(release_id, studies=studies,
                                             user=user,
                                             auths=release_controller.token_info(token_info))


def create_release_item(release_id, release_item, studies=None, user=None, token_info=None):  # noqa: E501
    """Adds an item  to a release

     # noqa: E501

    :param release_id: ID of release to modify
    :type release_id: str
    :param release_item:
    :type release_item: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        release_item = ReleaseItem.from_dict(
            connexion.request.get_json())  # noqa: E501
    return release_controller.create_release_item(release_id, release_item, studies=studies,
                                                  user=user,
                                                  auths=release_controller.token_info(token_info))


def create_release_note(release_id, note_id, release_note, studies=None, user=None, token_info=None):  # noqa: E501
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
    if connexion.request.is_json:
        release_note = ReleaseNote.from_dict(
            connexion.request.get_json())  # noqa: E501
    return release_controller.create_release_note(release_id, note_id,
                                                  release_note, studies=studies,
                                                  user=user,
                                                  auths=release_controller.token_info(token_info))


def delete_release(release_id, studies=None, user=None, token_info=None):  # noqa: E501
    """deletes an release

     # noqa: E501

    :param release_id: ID of release to delete
    :type release_id: str

    :rtype: None
    """
    return release_controller.delete_release(release_id, studies=studies,
                                             user=user,
                                             auths=release_controller.token_info(token_info))


def delete_release_item(release_id, release_item_id, studies=None, user=None, token_info=None):  # noqa: E501
    """deletes a release_item from an release

     # noqa: E501

    :param release_id: ID of release to modify
    :type release_id: str
    :param release_item_id: ID of release_item to remove from the set
    :type release_item_id: str

    :rtype: None
    """
    return release_controller.delete_release_item(release_id, release_item_id, studies=studies,
                                                  user=user,
                                                  auths=release_controller.token_info(token_info))


def delete_release_note(release_id, note_id, studies=None, user=None, token_info=None):  # noqa: E501
    """deletes an release note

     # noqa: E501

    :param release_id: ID of release to modify
    :type release_id: str
    :param note_id: ID of note to remove from the set
    :type note_id: str

    :rtype: None
    """
    return release_controller.delete_release_note(release_id, note_id, studies=studies,
                                                  user=user,
                                                  auths=release_controller.token_info(token_info))


def download_release(release_id, start=None, count=None, studies=None, user=None, token_info=None):  # noqa: E501
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
    return release_controller.download_release(release_id, start=start,
                                               count=count, studies=studies,
                                               user=user,
                                               auths=release_controller.token_info(token_info))

def download_release_item(release_item_id,
                          release_id=None,
                          original_sample_id=None, studies=None, user=None,
                          token_info=None):  # noqa: E501
    """fetches an release item

     # noqa: E501

    :param release_item_id: ID of release_item to fetch - use unknown if using query params instead
    :type release_item_id: str
    :param release_id: if the release_item_id is not known then it is possible to use release_id and original_sample_id
    :type release_id: str
    :param original_sample_id: if the release_item_id is not known then it is possible to use release_id and original_sample_id
    :type original_sample_id: str

    :rtype: ReleaseItem
    """
    return release_controller.download_release_item(release_item_id,
                                                    release_id=release_id,
                                                    original_sample_id=original_sample_id, studies=studies,
                                                    user=user,
                                                    auths=release_controller.token_info(token_info))

def download_releases(studies=None, user=None, token_info=None):  # noqa: E501
    """fetches releases

     # noqa: E501


    :rtype: Releases
    """
    return release_controller.download_releases(studies=studies,
                                                user=user,
                                                auths=release_controller.token_info(token_info))


def update_release(release_id, release, update_studies=None, studies=None, user=None, token_info=None):  # noqa: E501
    """updates an release

     # noqa: E501

    :param release_id: ID of release to update
    :type release_id: str
    :param release:
    :type release: dict | bytes

    :rtype: Release
    """
    if connexion.request.is_json:
        release = Release.from_dict(connexion.request.get_json())  # noqa: E501
    return release_controller.update_release(release_id,
                                             release,
                                             update_studies=update_studies, studies=studies,
                                             user=user,
                                             auths=release_controller.token_info(token_info))

def update_release_item(release_item_id, release_item,
                        update_samples=None, studies=None, user=None,
                        token_info=None):  # noqa: E501
    """updates an release item

     # noqa: E501

    :param release_item_id: ID of release_item to update
    :type release_item_id: str
    :param release_item:
    :type release_item: dict | bytes
    :param update_samples: Update the saved samples
    :type update_samples: bool

    :rtype: ReleaseItem
    """
    if connexion.request.is_json:
        release_item = ReleaseItem.from_dict(
            connexion.request.get_json())  # noqa: E501
    return release_controller.update_release_item(release_item_id,
                                                  release_item,
                                                  update_samples=update_samples, studies=studies,
                                                  user=user,
                                                  auths=release_controller.token_info(token_info))

def update_release_note(release_id, note_id, release_note, studies=None, user=None, token_info=None):  # noqa: E501
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
    if connexion.request.is_json:
        release_note = ReleaseNote.from_dict(
            connexion.request.get_json())  # noqa: E501
    return release_controller.update_release_note(release_id, note_id,
                                                  release_note, studies=studies,
                                                  user=user,
                                                  auths=release_controller.token_info(token_info))
