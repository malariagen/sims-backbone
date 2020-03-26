#!/bin/bash
./setup_import.sh
source environment_local
python3 uploader.py $1 $2 ${IMPORT_CONFIG} $3 $4
