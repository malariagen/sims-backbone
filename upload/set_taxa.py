import os
import json
import csv
import datetime
import logging
import sys
import openapi_client
from openapi_client.rest import ApiException

from remote_backbone_dao import RemoteBackboneDAO
from local_backbone_dao import LocalBackboneDAO


class SetTaxa():


    _auth_token = ''
    _api_client = None

    def __init__(self, config_file):
        self._logger = logging.getLogger(__name__)
        self._dao = RemoteBackboneDAO()

        if os.getenv('LOCAL_TEST'):
            self._dao = LocalBackboneDAO('upload_test',
                                         ['cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net',
                                          'cn=all_studies,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net'])

        self._config_file = config_file

        try:
            with open(config_file) as json_file:
                args = json.load(json_file)
                if 'debug' in args:
                    if args['debug']:
                        log_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
                        log_file = 'uploader_{}.log'.format(log_time)
                        print("Debugging to {}".format(log_file))
                        logging.basicConfig(level=logging.DEBUG, filename=log_file)
                if 'dao_type' in args:
                    if args['dao_type'] == 'local':
                        if 'database' in args:
                            os.environ['POSTGRES_DB'] = args['database']
                        self._logger.debug('Using database %s', os.getenv('POSTGRES_DB', 'backbone_service'))
                        self._dao = LocalBackboneDAO(args['username'], args['auths'])
        except FileNotFoundError as fnfe:
            self._logger.fatal('No config file found: %s', config_file)
            pass

        self._dao.setup(config_file)
        self._taxa_map = {}

    def load_taxa_map(self):

        input_stream = open('taxon_mapping.csv')

        with input_stream as csvfile:
            data_reader = csv.reader(csvfile)

            for row in data_reader:
                taxas = []
                for taxa in row[6].split(';'):
                    taxas.append(openapi_client.Taxonomy(taxonomy_id=int(taxa)))

                self._taxa_map[row[0]] = taxas

    def set_taxa(self):

        studies = self._dao.download_studies()

        update = False
        for study in studies.studies:
            study_detail = self._dao.download_study(study.code)
            if not study_detail.partner_species:
                study_detail.partner_species = []
            for species in study_detail.partner_species:
                if species.partner_species in self._taxa_map:
                    taxas = self._taxa_map[species.partner_species]
                    for taxa in taxas:
                        found = False
                        if species.taxa:
                            for st in species.taxa:
                                if int(taxa.taxonomy_id) == int(st.taxonomy_id):
                                    found = True
                        if not found:
                            print("In study {} Setting taxa for {} to {} from {}".format(study.code,
                                                                                         species.partner_species,
                                                                                         taxas, species.taxa))
                            species.taxa = taxas
                            update = True
                else:
                    #print("No mapping for species {} {}".format(species.partner_species, study_detail))
                    pass

            if update:
                #print(study_detail)
                self._dao.update_study(study.code, study_detail)


if __name__ == '__main__':
    sd = SetTaxa(sys.argv[1])
    sd.load_taxa_map()
    sd.set_taxa()
