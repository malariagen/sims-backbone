import sys
from copy import deepcopy

import logging

import openapi_client
from openapi_client.rest import ApiException

from base_entity import BaseEntity


class ReleaseProcessor(BaseEntity):

    def __init__(self, dao, event_set):
        super().__init__(dao, event_set)
        self._logger = logging.getLogger(__name__)
        self._dao = dao
        self._event_set = event_set
        self._release_cache = []
        self._item_cache = {}

    def create_release_item_from_values(self, values, original_sample):

        if not original_sample:
            return None

        r_sample = openapi_client.ReleaseItem(None,
                                              original_sample_id=original_sample.original_sample_id)

        idents = []

        r_sample.attrs = idents

        return r_sample

    def lookup_release_item(self, samp, values):

        existing = None

        if not samp or 'release' not in values:
            return existing

        release = values['release']
        if release not in self._release_cache:
            self._item_cache[release] = {}
            try:
                self._dao.create_release(release)
            except ApiException as error:
                self._item_cache[release] = {}
                downloaded_release = self._dao.download_release(release)
                for member in downloaded_release.members.release_items:
                    self._item_cache[release][member.original_sample_id] = member
            self._release_cache.append(release)

        if samp.original_sample_id in self._item_cache[release]:
            existing = self._item_cache[release][samp.original_sample_id]

        #if not existing:
        #    print('Not found {}'.format(samp))
        return existing

    def process_release_item(self, samp, existing, original_sample, values):

        user = None
        if 'updated_by' in values:
            user = values['updated_by']

        if 'release' not in values:
            return

        if not original_sample:
            print(f'No original sample {values}')
            return

        release = values['release']
        release_item = None
        if not existing:
            release_item = self._dao.create_release_item(release, original_sample.original_sample_id)
            self._item_cache[release][original_sample.original_sample_id] = release_item
        release_item = self._item_cache[release][original_sample.original_sample_id]

        # Attrs are only ever added or changed
        changed = False
        for attr in samp.attrs:
            found = False
            if release_item.attrs:
                for old_attr in release_item.attrs:
                    if old_attr.attr_type == attr.attr_type:
                        found = True
                        if not old_attr.attr_value == attr.attr_value:
                            old_attr.attr_value = attr.attr_value
                            old_attr.attr_source = self._event_set
                            changed = True
            else:
                release_item.attrs = []
            if not found:
                changed = True
                release_item.attrs.append(attr)

        if changed:
            release_item = self._dao.update_release_item(release_item.release_item_id,
                                                         release_item, update_samples=True)
            self._item_cache[release][original_sample.original_sample_id] = release_item
