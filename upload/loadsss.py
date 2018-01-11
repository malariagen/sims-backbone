# Import pandas
from __future__ import print_function
import pandas as pd
import sys

import swagger_client
from swagger_client.rest import ApiException
import uploader

class ExcelUploader(uploader.Uploader):

    _country_cache = {
        'nan': None
    }

    def load_data_file(self, filename, sheets):

        self.setup(filename)

        # Load spreadsheet
        xls = pd.ExcelFile(filename)

        sheet_study_map = {}

        configuration = swagger_client.Configuration()
        configuration.access_token = self._auth_token

        if sheets:
            #You will want Report as well if it's not a numbered study sheet
            sheet_names = sheets.split(',')
        else:
            sheet_names = xls.sheet_names

        for sheet in sheet_names:

            if not sheet[0].isdigit():
                event_set_api_instance = swagger_client.EventSetApi(swagger_client.ApiClient(configuration))
                event_set_id = self._event_set # str | ID of eventSet to create
                try:
                    # creates an eventSet
                    api_response = event_set_api_instance.create_event_set(sheet)
                except ApiException as e:
                    if e.status != 422: #Already existis
                        print("Exception when calling EventSetApi->create_event_set: %s\n" % e)

            df1 = xls.parse(sheet)
            start = False
            human = False
            for idx, row in df1.iterrows():
                if sheet == 'Report':
                    if str(row.iloc[2])[0].isdigit():
                        study_id = str(row.iloc[2])
                        sheet_name = str(row.iloc[1])
                        sheet_study_map[sheet_name] = study_id
                    continue


                if row.iloc[0] == 'Oxford Code':
                    start = True
                    continue
                if not start:
                    continue
                oxford_code = str(row.iloc[0])
                source_code = str(row.iloc[1])
                taxon = str(row.iloc[3])
                iso2 = str(row.iloc[5])
                state = str(row.iloc[8])
                if oxford_code == 'nan':
                    continue
                if taxon == 'HS':
                    if human:
                        continue
                    print('Ignoring HS in sheet {}'.format(sheet))
                    human = True
                    continue
                values = {
                    'sample_oxford_id': oxford_code,
                    'sample_partner_id': source_code,
                    'species': taxon,
                    'iso2': iso2,
                    'state': state
                }
                if iso2 not in self._country_cache:
                    try:
                        api_instance = swagger_client.MetadataApi(swagger_client.ApiClient(configuration))
                        metadata = api_instance.get_country_metadata(iso2)
                        self._country_cache[iso2] = metadata
                    except ApiException as e:
                        print("Exception when looking up country {} {}".format(iso2, values))


                if iso2 in self._country_cache and self._country_cache[iso2]:
                    values['country'] = self._country_cache[iso2].alpha3

                if sheet in sheet_study_map:
                    values['study_id'] = sheet_study_map[sheet]

                item = self.process_item(values)

                if not sheet[0].isdigit():
                    try:
                        event_set_api_instance.create_event_set_item(sheet, item.sampling_event_id)
                    except ApiException as err:
                        #Probably because it already exists
                        self._logger.debug("Error adding sample {} to event set {} {}".format(item.sampling_event_id, sheet, err))

                if item.location and 'country' in values:
                    item.location = self.update_country(values['country'], item.location)
                else:
                    print("No location {}".format(values))

#                print(values)
#                print(item)

                self.validate(values, item)


    def validate(self, input_values, output_values):

        if 'study_id' in input_values:
            if input_values['study_id'][:4] != output_values.study_id[:4]:
                if input_values['study_id'][:4] != '0000':
                    print("Conflicting study id {} {}".format(input_values, output_values))
        else:
            print("No study id {} {}".format(input_values, output_values))

if __name__ == '__main__':
    el = ExcelUploader(sys.argv[1])
    sheets = None
    if len(sys.argv) > 3:
        sheets = sys.argv[3]
    el.load_data_file(sys.argv[2], sheets)
