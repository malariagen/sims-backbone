import sys

import logging

import openapi_client
from openapi_client.rest import ApiException

from base_entity import BaseEntity


class ManifestProcessor(BaseEntity):

    def __init__(self, dao, event_set):
        super().__init__(dao, event_set)
        self._logger = logging.getLogger(__name__)
        self._dao = dao
        self._event_set = event_set
        self._manifest_cache = []
        self._item_cache = {}

    def create_manifest_item_from_values(self, values, original_sample):

        if not original_sample:
            return None

        r_sample = openapi_client.ManifestItem(None,
                                               original_sample_id=original_sample.original_sample_id)

        idents = []

        r_sample.attrs = idents

        return r_sample

    def lookup_manifest_item(self, samp, values):

        existing = None

        if not samp or 'release' not in values:
            return existing

        manifest = values['release']
        if manifest not in self._manifest_cache:
            self._item_cache[manifest] = {}
            try:
                self._dao.create_manifest(manifest)
            except ApiException as error:
                self._item_cache[manifest] = {}
                downloaded_manifest = self._dao.download_manifest(manifest)
                for member in downloaded_manifest.members.manifest_items:
                    self._item_cache[manifest][member.original_sample_id] = member
            self._manifest_cache.append(manifest)

        if samp.original_sample_id in self._item_cache[manifest]:
            existing = self._item_cache[manifest][samp.original_sample_id]

        #if not existing:
        #    print('Not found {}'.format(samp))
        return existing

    def process_manifest_item(self, samp, existing, original_sample, values):

        user = None
        if 'updated_by' in values:
            user = values['updated_by']

        if 'release' not in values:
            return

        if not original_sample:
            print(f'No original sample {values}')
            return

        manifest = values['release']
        manifest_item = None
        if not existing:
            manifest_item = self._dao.create_manifest_item(manifest, original_sample.original_sample_id)
            self._item_cache[manifest][original_sample.original_sample_id] = manifest_item
        manifest_item = self._item_cache[manifest][original_sample.original_sample_id]

        # Attrs are only ever added or changed
        changed = False
        for attr in samp.attrs:
            found = False
            if manifest_item.attrs:
                for old_attr in manifest_item.attrs:
                    if old_attr.attr_type == attr.attr_type:
                        found = True
                        if not old_attr.attr_value == attr.attr_value:
                            old_attr.attr_value = attr.attr_value
                            old_attr.attr_source = self._event_set
                            changed = True
            else:
                manifest_item.attrs = []
            if not found:
                changed = True
                manifest_item.attrs.append(attr)

        if changed:
            manifest_item = self._dao.update_manifest_item(manifest_item.manifest_item_id,
                                                           manifest_item, update_samples=True)
            self._item_cache[manifest][original_sample.original_sample_id] = manifest_item
