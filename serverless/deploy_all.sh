#!/bin/bash

if [ "$1" = "" ]
then
    STAGE=dev
else
    STAGE=$1
fi
for i in ./sims-backbone-service ./assay_data_service ./event_set_service ./sampling_event_service ./report_service ./original_sample_service ./derivative_sample_service ./location_service
do
    (cd $i;sls deploy --stage ${STAGE})
done
