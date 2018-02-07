from __future__ import print_function
import sys

import swagger_client
from swagger_client.rest import ApiException
import uploader
import json

class Upload_ROMA(uploader.Uploader):

    def load_data_file(self, filename, sheets):

        self.setup(filename)

        print("Event set:" + self._event_set)

        with open(filename) as json_file:
            data = json.load(json_file)

        items = {}

        for item in data:
            if not item['model'] in items:
                items[item['model']] = {}
            items[item['model']][item['pk']] = item

        for key, item in items['samples.sample'].items():
            fields = item['fields']
            roma_id = fields['sample_name']
            source_code = fields['external_id']
            #source_code = None
            doc = fields['collection_date']
            loc = items['locations.location'][fields['location']]
            latitude = loc['fields']['latitude']
            longitude = loc['fields']['longitude']
            loc_name = loc['fields']['location_name']
            country = items['locations.country'][loc['fields']['country']]['fields']['iso3']
            roma_manifest_id = fields['manifest']
            roma_study_id = items['samples.manifest'][roma_manifest_id]['fields']['study']
            study_id = items['managements.study'][roma_study_id]['fields']['project_code'][1:]

            tags = {}
            if 'tags' in fields and fields['tags']:
                tags = json.loads(fields['tags'])

            oxford_code = None
            taxon = None
            if '27. original_oxford_code' in tags:
                oxford_code = tags['27. original_oxford_code']
                pass
            if '24. Patient Id' in tags:
                #oxford_code = tags['24. Patient Id']
                pass
            if 'Species' in tags:
                taxon = tags['Species']
            else:
                if filename.startswith('spot'):
                    taxon = 'P. falciparum'
                elif filename.startswith('vobs'):
                    taxon = 'Anopheles'
                elif filename.startswith('vivax'):
                    taxon = 'Plasmodium'

            values = {
                'study_id': study_id,
                'sample_roma_id': roma_id,
                'sample_oxford_id': oxford_code,
                'sample_partner_id': source_code,
                'species': taxon,
                'doc': doc,
                'location_name': loc_name,
                'country': country,
                'latitude': latitude,
                'longitude': longitude,
            }


            sampling_event = self.process_item(values)

#            print(values)
#            print(sampling_event)

            self.validate(values, sampling_event)


    def validate(self, input_values, output_values):

        if 'study_id' in input_values:
            if input_values['study_id'][:4] != output_values.study_id[:4]:
                if input_values['study_id'][:4] != '0000':
                    pass
                    #print("Conflicting study id {} {}".format(input_values, output_values))
        else:
            print("No study id {} {}".format(input_values, output_values))

if __name__ == '__main__':
    el = Upload_ROMA(sys.argv[1])
    sheets = None
    if len(sys.argv) > 3:
        sheets = sys.argv[3]
    el.load_data_file(sys.argv[2], sheets)
