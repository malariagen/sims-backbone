import connexion
import six

from openapi_server.models.manifest import Manifest  # noqa: E501
from openapi_server.models.manifest_item import ManifestItem  # noqa: E501
from openapi_server.models.manifest_note import ManifestNote  # noqa: E501
from openapi_server.models.manifests import Manifests  # noqa: E501
from openapi_server import util

from backbone_server.controllers.manifest_controller import ManifestController

manifest_controller = ManifestController()

def create_manifest(manifest_id, studies=None, user=None, token_info=None):  # noqa: E501
    """creates an manifest

     # noqa: E501

    :param manifest_id: ID of manifest to create
    :type manifest_id: str

    :rtype: Manifest
    """
    return manifest_controller.create_manifest(manifest_id, studies=studies,
                                               user=user,
                                               auths=manifest_controller.token_info(token_info))


def create_manifest_item(manifest_id, manifest_item, studies=None, user=None, token_info=None):  # noqa: E501
    """Adds an item  to a manifest

     # noqa: E501

    :param manifest_id: ID of manifest to modify
    :type manifest_id: str
    :param manifest_item:
    :type manifest_item: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        manifest_item = ManifestItem.from_dict(
            connexion.request.get_json())  # noqa: E501
    return manifest_controller.create_manifest_item(manifest_id, manifest_item, studies=studies,
                                                    user=user,
                                                    auths=manifest_controller.token_info(token_info))


def create_manifest_note(manifest_id, note_id, manifest_note, studies=None, user=None, token_info=None):  # noqa: E501
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
    if connexion.request.is_json:
        manifest_note = ManifestNote.from_dict(
            connexion.request.get_json())  # noqa: E501
    return manifest_controller.create_manifest_note(manifest_id, note_id,
                                                    manifest_note, studies=studies,
                                                    user=user,
                                                    auths=manifest_controller.token_info(token_info))


def delete_manifest(manifest_id, studies=None, user=None, token_info=None):  # noqa: E501
    """deletes an manifest

     # noqa: E501

    :param manifest_id: ID of manifest to delete
    :type manifest_id: str

    :rtype: None
    """
    return manifest_controller.delete_manifest(manifest_id, studies=studies,
                                               user=user,
                                               auths=manifest_controller.token_info(token_info))


def delete_manifest_item(manifest_id, manifest_item_id, studies=None, user=None, token_info=None):  # noqa: E501
    """deletes a manifest_item from an manifest

     # noqa: E501

    :param manifest_id: ID of manifest to modify
    :type manifest_id: str
    :param manifest_item_id: ID of manifest_item to remove from the set
    :type manifest_item_id: str

    :rtype: None
    """
    return manifest_controller.delete_manifest_item(manifest_id, manifest_item_id, studies=studies,
                                                    user=user,
                                                    auths=manifest_controller.token_info(token_info))


def delete_manifest_note(manifest_id, note_id, studies=None, user=None, token_info=None):  # noqa: E501
    """deletes an manifest note

     # noqa: E501

    :param manifest_id: ID of manifest to modify
    :type manifest_id: str
    :param note_id: ID of note to remove from the set
    :type note_id: str

    :rtype: None
    """
    return manifest_controller.delete_manifest_note(manifest_id, note_id, studies=studies,
                                                    user=user,
                                                    auths=manifest_controller.token_info(token_info))


def download_manifest(manifest_id, start=None, count=None, studies=None, user=None, token_info=None):  # noqa: E501
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
    return manifest_controller.download_manifest(manifest_id, start=start,
                                                 count=count, studies=studies,
                                                 user=user,
                                                 auths=manifest_controller.token_info(token_info))

def download_manifest_item(manifest_item_id,
                           manifest_id=None,
                           original_sample_id=None, studies=None, user=None,
                           token_info=None):  # noqa: E501
    """fetches an manifest item

     # noqa: E501

    :param manifest_item_id: ID of manifest_item to fetch - use unknown if using query params instead
    :type manifest_item_id: str
    :param manifest_id: if the manifest_item_id is not known then it is possible to use manifest_id and original_sample_id
    :type manifest_id: str
    :param original_sample_id: if the manifest_item_id is not known then it is possible to use manifest_id and original_sample_id
    :type original_sample_id: str

    :rtype: ManifestItem
    """
    return manifest_controller.download_manifest_item(manifest_item_id,
                                                      manifest_id=manifest_id,
                                                      original_sample_id=original_sample_id, studies=studies,
                                                      user=user,
                                                      auths=manifest_controller.token_info(token_info))

def download_manifests(studies=None, user=None, token_info=None):  # noqa: E501
    """fetches manifests

     # noqa: E501


    :rtype: Manifests
    """
    return manifest_controller.download_manifests(studies=studies,
                                                  user=user,
                                                  auths=manifest_controller.token_info(token_info))


def update_manifest(manifest_id, manifest, update_studies=None, studies=None, user=None, token_info=None):  # noqa: E501
    """updates an manifest

     # noqa: E501

    :param manifest_id: ID of manifest to update
    :type manifest_id: str
    :param manifest:
    :type manifest: dict | bytes

    :rtype: Manifest
    """
    if connexion.request.is_json:
        manifest = Manifest.from_dict(connexion.request.get_json())  # noqa: E501
    return manifest_controller.update_manifest(manifest_id,
                                               manifest,
                                               update_studies=update_studies, studies=studies,
                                               user=user,
                                               auths=manifest_controller.token_info(token_info))

def update_manifest_item(manifest_item_id, manifest_item,
                         update_samples=None, studies=None, user=None,
                         token_info=None):  # noqa: E501
    """updates an manifest item

     # noqa: E501

    :param manifest_item_id: ID of manifest_item to update
    :type manifest_item_id: str
    :param manifest_item:
    :type manifest_item: dict | bytes
    :param update_samples: Update the saved samples
    :type update_samples: bool

    :rtype: ManifestItem
    """
    if connexion.request.is_json:
        manifest_item = ManifestItem.from_dict(
            connexion.request.get_json())  # noqa: E501
    return manifest_controller.update_manifest_item(manifest_item_id,
                                                    manifest_item,
                                                    update_samples=update_samples, studies=studies,
                                                    user=user,
                                                    auths=manifest_controller.token_info(token_info))

def update_manifest_note(manifest_id, note_id, manifest_note, studies=None, user=None, token_info=None):  # noqa: E501
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
    if connexion.request.is_json:
        manifest_note = ManifestNote.from_dict(
            connexion.request.get_json())  # noqa: E501
    return manifest_controller.update_manifest_note(manifest_id, note_id,
                                                    manifest_note, studies=studies,
                                                    user=user,
                                                    auths=manifest_controller.token_info(token_info))
