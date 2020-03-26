from __future__ import print_function
import sys

import openapi_client
from openapi_client.rest import ApiException
import uploader
import json
import datetime
import time

class Upload_ROMA(uploader.Uploader):

    def clean_up_manifests(self, instance, items, max_manifest, max_location):

        original_samples_to_delete = []
        sampling_events_to_delete = []
        event_sets_to_delete = []
        for manifest_id in range(1, max_manifest + 1):
            if manifest_id not in items['samples.manifest']:
                event_set_name = f'{instance}_MNF{str(manifest_id).zfill(5)}'
                try:
                    samples = self._dao.download_original_samples_by_event_set(event_set_name)
                    for sample in samples.original_samples:
                        original_samples_to_delete.append(sample.original_sample_id)
                        if sample.sampling_event_id not in sampling_events_to_delete:
                            sampling_events_to_delete.append(sample.sampling_event_id)
                    samples = self._dao.download_sampling_events_by_event_set(event_set_name)
                    for sample in samples.sampling_events:
                        if sample.sampling_event_id not in sampling_events_to_delete:
                            sampling_events_to_delete.append(sample)
                    event_sets_to_delete.append(event_set_name)
                except ApiException as e:
                    print(e)
                    pass #Already gone

        locations_to_delete = []
        for location_id in range(1, max_location + 1):
            if location_id not in items['locations.location']:
                location_name = f'{instance}_loc_{location_id}'
                locations = self._dao.download_locations_by_attr('src_location_id',
                                                                 location_name)
                for location in locations.locations:
                    if location.location_id not in locations_to_delete:
                        locations_to_delete.append(location.location_id)

        return original_samples_to_delete, sampling_events_to_delete, event_sets_to_delete, locations_to_delete

    def load_data_file(self, filename):

        self.setup(filename)

        (instance,dumps,) = self._event_set.split('_')

        with open(filename) as json_file:
            data = json.load(json_file)

        items = {}
        event_sets = []
        max_manifest = 1
        max_location = 1

        for item in data:
            if not item['model'] in items:
                items[item['model']] = {}
            items[item['model']][item['pk']] = item
            if item['model'] == 'samples.manifest':
                if item['pk'] > max_manifest:
                    max_manifest = item['pk']
            if item['model'] == 'locations.location':
                if item['pk'] > max_location:
                    max_location = item['pk']
            if item['model'] == 'samples.well':
                if 'sample_well' not in items:
                    items['sample_well'] = {}
                sample_id = item['fields']['sample']
                if sample_id in items['sample_well']:
                    items['sample_well'][sample_id].append(item)
                    print(f'{sample_id} in multiple wells')
                else:
                    items['sample_well'][sample_id] = [item]


        original_samples_to_delete, sampling_events_to_delete, event_sets_to_delete, locations_to_delete = self.clean_up_manifests(instance, items,
                                                                                                                                   max_manifest,
                                                                                                                                   max_location)
        self.delete_items(original_samples_to_delete,
                          sampling_events_to_delete, event_sets_to_delete,
                          locations_to_delete)

        proxy_locations = {}

        if 'locations.proxylocation' in items:
            for key, item in items['locations.proxylocation'].items():
                fields = item['fields']
                proxy_locations[fields['location']] = fields['proxy_location']


        for key, item in items['samples.sample'].items():
            roma_pk_id = instance + '_' + str(item['pk'])
            fields = item['fields']
            roma_id = fields['sample_name']
            creation_date = fields['creation_date']
            source_code = fields['external_id'].strip()
            #source_code = None
            date_format = '%Y-%m-%d'
            doc = datetime.datetime(*(time.strptime(fields['collection_date'], date_format))[:6]).date()

            loc = items['locations.location'][fields['location']]
            src_location_id = instance + '_loc_' + str(loc['pk'])
            latitude = loc['fields']['latitude']
            longitude = loc['fields']['longitude']
            loc_name = loc['fields']['location_name']
            country = items['locations.country'][loc['fields']['country']]['fields']['iso3']

            proxy_latitude = None
            proxy_longitude = None
            proxy_loc_name = None
            proxy_country = None
            proxy_src_location_id = None

            if fields['location'] in proxy_locations:
                proxy_loc = items['locations.location'][proxy_locations[fields['location']]]
                proxy_src_location_id = instance + '_loc_' + str(proxy_loc['pk'])
                proxy_latitude = proxy_loc['fields']['latitude']
                proxy_longitude = proxy_loc['fields']['longitude']
                proxy_loc_name = proxy_loc['fields']['location_name']
                proxy_loc_name = proxy_loc_name.strip()
                proxy_country = items['locations.country'][proxy_loc['fields']['country']]['fields']['iso3']

            roma_manifest_id = fields['manifest']
            roma_study_id = items['samples.manifest'][roma_manifest_id]['fields']['study']
            manifest = instance + '_' + items['samples.manifest'][roma_manifest_id]['fields']['name']
            updated_by = items['samples.manifest'][roma_manifest_id]['fields']['updated_by'][0]
            study_id = items['managements.study'][roma_study_id]['fields']['project_code'][1:]

            tags = {}
            if 'tags' in fields and fields['tags']:
                if isinstance(fields['tags'], str):
                    tags = json.loads(fields['tags'])
                else:
                    tags = fields['tags']

            oxford_code = None
            taxon = None
            patient_id = None
            if '27. original_oxford_code' in tags:
                oxford_code = tags['27. original_oxford_code'].strip()
                pass
            if 'Patient Id' in tags:
                patient_id = tags['Patient Id']
            elif '24. Patient Id' in tags:
                patient_id = tags['24. Patient Id']

            if 'Species' in tags:
                taxon = tags['Species'].strip()
            else:
                if filename.startswith('spot'):
                    taxon = 'P. falciparum'
                elif filename.startswith('vobs'):
                    taxon = 'Anopheles'
                elif filename.startswith('vivax'):
                    taxon = 'Plasmodium'

            well = {
                'well_pk_id': None,
                'plate_name': None,
                'plate_position': None
            }
            wells = [ well ]
            if 'sample_well' in items and item['pk'] in items['sample_well']:
                sample_wells = items['sample_well'][item['pk']]
                wells = []
                for well in sample_wells:
                    plate = items['samples.plate'][well['fields']['plate']]
                    wells.append({
                        'well_pk_id': instance + '_well_' + str(well['pk']),
                        'plate_name': plate['fields']['name'],
                        'plate_position': well['fields']['position']
                    })

            for well in wells:
                values = {
                    'study_id': study_id.strip(),
                    'sample_roma_id': roma_id.strip(),
                    'roma_pk_id': roma_pk_id,
                    'sample_oxford_id': oxford_code,
                    'sample_partner_id': source_code,
                    'patient_id': patient_id,
                    'species': taxon,
                    'doc': doc,
                    'creation_date': creation_date,
                    'src_location_id': src_location_id,
                    'proxy_src_location_id': proxy_src_location_id,
                    'location_name': loc_name.strip(),
                    'country': country.strip(),
                    'latitude': latitude,
                    'longitude': longitude,
                    'proxy_latitude': proxy_latitude,
                    'proxy_longitude': proxy_longitude,
                    'proxy_location_name': proxy_loc_name,
                    'proxy_country': proxy_country,
                    'manifest': manifest,
                    'updated_by': updated_by,
                    'unique_ds_id': well['well_pk_id'],
                    'plate_name': well['plate_name'],
                    'plate_position': well['plate_position']
                }

                sampling_event = self.process_item(values)

                if values['manifest'] not in event_sets:
                    self._dao.create_event_set(values['manifest'])
                    event_sets.append(values['manifest'])

                if sampling_event:
                    if not sampling_event.event_sets or values['manifest'] not in sampling_event.event_sets:
                        self._dao.create_event_set_item(values['manifest'],
                                                        sampling_event.sampling_event_id)
                #print(values)
                #print(sampling_event)

                self.validate(values, sampling_event)

    def delete_items(self, original_samples_to_delete,
                     sampling_events_to_delete, event_sets_to_delete,
                     locations_to_delete):
        # Need to do after processing otherwise sampling event may still
        # reference location
        for original_sample_id in original_samples_to_delete:
            sample = self._dao.download_original_sample(original_sample_id)
            if sample.sampling_event_id not in sampling_events_to_delete:
                sampling_events_to_delete.append(sample.sampling_event_id)
            self._dao.delete_original_sample(original_sample_id)
        for sampling_event_id in sampling_events_to_delete:
            sample = self._dao.download_sampling_event(sampling_event_id)
            for event_set_name in sample.event_sets:
                self._dao.delete_event_set_item(event_set_name,
                                                sample.sampling_event_id)
            self._dao.delete_sampling_event(sample.sampling_event_id)
        for event_set_name in event_sets_to_delete:
            self._dao.delete_event_set(event_set_name)
        for location_id in locations_to_delete:
            try:
                self._dao.delete_location(location_id)
            except ApiException as e:
                print(e)
                pass


    def validate(self, input_values, output_values):

        if not output_values:
            #Item wasn't processed but should be messages elsewhere
            return

        if 'study_id' not in input_values:
            print("No study id {} {}".format(input_values, output_values))

if __name__ == '__main__':
    el = Upload_ROMA(sys.argv[1])
    el.load_data_file(sys.argv[2])
