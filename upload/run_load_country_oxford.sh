#!/bin/bash
./setup_import.sh
source environment_local
python3 set_country.py ${IMPORT_CONFIG} oxford_id $1 3 10 $2
