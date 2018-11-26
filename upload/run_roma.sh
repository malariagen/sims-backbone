#!/bin/bash
./setup_import.sh
source environment_local
python3 upload_roma.py ${IMPORT_CONFIG} $1 $2
