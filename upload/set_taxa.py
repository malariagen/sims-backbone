from __future__ import print_function
import json
import csv
import re
import time
import datetime
import logging
import sys
import swagger_client
from swagger_client.rest import ApiException

from decimal import *

import urllib.parse
from copy import deepcopy

from pprint import pprint

import os
import requests


class SetTaxa():


    _taxa_map = {}
    _auth_token = {}
    _api_client = None

    def __init__(self, config):
        configuration = swagger_client.Configuration()
        configuration.access_token = self._auth_token
        self._api_client = swagger_client.ApiClient(configuration)

    def load_taxa_map(self):

        input_stream = open('taxon_mapping.csv')

        with input_stream as csvfile:
            data_reader = csv.reader(csvfile)

            for row in data_reader:
                taxas = []
                for taxa in row[6].split(';'):
                    taxas.append(swagger_client.Taxonomy(taxonomy_id=int(taxa)))

                self._taxa_map[row[0]] = taxas

    def set_taxa(self):

        study_api = swagger_client.StudyApi(self._api_client)

        studies = study_api.download_studies()

        update = False
        for study in studies.studies:
            study_detail = study_api.download_study(study.code)
            for species in study_detail.partner_species:
                if species.partner_species in self._taxa_map:
                    taxa = self._taxa_map[species.partner_species]
                    #print("Setting taxa for {} to {} from {}".format(species.partner_species, taxa, species.taxa))
                    species.taxa = taxa
                    update = True
                else:
                    #print("No mapping for species {} {}".format(species.partner_species, study_detail))
                    pass

            if update:
                #print(study_detail)
                study_api.update_study(study.code, study_detail)


if __name__ == '__main__':
    sd = SetTaxa(sys.argv[1])
    sd.load_taxa_map()
    sd.set_taxa()

