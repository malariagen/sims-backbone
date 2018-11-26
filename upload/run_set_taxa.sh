#!/bin/bash
./setup_import.sh
source environment_local
python3 set_taxa.py ${IMPORT_CONFIG}
