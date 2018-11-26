#!/bin/bash
./setup_import.sh
source environment_local
python3 uploader.py $1 $2 $3 ${IMPORT_CONFIG}
