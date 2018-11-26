#!/bin/bash
./setup_import.sh
source environment_local
pip3 install git+https://github.com/idwright/chemistry-cmislib.git
python3 set_studies.py ${IMPORT_CONFIG} cmis_config.json
