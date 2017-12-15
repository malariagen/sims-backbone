sudo cp pv_3_*.txt /var/lib/mysql-files/
sudo cp pf_6_*.txt /var/lib/mysql-files/
mysql -u root -proot <<+++EOF
DROP SCHEMA IF EXISTS tmp;
CREATE SCHEMA tmp;
use tmp;
DROP TABLE IF EXISTS pv_3_locations;
CREATE TABLE pv_3_locations
(id TEXT,
    country TEXT,
    location TEXT,
    public_id TEXT,
    public_location TEXT);
CREATE TABLE pv_3_sanger_source_code_metadata
  ( study_id TEXT,
  oxford_src_code TEXT,
  oxford_donor_code TEXT,
  related_src_code TEXT,
  relationship TEXT,
  blood_draw_id TEXT,
  individual_id TEXT,
  collection_date TEXT,
  collection_location TEXT);
CREATE TABLE pv_3_broad_metadata
  ( partner_id TEXT,
  blood_draw_id TEXT,
  individual_id TEXT,
  collection_date TEXT,
  year_of_collection TEXT,
  collection_location TEXT);
CREATE TABLE oxford
  ( oxf_database TEXT,
  individual_id TEXT,
  Oxford_db_id_source_code TEXT,
  oxford_db_id_sample_code TEXT,
  oxford_db_id_sample_id TEXT,
  oxford_db_id_alternate_id1 TEXT,
  UNIQUE_SAMPLE_ID TEXT);
CREATE TABLE solaris
  ( oxford_code TEXT,
  study_group TEXT,
  alfresco TEXT,
  name TEXT);
CREATE TABLE pf_6_metadata
  ( oxford_code TEXT,
  oxford_src_code TEXT,
  oxford_donor_code TEXT,
  individual_id TEXT,
  study_id TEXT,
  type TEXT,
  location_name TEXT,
  latitude TEXT,
  longitude TEXT,
  doc TEXT,
  collection_year TEXT,
  release_exclusion_reason TEXT);
LOAD DATA INFILE '/var/lib/mysql-files/pv_3_locations.txt' INTO TABLE pv_3_locations IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/pv_3_locations.txt' INTO TABLE pv_3_locations IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/pv_3_sanger_source_code_metadata.txt' INTO TABLE pv_3_sanger_source_code_metadata IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/pv_3_broad_metadata.txt' INTO TABLE pv_3_broad_metadata IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/oxford.txt' INTO TABLE oxford IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/vw_vrpipe.txt' INTO TABLE solaris IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/pf_6_metadata.txt' INTO TABLE pf_6_metadata IGNORE 1 LINES;
CREATE OR REPLACE VIEW samples AS
    SELECT oxford.oxford_db_id_sample_code as sample_oxford_id, oxford.Oxford_db_id_source_code as
    sample_partner_id, solaris.alfresco as study_id, substring(solaris.alfresco,1, 4) as study_code FROM oxford
    LEFT JOIN solaris ON solaris.oxford_code = oxford.oxford_db_id_sample_code;
SELECT 'oxford_code', 'study_id', 'oxford_src_code','location_name', 'location', 'country',
    'proxy_location_name', 'public_location', 'collection_date', 'location_name', 'latitude',
    'longitude', 'doc'
    union
select DISTINCT IFNULL(samples.sample_oxford_id,pf_6_metadata.oxford_code),
        IFNULL(samples.study_id, IFNULL(pf_6_metadata.study_id,
        pv_3_sanger_source_code_metadata.study_id)), pv_3_sanger_source_code_metadata.oxford_src_code as sample_partner_id,
    id as location_name, location, country, 
    public_id as proxy_location_name, public_location, collection_date,
    pf_6_metadata.location_name, pf_6_metadata.latitude, pf_6_metadata.longitude, pf_6_metadata.doc
    INTO OUTFILE '/var/lib/mysql-files/result.txt'
  FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    from pv_3_sanger_source_code_metadata 
        LEFT JOIN pv_3_locations On pv_3_sanger_source_code_metadata.collection_location = pv_3_locations.id
        LEFT JOIN samples ON pv_3_sanger_source_code_metadata.oxford_src_code = samples.sample_partner_id AND pv_3_sanger_source_code_metadata.study_id = samples.study_code
        LEFT JOIN pf_6_metadata ON pv_3_sanger_source_code_metadata.oxford_src_code =
        pf_6_metadata.oxford_src_code AND pv_3_sanger_source_code_metadata.study_id = substring(pf_6_metadata.study_id,1,4)
   ;
+++EOF
sudo mv /var/lib/mysql-files/result.txt pv_3.denormalized.txt
