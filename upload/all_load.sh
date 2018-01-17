./run.sh oxford.csv oxford.json
./runsss.sh 2017_06_07_report_sample_status.xls
./run.sh pf_6_metadata.txt pf_6_metadata.json
./run.sh pv_3.denormalized.txt pv_3_sanger_source_code_metadata.json
./run.sh pv_3_broad_metadata.txt pv_3_broad_metadata.json
for i in ../../ROMA_Deploy/data/genre_dump.20180116103346.json ../../ROMA_Deploy/data/vivax_dump.20180116103346.json ../../ROMA_Deploy/data/spotmalaria_dump.20180116103346.json ../../ROMA_Deploy/data/vobs_dump.20180116103346.json
do
    ./run_roma.sh $i
done
./run.sh ag1000g.samples.meta.txt ag1000g.json
./run_load_country_oxford.sh
./run.sh manage_sites.denormalized.txt denorm_manage_sites.json
