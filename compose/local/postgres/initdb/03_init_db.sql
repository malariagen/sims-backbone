\copy countries (English, French, alpha2, alpha3, numeric_code) FROM '/docker-entrypoint-initdb.d/country_codes.tsv' DELIMITER E'\t'  HEADER CSV;
\copy taxonomies (id, rank, name) FROM '/docker-entrypoint-initdb.d/taxa.tsv' DELIMITER E'\t'  HEADER CSV;
