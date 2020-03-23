import openapi_client
from openapi_client.rest import ApiException
from test_base import TestBase
from datetime import date

import sys
import pytest
import uuid

class TestManifests(TestBase):


    attr_value = 12345

    def create_original_sample(self, api_factory):

        os_api_instance = api_factory.OriginalSampleApi()
        ds_api_instance = api_factory.DerivativeSampleApi()
        ad_api_instance = api_factory.AssayDataApi()

        try:
            study_code = '1010-MD-UP'

            samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                 partner_species='PF')

            samp.attrs = [
                openapi_client.Attr(attr_type='oxford',
                                    attr_value=str(self.attr_value),
                                    attr_source='upd')
            ]
            self.attr_value = self.attr_value + 1
            created_os = os_api_instance.create_original_sample(samp)

            der_samp = openapi_client.DerivativeSample(None,
                                                       original_sample_id=created_os.original_sample_id)

            created_ds = ds_api_instance.create_derivative_sample(der_samp)

            a_data = openapi_client.AssayDatum(None,
                                               derivative_sample_id=created_ds.derivative_sample_id)

            created_ad = ad_api_instance.create_assay_datum(a_data)

            return created_os, created_ad

        except ApiException as error:
            self.check_api_exception(api_factory, "TestManifests->create_original_sample", error)

    def delete_original_sample(self, api_factory, original_sample, assay_datum):

        os_api_instance = api_factory.OriginalSampleApi()
        ds_api_instance = api_factory.DerivativeSampleApi()
        ad_api_instance = api_factory.AssayDataApi()

        try:
            ad_api_instance.delete_assay_datum(assay_datum.assay_datum_id)
            ds_api_instance.delete_derivative_sample(assay_datum.derivative_sample_id)
            os_api_instance.delete_original_sample(original_sample.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "TestManifests->create_original_sample", error)

    """
    """
    def test_create_manifest_simple(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            created = api_instance.create_manifest('Manifest1')
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_manifest succeeded')

            assert created.manifest_name == 'Manifest1'

            created = api_instance.delete_manifest('Manifest1')
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to delete_manifest succeeded')


        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)


    """
    """
    def test_create_member(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = 'Manifest2'
            created = api_instance.create_manifest(manifest)

            os_created, created = self.create_original_sample(api_factory)

            created_set = api_instance.create_manifest_item(manifest, os_created.original_sample_id)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_manifest_item succeeded')
            fetched_set = api_instance.download_manifest(manifest)

            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to download_manifest succeeded')

            assert fetched_set.members.count == 1
            assert fetched_set.members.manifest_items[0].original_sample_id == os_created.original_sample_id

            api_instance.delete_manifest_item(manifest, os_created.original_sample_id)

            fetched_set = api_instance.download_manifest(manifest)

            assert fetched_set.members.count == 0

            self.delete_original_sample(api_factory, os_created, created)

            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)


    """
    """
    def test_lookup_manifest_member(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = 'Manifest2'
            created = api_instance.create_manifest(manifest)

            os_created, created = self.create_original_sample(api_factory)

            created_item = api_instance.create_manifest_item(manifest, os_created.original_sample_id)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_manifest_item succeeded')
            fetched_set = api_instance.download_manifest(manifest)

            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to download_manifest succeeded')

            assert fetched_set.members.count == 1
            assert fetched_set.members.manifest_items[0].original_sample_id == os_created.original_sample_id

            looked_up = api_instance.download_manifest_item(created_item.manifest_item_id)

            assert created_item == looked_up

            looked_up = api_instance.download_manifest_item('unknown',
                                                            manifest_id=manifest,
                                                            original_sample_id=os_created.original_sample_id)

            assert created_item == looked_up

            api_instance.delete_manifest_item(manifest, os_created.original_sample_id)

            fetched_set = api_instance.download_manifest(manifest)

            assert fetched_set.members.count == 0

            self.delete_original_sample(api_factory, os_created, created)

            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_update_manifest_member(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = 'Manifest2'
            created = api_instance.create_manifest(manifest)

            os_created, created = self.create_original_sample(api_factory)

            created_item = api_instance.create_manifest_item(manifest, os_created.original_sample_id)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_manifest_item succeeded')
            fetched_set = api_instance.download_manifest(manifest)

            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to download_manifest succeeded')

            assert fetched_set.members.count == 1
            assert fetched_set.members.manifest_items[0].original_sample_id == os_created.original_sample_id

            created_item.attrs = [
                openapi_client.Attr(attr_type='update_item',
                                    attr_value=str(self.attr_value),
                                    attr_source='upd')
            ]
            created_item.original_sample = {'original_sample_id': uuid.uuid4()}
            orig_ad = created_item.assay_data
            created_item.assay_data = {'count': 0, 'assay_data': []}
            updated_item = api_instance.update_manifest_item(created_item.manifest_item_id, created_item)

            created_item.original_sample = os_created
            created_item.assay_data = orig_ad
            created_item.version = updated_item.version

            assert created_item == updated_item

            api_instance.delete_manifest_item(manifest, os_created.original_sample_id)

            fetched_set = api_instance.download_manifest(manifest)

            assert fetched_set.members.count == 0

            self.delete_original_sample(api_factory, os_created, created)

            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_create_missing_member(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = 'Manifest2'
            created = api_instance.create_manifest(manifest)

            with pytest.raises(ApiException, status=404):
                created_set = api_instance.create_manifest_item('404', str(uuid.uuid4()))

            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_create_member_permissions(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    created_set = api_instance.create_manifest_item('404', str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=403):
                    created_set = api_instance.create_manifest_item('404', str(uuid.uuid4()))


        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_create_note(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = 'Manifest3'
            evsn = openapi_client.ManifestNote('note3', 'note3text')
            created = api_instance.create_manifest(manifest)

            created_set = api_instance.create_manifest_note(manifest, evsn.note_name, evsn)

            fetched_set = api_instance.download_manifest(manifest)

            assert fetched_set.notes[0].note_name == evsn.note_name

            with pytest.raises(ApiException, status=422):
                created_set = api_instance.create_manifest_note(manifest, evsn.note_name, evsn)


            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_update_note(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = 'Manifest4'
            evsn = openapi_client.ManifestNote('note4', 'note4text')
            created = api_instance.create_manifest(manifest)

            created_set = api_instance.create_manifest_note(manifest, evsn.note_name, evsn)

            fetched_set = api_instance.download_manifest(manifest)

            note = fetched_set.notes[0]

            assert note.note_name == evsn.note_name
            assert note.note_text == evsn.note_text

            assert len(fetched_set.notes) == 1

            new_text = 'updated_note'

            note.note_text = new_text

            api_instance.update_manifest_note(manifest, note.note_name, note)

            fetched_set = api_instance.download_manifest(manifest)

            assert len(fetched_set.notes) == 1

            note = fetched_set.notes[0]

            assert note.note_name == evsn.note_name
            assert note.note_text == new_text

            with pytest.raises(ApiException, status=404):
                api_instance.update_manifest_note(manifest, '404', note)

            #Can't change the name of a note to be the same as another note
            evsna = openapi_client.ManifestNote('note4a', 'note4atext')
            created_set = api_instance.create_manifest_note(manifest, evsna.note_name, evsna)

            with pytest.raises(ApiException, status=422):
                api_instance.update_manifest_note(manifest, evsn.note_name, evsna)


            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_delete_note(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = 'Manifest5'
            evsn = openapi_client.ManifestNote('note5', 'note5text')
            created = api_instance.create_manifest(manifest)

            created_set = api_instance.create_manifest_note(manifest, evsn.note_name, evsn)

            fetched_set = api_instance.download_manifest(manifest)

            note = fetched_set.notes[0]

            assert note.note_name == evsn.note_name
            assert note.note_text == evsn.note_text

            api_instance.delete_manifest_note(manifest, note.note_name)

            fetched_set = api_instance.download_manifest(manifest)

            assert fetched_set.notes is None

            with pytest.raises(ApiException, status=404):
                api_instance.delete_manifest_note(manifest, note.note_name)


            with pytest.raises(ApiException, status=404):
                api_instance.delete_manifest_note('xxxx', note.note_name)


            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_manifests(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            sets = ['Manifest6', 'Manifest7']

            for evset in sets:
                created = api_instance.create_manifest(evset)
            downloaded = api_instance.download_manifests()

            print(downloaded)
            assert len(downloaded.manifests) == 2

            for evset in sets:
                api_instance.delete_manifest(evset)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_update_manifest(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = 'Manifest8'
            created = api_instance.create_manifest(manifest)

            os_created, created = self.create_original_sample(api_factory)

            os_created2, created2 = self.create_original_sample(api_factory)

            created_set = api_instance.create_manifest_item(manifest, os_created.original_sample_id)
            created_set2 = api_instance.create_manifest_item(manifest, os_created2.original_sample_id)
            fetched_set1 = api_instance.download_manifest(manifest)

            assert fetched_set1.members.count == 2
            ids = []
            for i in fetched_set1.members.manifest_items:
                ids.append(i.original_sample_id)
            assert os_created.original_sample_id in ids
            assert fetched_set1.notes is None

            evsn = openapi_client.ManifestNote('note8', 'note8text')

            fetched_set1.notes = [evsn]

            api_instance.update_manifest(manifest, fetched_set1,
                                         update_studies=True)

            fetched_set2 = api_instance.download_manifest(manifest)
            assert fetched_set2.studies.count == 1
            assert fetched_set2.studies.studies[0].name == os_created.study_name
            assert fetched_set2.members.manifest_items[0].assay_data.count == 1
            assert fetched_set2.members.count == 2
            assert len(fetched_set2.notes) == 1

            api_instance.delete_manifest_item(manifest, os_created.original_sample_id)
            api_instance.delete_manifest_item(manifest, os_created2.original_sample_id)

            fetched_set = api_instance.download_manifest(manifest)

            assert fetched_set.members.count == 0


            self.delete_original_sample(api_factory, os_created, created)
            self.delete_original_sample(api_factory, os_created2, created2)
            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_create_duplicate(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = 'Manifest9'

            created = api_instance.create_manifest(manifest)

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_manifest(manifest)

            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_create_note_duplicate(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = 'Manifest10'
            evsn = openapi_client.ManifestNote('note10', 'note10text')
            created = api_instance.create_manifest(manifest)

            created_set = api_instance.create_manifest_note(manifest, evsn.note_name, evsn)
            with pytest.raises(ApiException, status=422):
                created_set = api_instance.create_manifest_note(manifest, evsn.note_name, evsn)

            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_create_member_duplicate(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = 'Manifest11'
            created = api_instance.create_manifest(manifest)

            os_created, created = self.create_original_sample(api_factory)

            created_set = api_instance.create_manifest_item(manifest, os_created.original_sample_id)

            with pytest.raises(ApiException, status=422):
                created_set = api_instance.create_manifest_item(manifest, os_created.original_sample_id)

            api_instance.delete_manifest_item(manifest, os_created.original_sample_id)

            self.delete_original_sample(api_factory, os_created, created)
            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_delete_missing_member(self, api_factory):

        api_instance = api_factory.ManifestApi()
        event_api_instance = api_factory.OriginalSampleApi()

        try:

            manifest = 'Manifest12'
            created = api_instance.create_manifest(manifest)

            os_created, created = self.create_original_sample(api_factory)

            created_set = api_instance.create_manifest_item(manifest, os_created.original_sample_id)

            api_instance.delete_manifest_item(manifest, os_created.original_sample_id)

            with pytest.raises(ApiException, status=404):
                api_instance.delete_manifest_item(manifest, os_created.original_sample_id)

            self.delete_original_sample(api_factory, os_created, created)
            api_instance.delete_manifest(manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest", error)

    """
    """
    def test_create_note_missing_manifest(self, api_factory):

        api_instance = api_factory.ManifestApi()
        event_api_instance = api_factory.OriginalSampleApi()

        try:

            evsn = openapi_client.ManifestNote('note404', 'note404text')

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    created_set = api_instance.create_manifest_note('404', evsn.note_name, evsn)
            else:
                with pytest.raises(ApiException, status=403):
                    created_set = api_instance.create_manifest_note('404', evsn.note_name, evsn)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->create_manifest_note", error)


    """
    """
    def test_download_missing(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.download_manifest('404')
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.download_manifest('404')

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->download_manifest", error)

    """
    """
    def test_update_missing(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:

            manifest = openapi_client.Manifest('404')

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.update_manifest('404',manifest)
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.update_manifest('404',manifest)

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->update_manifest", error)


    """
    """
    def test_delete_missing(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:


            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.delete_manifest('404')
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_manifest('404')

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->delete_manifest", error)

    """
    """
    def test_delete_item_permission(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:


            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_manifest_item('404', str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->delete_manifest_item", error)

    """
    """
    def test_delete_note_permission(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:


            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_manifest_note('404', '404 note')

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->delete_manifest_note", error)


    """
    """
    def test_update_note_permission(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:


            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.update_manifest_note('404', '404 note', {})

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->update_manifest_note", error)

    """
    """
    def test_download_permission(self, api_factory):

        api_instance = api_factory.ManifestApi()

        try:


            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.download_manifests()

        except ApiException as error:
            self.check_api_exception(api_factory, "ManifestsApi->download_manifests", error)
