--
-- PostgreSQL database dump
--

-- Dumped from database version 10.7 (Debian 10.7-1.pgdg90+1)
-- Dumped by pg_dump version 12.1 (Ubuntu 12.1-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


SET default_tablespace = '';

--
-- Name: archive; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.archive (
    id integer NOT NULL,
    submitter character varying(64),
    action_id character varying(64),
    entity_id character varying(64),
    input_value text,
    output_value json,
    result_code integer,
    action_date timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: archive_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.archive_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: archive_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.archive_id_seq OWNED BY public.archive.id;


--
-- Name: assay_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assay_data (
    id uuid NOT NULL,
    derivative_sample_id uuid,
    acc_date date,
    ebi_run_acc character varying
);


--
-- Name: assay_datum_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assay_datum_attrs (
    assay_datum_id uuid,
    attr_id uuid
);


--
-- Name: attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.attrs (
    id uuid NOT NULL,
    study_id uuid,
    attr_type character varying(256),
    attr_value character varying(256),
    attr_source character varying(256)
);


--
-- Name: countries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.countries (
    english character varying,
    french character varying,
    alpha2 character(2),
    alpha3 character(3) NOT NULL,
    numeric_code integer
);


--
-- Name: derivative_sample_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.derivative_sample_attrs (
    derivative_sample_id uuid,
    attr_id uuid
);


--
-- Name: derivative_samples; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.derivative_samples (
    id uuid NOT NULL,
    original_sample_id uuid,
    dna_prep character varying,
    acc_date date,
    parent_derivative_sample_id uuid
);


--
-- Name: derived_sample_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.derived_sample_attrs (
    derived_sample_id uuid,
    attr_id uuid
);


--
-- Name: event_set_members; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.event_set_members (
    event_set_id integer,
    sampling_event_id uuid
);


--
-- Name: event_set_notes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.event_set_notes (
    event_set_id integer NOT NULL,
    note_name character varying(128) NOT NULL,
    note_text text
);


--
-- Name: event_sets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.event_sets (
    id integer NOT NULL,
    event_set_name character varying(128) NOT NULL
);


--
-- Name: event_sets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.event_sets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: event_sets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.event_sets_id_seq OWNED BY public.event_sets.id;


--
-- Name: expected_samples; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.expected_samples (
    id uuid NOT NULL,
    study_id uuid NOT NULL,
    partner_species_id uuid,
    sample_count integer,
    date_of_arrival date
);


--
-- Name: individual_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.individual_attrs (
    individual_id uuid,
    attr_id uuid
);


--
-- Name: individuals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.individuals (
    id uuid NOT NULL
);


--
-- Name: location_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.location_attrs (
    location_id uuid,
    attr_id uuid
);


--
-- Name: locations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.locations (
    id uuid NOT NULL,
    location public.geometry(Point),
    proxy_location_id uuid,
    country character(3),
    accuracy character varying,
    curated_name character varying,
    curation_method character varying,
    notes character varying
);


--
-- Name: original_sample_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.original_sample_attrs (
    original_sample_id uuid,
    attr_id uuid
);


--
-- Name: original_samples; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.original_samples (
    id uuid NOT NULL,
    study_id uuid,
    sampling_event_id uuid,
    partner_species_id uuid,
    acc_date date,
    days_in_culture integer
);


--
-- Name: partner_species_identifiers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.partner_species_identifiers (
    id uuid NOT NULL,
    study_id uuid,
    partner_species character varying(128)
);


--
-- Name: sampling_event_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sampling_event_attrs (
    sampling_event_id uuid,
    attr_id uuid
);


--
-- Name: sampling_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sampling_events (
    id uuid NOT NULL,
    doc date,
    doc_accuracy character varying,
    acc_date date,
    location_id uuid,
    individual_id uuid
);


--
-- Name: studies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.studies (
    id uuid NOT NULL,
    study_name character varying(64),
    study_code character varying(4),
    ethics_expiry date
);


--
-- Name: taxonomies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.taxonomies (
    id bigint NOT NULL,
    rank character varying(32),
    name character varying(128)
);


--
-- Name: taxonomy_identifiers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.taxonomy_identifiers (
    taxonomy_id bigint,
    partner_species_id uuid
);


--
-- Name: v_sampling_events; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_sampling_events AS
 SELECT sampling_events.id,
    sampling_events.doc,
    sampling_events.doc_accuracy,
    sampling_events.location_id,
    sampling_events.individual_id,
    public.st_x(loc.location) AS latitude,
    public.st_y(loc.location) AS longitude,
    loc.accuracy,
    loc.curated_name,
    loc.curation_method,
    loc.country,
    loc.notes,
    la.attr_value AS partner_name,
    loc.proxy_location_id,
    public.st_x(proxy_loc.location) AS proxy_latitude,
    public.st_y(proxy_loc.location) AS proxy_longitude,
    proxy_loc.accuracy AS proxy_accuracy,
    proxy_loc.curated_name AS proxy_curated_name,
    proxy_loc.curation_method AS proxy_curation_method,
    proxy_loc.country AS proxy_country,
    proxy_loc.notes AS proxy_notes,
    pla.attr_value AS proxy_partner_name
   FROM ((((((public.sampling_events
     LEFT JOIN public.locations loc ON ((loc.id = sampling_events.location_id)))
     LEFT JOIN public.location_attrs li ON ((li.location_id = sampling_events.location_id)))
     LEFT JOIN public.attrs la ON (((li.attr_id = la.id) AND ((la.attr_type)::text = 'partner_name'::text))))
     LEFT JOIN public.locations proxy_loc ON ((proxy_loc.id = loc.proxy_location_id)))
     LEFT JOIN public.location_attrs pli ON ((pli.location_id = loc.proxy_location_id)))
     LEFT JOIN public.attrs pla ON (((pli.attr_id = pla.id) AND ((pla.attr_type)::text = 'partner_name'::text))));


--
-- Name: archive id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.archive ALTER COLUMN id SET DEFAULT nextval('public.archive_id_seq'::regclass);


--
-- Name: event_sets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_sets ALTER COLUMN id SET DEFAULT nextval('public.event_sets_id_seq'::regclass);


--
-- Name: assay_data assay_datum_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assay_data
    ADD CONSTRAINT assay_datum_id PRIMARY KEY (id);


--
-- Name: attrs attr_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.attrs
    ADD CONSTRAINT attr_id PRIMARY KEY (id);


--
-- Name: countries countries_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_id PRIMARY KEY (alpha3);


--
-- Name: derivative_samples derivative_sample_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivative_samples
    ADD CONSTRAINT derivative_sample_id PRIMARY KEY (id);


--
-- Name: individuals individual_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.individuals
    ADD CONSTRAINT individual_id PRIMARY KEY (id);


--
-- Name: locations location_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT location_id PRIMARY KEY (id);


--
-- Name: original_samples original_sample_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.original_samples
    ADD CONSTRAINT original_sample_id PRIMARY KEY (id);


--
-- Name: partner_species_identifiers partner_species_identifiers_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partner_species_identifiers
    ADD CONSTRAINT partner_species_identifiers_id PRIMARY KEY (id);


--
-- Name: event_sets pk_es; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_sets
    ADD CONSTRAINT pk_es PRIMARY KEY (id);


--
-- Name: event_set_notes pk_esn; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_set_notes
    ADD CONSTRAINT pk_esn PRIMARY KEY (event_set_id, note_name);


--
-- Name: sampling_events sampling_event_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sampling_events
    ADD CONSTRAINT sampling_event_id PRIMARY KEY (id);


--
-- Name: studies studies_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.studies
    ADD CONSTRAINT studies_id PRIMARY KEY (id);


--
-- Name: taxonomies taxonomy_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.taxonomies
    ADD CONSTRAINT taxonomy_id PRIMARY KEY (id);


--
-- Name: event_set_members uniq_event_set_members; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_set_members
    ADD CONSTRAINT uniq_event_set_members UNIQUE (event_set_id, sampling_event_id);


--
-- Name: event_sets uniq_event_sets; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_sets
    ADD CONSTRAINT uniq_event_sets UNIQUE (event_set_name);


--
-- Name: studies uniq_study_code; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.studies
    ADD CONSTRAINT uniq_study_code UNIQUE (study_code);


--
-- Name: attrs_attr_source_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX attrs_attr_source_idx ON public.attrs USING btree (attr_source);


--
-- Name: attrs_attr_type_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX attrs_attr_type_idx ON public.attrs USING btree (attr_type, attr_value);


--
-- Name: event_set_members_sampling_event_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_set_members_sampling_event_id_idx ON public.event_set_members USING btree (sampling_event_id);


--
-- Name: fki_fk_esm_es; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_fk_esm_es ON public.event_set_members USING btree (event_set_id);


--
-- Name: fki_fk_esm_se; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_fk_esm_se ON public.event_set_members USING btree (sampling_event_id);


--
-- Name: fki_fk_esn_es; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_fk_esn_es ON public.event_set_notes USING btree (event_set_id);


--
-- Name: fki_individual; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_individual ON public.sampling_events USING btree (individual_id);


--
-- Name: fki_individual_attr_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_individual_attr_id ON public.individual_attrs USING btree (attr_id);


--
-- Name: fki_individual_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_individual_id ON public.individual_attrs USING btree (individual_id);


--
-- Name: fki_location; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_location ON public.sampling_events USING btree (location_id);


--
-- Name: fki_location_attr_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_location_attr_id ON public.location_attrs USING btree (attr_id);


--
-- Name: fki_location_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_location_id ON public.location_attrs USING btree (location_id);


--
-- Name: fki_proxy_location; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_proxy_location ON public.locations USING btree (proxy_location_id);


--
-- Name: fki_sampling_event_attr_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_sampling_event_attr_id ON public.sampling_event_attrs USING btree (attr_id);


--
-- Name: fki_sampling_event_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_sampling_event_id ON public.sampling_event_attrs USING btree (sampling_event_id);


--
-- Name: idx_ident_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ident_type ON public.attrs USING btree (attr_type);


--
-- Name: idx_ident_value; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ident_value ON public.attrs USING btree (attr_value);


--
-- Name: idx_partner_species; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_partner_species ON public.partner_species_identifiers USING btree (partner_species);


--
-- Name: idx_se_doc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_se_doc ON public.sampling_events USING btree (doc);


--
-- Name: idx_study_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_study_id ON public.studies USING btree (id);


--
-- Name: idx_study_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_study_name ON public.studies USING btree (study_name);


--
-- Name: individual_attrs_individual_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX individual_attrs_individual_id_idx ON public.individual_attrs USING btree (individual_id);


--
-- Name: location_attrs_location_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX location_attrs_location_id_idx ON public.location_attrs USING btree (location_id);


--
-- Name: original_sample_attrs_original_sample_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX original_sample_attrs_original_sample_id_idx ON public.original_sample_attrs USING btree (original_sample_id);


--
-- Name: partner_species_identifiers_partner_species_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX partner_species_identifiers_partner_species_idx ON public.partner_species_identifiers USING btree (partner_species);


--
-- Name: studies_study_code_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX studies_study_code_idx ON public.studies USING btree (study_code);


--
-- Name: assay_datum_attrs assay_datum_attrs_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assay_datum_attrs
    ADD CONSTRAINT assay_datum_attrs_fk FOREIGN KEY (attr_id) REFERENCES public.attrs(id);


--
-- Name: derivative_sample_attrs derivative_sample_attrs_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivative_sample_attrs
    ADD CONSTRAINT derivative_sample_attrs_fk FOREIGN KEY (attr_id) REFERENCES public.attrs(id);


--
-- Name: derivative_samples derivative_samples_derivative_samples_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivative_samples
    ADD CONSTRAINT derivative_samples_derivative_samples_fk FOREIGN KEY (parent_derivative_sample_id) REFERENCES public.derivative_samples(id);


--
-- Name: assay_data fk_ad_ds; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assay_data
    ADD CONSTRAINT fk_ad_ds FOREIGN KEY (derivative_sample_id) REFERENCES public.derivative_samples(id);


--
-- Name: assay_datum_attrs fk_assay_datum; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assay_datum_attrs
    ADD CONSTRAINT fk_assay_datum FOREIGN KEY (assay_datum_id) REFERENCES public.assay_data(id);


--
-- Name: locations fk_country; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT fk_country FOREIGN KEY (country) REFERENCES public.countries(alpha3);


--
-- Name: derivative_sample_attrs fk_derivative_sample; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivative_sample_attrs
    ADD CONSTRAINT fk_derivative_sample FOREIGN KEY (derivative_sample_id) REFERENCES public.derivative_samples(id);


--
-- Name: derivative_samples fk_ds_os; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivative_samples
    ADD CONSTRAINT fk_ds_os FOREIGN KEY (original_sample_id) REFERENCES public.original_samples(id);


--
-- Name: expected_samples fk_es_psi; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.expected_samples
    ADD CONSTRAINT fk_es_psi FOREIGN KEY (partner_species_id) REFERENCES public.partner_species_identifiers(id);


--
-- Name: expected_samples fk_es_si; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.expected_samples
    ADD CONSTRAINT fk_es_si FOREIGN KEY (study_id) REFERENCES public.studies(id);


--
-- Name: event_set_members fk_esm_es; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_set_members
    ADD CONSTRAINT fk_esm_es FOREIGN KEY (event_set_id) REFERENCES public.event_sets(id);


--
-- Name: event_set_members fk_esm_se; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_set_members
    ADD CONSTRAINT fk_esm_se FOREIGN KEY (sampling_event_id) REFERENCES public.sampling_events(id);


--
-- Name: event_set_notes fk_esn_es; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_set_notes
    ADD CONSTRAINT fk_esn_es FOREIGN KEY (event_set_id) REFERENCES public.event_sets(id);


--
-- Name: sampling_events fk_individual; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sampling_events
    ADD CONSTRAINT fk_individual FOREIGN KEY (individual_id) REFERENCES public.individuals(id);


--
-- Name: individual_attrs fk_individual; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.individual_attrs
    ADD CONSTRAINT fk_individual FOREIGN KEY (individual_id) REFERENCES public.individuals(id);


--
-- Name: individual_attrs fk_individual_attr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.individual_attrs
    ADD CONSTRAINT fk_individual_attr FOREIGN KEY (attr_id) REFERENCES public.attrs(id);


--
-- Name: sampling_events fk_location; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sampling_events
    ADD CONSTRAINT fk_location FOREIGN KEY (location_id) REFERENCES public.locations(id);


--
-- Name: location_attrs fk_location; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.location_attrs
    ADD CONSTRAINT fk_location FOREIGN KEY (location_id) REFERENCES public.locations(id);


--
-- Name: location_attrs fk_location_attr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.location_attrs
    ADD CONSTRAINT fk_location_attr FOREIGN KEY (attr_id) REFERENCES public.attrs(id);


--
-- Name: original_sample_attrs fk_original_sample; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.original_sample_attrs
    ADD CONSTRAINT fk_original_sample FOREIGN KEY (original_sample_id) REFERENCES public.original_samples(id);


--
-- Name: original_samples fk_os_psi; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.original_samples
    ADD CONSTRAINT fk_os_psi FOREIGN KEY (partner_species_id) REFERENCES public.partner_species_identifiers(id);


--
-- Name: original_samples fk_os_se; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.original_samples
    ADD CONSTRAINT fk_os_se FOREIGN KEY (sampling_event_id) REFERENCES public.sampling_events(id);


--
-- Name: original_samples fk_os_study; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.original_samples
    ADD CONSTRAINT fk_os_study FOREIGN KEY (study_id) REFERENCES public.studies(id);


--
-- Name: taxonomy_identifiers fk_partner_sp; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.taxonomy_identifiers
    ADD CONSTRAINT fk_partner_sp FOREIGN KEY (partner_species_id) REFERENCES public.partner_species_identifiers(id);


--
-- Name: partner_species_identifiers fk_partner_sp_study; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partner_species_identifiers
    ADD CONSTRAINT fk_partner_sp_study FOREIGN KEY (study_id) REFERENCES public.studies(id);


--
-- Name: locations fk_proxy_location; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT fk_proxy_location FOREIGN KEY (proxy_location_id) REFERENCES public.locations(id);


--
-- Name: sampling_event_attrs fk_sampling_event; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sampling_event_attrs
    ADD CONSTRAINT fk_sampling_event FOREIGN KEY (sampling_event_id) REFERENCES public.sampling_events(id);


--
-- Name: sampling_event_attrs fk_sampling_event_attr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sampling_event_attrs
    ADD CONSTRAINT fk_sampling_event_attr FOREIGN KEY (attr_id) REFERENCES public.attrs(id);


--
-- Name: attrs fk_study_loc; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.attrs
    ADD CONSTRAINT fk_study_loc FOREIGN KEY (study_id) REFERENCES public.studies(id);


--
-- Name: taxonomy_identifiers fk_taxa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.taxonomy_identifiers
    ADD CONSTRAINT fk_taxa FOREIGN KEY (taxonomy_id) REFERENCES public.taxonomies(id);


--
-- Name: original_sample_attrs original_sample_attrs_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.original_sample_attrs
    ADD CONSTRAINT original_sample_attrs_fk FOREIGN KEY (attr_id) REFERENCES public.attrs(id);


--
-- PostgreSQL database dump complete
--

