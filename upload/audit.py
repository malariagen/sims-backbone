import json
import os
import sys
import datetime
import logging

import requests

from cmislib import CmisClient
import openapi_client

from remote_backbone_dao import RemoteBackboneDAO
from local_backbone_dao import LocalBackboneDAO

class AuditStudies():


    _auth_token = ''
    _api_client = None

    def __init__(self, config_file, cmis_config):

        self._logger = logging.getLogger(__name__)
        self.get_cmis_client(cmis_config)

        self._dao = RemoteBackboneDAO()

        if os.getenv('LOCAL_TEST'):
            self._dao = LocalBackboneDAO('upload_test',
                                         [
                                             'cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net',
                                             'cn=all_studies,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net'
                                         ])

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
                                    self._logger.debug('Using database {}'.format(os.getenv('POSTGRES_DB','backbone_service')))
                                    self._dao = LocalBackboneDAO(args['username'], args['auths'])
        except FileNotFoundError as fnfe:
            print('No config file found: {}'.format(config_file))

        self._dao.setup(config_file)

    def get_cmis_client(self, config_file):

        with open(config_file) as json_file:
            config = json.load(json_file)

        self.cmis_client = CmisClient(config['endpoint'], config['username'], config['password'])
        self.repo = self.cmis_client.defaultRepository

    def check_studies(self):

        studies = self._dao.download_studies()

        studies_dict = {}
        for study in studies.studies:
            studies_dict[study.code] = study

        results = self.repo.query('''select * from cggh:collaborationFolder f
                                  JOIN cggh:collaboration AS c ON f.cmis:objectId = c.cmis:objectId
                                  JOIN cggh:collaborationData AS cd ON f.cmis:objectId = cd.cmis:objectId''')

        for result in results:
            code = result.getName()[:4]
            if code in studies_dict:
                study_detail = self._dao.download_study(code)
                #print(study_detail)
                #print(result.properties)
                self.check_countries(result, study_detail)
                self.check_species(result, study_detail)



    def check_species(self, result, study_detail):

        alf_species = []
        sims_species = []
        if 'cggh:species' in result.properties:
            props = result.properties['cggh:species']
            if isinstance(props, str):
                alf_species.append(props)
            elif props:
                alf_species = props

            for species in study_detail.partner_species:
                for taxa in species.taxa:
                    t_name = taxa.name
                    if taxa.name == 'Plasmodium falciparum':
                        t_name = 'P. falciparum'
                    if taxa.name == 'Plasmodium vivax':
                        t_name = 'P. vivax'
                    if taxa.name == 'Anopheles gambiae' or taxa.name == 'gambiae species complex':
                        t_name = 'A. gambiae'
                    if t_name not in sims_species:
                        sims_species.append(t_name)

        for species in sims_species:
            if species not in alf_species:
                #print(result.properties['cggh:species'])
                #print(study_detail.partner_species)
                print(f'{result.name} {species} not in Alfresco')

        for species in alf_species:
            if species not in sims_species:
                #print(result.properties['cggh:species'])
                #print(study_detail.partner_species)
                print(f'{result.name} No samples from {species}')



    def check_countries(self, result, study_detail):
        iso3_alf_countries = []
        if 'cggh:sampleCountry' in result.properties:
            alf_countries = []
            props = result.properties['cggh:sampleCountry']
            if isinstance(props, str):
                alf_countries.append(props)
            else:
                alf_countries = props

            if alf_countries:
                for country in alf_countries:
                    if country == 'GAMBIA':
                        iso3_alf_countries.append('GMB')
                    elif country == 'PHILIPPINES':
                        iso3_alf_countries.append('PHL')
                    elif country == 'SUDAN':
                        iso3_alf_countries.append('SDN')
                    elif country == 'CENTRAL AFRICAN REPUBLIC':
                        iso3_alf_countries.append('CAF')
                    elif country == 'CONGO':
                        iso3_alf_countries.append('COG')
                    elif country == 'TANZANIA (UNITED REPUBLIC OF)':
                        iso3_alf_countries.append('TZA')
                    elif country == "LAO PEOPLE'S DEMOCRATIC REPUBLIC":
                        iso3_alf_countries.append('LAO')
                    else:
                        metadata = self._dao.get_country_metadata(country)
                        iso3_alf_countries.append(metadata.alpha3)

        sims_countries = []
        for loc in study_detail.locations.locations:
            if loc.country not in sims_countries:
                sims_countries.append(loc.country)
        for country in sims_countries:
            if country not in iso3_alf_countries:
                print(f'{result.name} {country} not in Alfresco')

        for country in iso3_alf_countries:
            if country not in sims_countries:
                print(f'{result.name} No samples from {country}')




if __name__ == '__main__':
    studies_setter = AuditStudies(sys.argv[1], sys.argv[2])
    studies_setter.check_studies()
