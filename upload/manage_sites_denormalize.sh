sudo cp manage_sites*.txt /var/lib/mysql-files/
mysql -u root -proot <<+++EOF
DROP SCHEMA IF EXISTS tmp;
CREATE SCHEMA tmp;
use tmp;
DROP TABLE IF EXISTS manage_sites;
CREATE TABLE manage_sites
  (id INT NOT NULL PRIMARY KEY,
    code TEXT,
    location_name TEXT,
    country_code TEXT,
    description TEXT,
    latitude TEXT,
    longitude TEXT,
    map_zoom TEXT,
    type TEXT,
    part_of_site TEXT NOT NULL);
CREATE TABLE manage_sites_samples
  (oxford_code TEXT,
    study_id TEXT,
  id INT NOT NULL PRIMARY KEY,
  site_id INT);
LOAD DATA INFILE '/var/lib/mysql-files/manage_sites.txt' INTO TABLE manage_sites IGNORE 1 LINES;
LOAD DATA INFILE '/var/lib/mysql-files/manage_sites_samples.txt' INTO TABLE manage_sites_samples IGNORE 1 LINES;
SELECT * FROM (
(select 'oxford_code', 'location_name', 'latitude', 'longitude', 'country_code', 'type', 'description' )
UNION ALL
(select oxford_code, location_name, latitude, longitude, country_code, type, description 
    from manage_sites JOIN manage_sites_samples On manage_sites_samples.site_id = manage_sites.id))
    a
    INTO OUTFILE '/var/lib/mysql-files/result.txt'
  FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n';

+++EOF
sudo mv /var/lib/mysql-files/result.txt denormalized_manage_sites.txt
