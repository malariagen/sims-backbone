# Import pandas
from __future__ import print_function
import pandas as pd
import sys

import openapi_client
from openapi_client.rest import ApiException
import uploader

class Upload_SSR(uploader.Uploader):

    _country_cache = {
        'nan': None
    }

    def load_data_file(self, filename, sheets):

        self.setup(filename)

        # Load spreadsheet
        xls = pd.ExcelFile(filename)

        sheet_study_map = {}

        if sheets:
            #You will want Report as well if it's not a numbered study sheet
            sheet_names = sheets.split(',')
        else:
            sheet_names = xls.sheet_names

        for sheet in sheet_names:

            if not sheet[0].isdigit():
                event_set_id = self._event_set # str | ID of eventSet to create

                self._dao.create_event_set(sheet)

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
                if taxon == 'PF':
                    taxon = 'Plasmodium falciparum'
                if taxon == 'PV':
                    taxon = 'Plasmodium vivax'
                if taxon == 'PK':
                    taxon = 'Plasmodium knowlesi'
                if taxon == 'PB':
                    taxon = 'Plasmodium berghei'
                if taxon == 'PM':
                    taxon = 'Plasmodium malariae'

                values = {
                    'sample_oxford_id': oxford_code,
                    'sample_partner_id': source_code,
                    'species': taxon,
                    'iso2': iso2,
                    'state': state
                }

                if sheet in sheet_study_map:
                    values['study_id'] = sheet_study_map[sheet]

                item = self.process_item(values)

                if not sheet[0].isdigit() and item:
                    try:
                        self._dao.create_event_set_item(sheet, item.sampling_event_id)
                    except ApiException as err:
                        # 422 probably means already exists
                        if err.status != 422:
                            print(f'Failed to add event_set_item {err.body}')

#                print(values)
#                print(item)

                self.validate(values, item)


    def validate(self, input_values, output_values):

        if not input_values:
            return


        if not output_values:
            return

        if 'study_id' not in input_values:
            print("No study id {} {}".format(input_values, output_values))

if __name__ == '__main__':
    el = Upload_SSR(sys.argv[1])
    sheets = None
    if len(sys.argv) > 3:
        sheets = sys.argv[3]
    el.load_data_file(sys.argv[2], sheets)
