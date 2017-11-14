sudo -u postgres psql << +++EOF
DROP database backbone_service;
CREATE DATABASE backbone_service;
Alter DATABASE backbone_service OWNER TO iwright;
ALTER DATABASE backbone_service SET search_path=public, backbone_service, contrib;
\connect backbone_service;
\i backbone_service.psql;
\connect backbone_service;
SELECT postgis_full_version();
\copy countries (English, French, alpha2, alpha3, numeric_code) FROM './country_codes.tsv' DELIMITER E'\t'  HEADER CSV;
\copy taxonomies (id, rank, name) FROM './taxa.tsv' DELIMITER E'\t'  HEADER CSV;
+++EOF
