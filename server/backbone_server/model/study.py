import os

from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, Text, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import text
from sqlalchemy.types import ARRAY

from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy import event, and_

from openapi_server.models.study import Study as ApiStudy
from openapi_server.models.studies import Studies as ApiStudies
from openapi_server.models.partner_species import PartnerSpecies
from openapi_server.models.taxonomy import Taxonomy as ApiTaxonomy
from openapi_server.models.batch import Batch as ApiBatch

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.model.history_meta import Versioned
from backbone_server.model.base import SimsDbBase
from backbone_server.model.mixins import Base
from backbone_server.model.country import Country


class Taxonomy(Base):

    id = Column(Integer(), primary_key=True)
    rank = Column(String(32))
    name = Column(String(128))

    @staticmethod
    def get_or_create(db, tid, user):

        taxa = db.query(Taxonomy).filter_by(id=tid).first()

        if taxa is None:
            taxa = Taxonomy(id=tid)
            db.add(taxa)
            db.commit()
            taxa = db.query(Taxonomy).filter_by(id=tid).first()

        return taxa

    openapi_class = ApiTaxonomy

    def __repr__(self):
        return f'''<Taxonomy ID {self.id}
    Rank {self.rank}
    Name {self.name}
    >'''


@event.listens_for(Taxonomy.__table__, "after_create")
def insert_taxa(mapper, connection, checkfirst, _ddl_runner,
                _is_metadata_operation):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'data', 'taxa.tsv')

    with connection.connection.cursor() as cur:
        with open(file_path) as fp:
            fp.readline()
            # Default sep is tab
            cur.copy_from(fp, 'taxonomy', columns=('id', 'rank', 'name'))
    connection.connection.commit()

taxonomy_identifier_table = Table('taxonomy_identifier', Base.metadata,
                                  Column('taxonomy_id', Integer(), ForeignKey('taxonomy.id')),
                                  Column('partner_species_identifier_id', UUID(as_uuid=True), ForeignKey('partner_species_identifier.id'))
                                  )

class PartnerSpeciesIdentifier(Base, Versioned):
    @declared_attr
    def __tablename__(cls):
        return 'partner_species_identifier'

    partner_species = Column(String(128))
    study_id = Column('study_id',
                      UUID(as_uuid=True),
                      ForeignKey('study.id'))
    taxa = relationship('Taxonomy',
                        secondary=taxonomy_identifier_table)

    openapi_class = PartnerSpecies

    @staticmethod
    def get_or_create(db, partner_species, study_id, user=None):
        ps_item_query = db.query(PartnerSpeciesIdentifier).\
                            filter(and_(PartnerSpeciesIdentifier.partner_species == partner_species,
                                        PartnerSpeciesIdentifier.study_id == study_id))
        ps_item = ps_item_query.first()

        if not ps_item:
            ps_item = PartnerSpeciesIdentifier(partner_species=partner_species,
                                               study_id=study_id,
                                               created_by=user)
            db.add(ps_item)

        return ps_item

    def submapped_items(self):
        return {
            'taxa': Taxonomy,
        }
    def __repr__(self):
        return f'''<PartnerSpeciesIdentifier ID {self.id}
    Study Id {self.study_id}
    Partner Species {self.partner_species}
    {self.taxa}
    >'''

class Batch(Base, Versioned):

    sample_count = Column(Integer())
    expected_sample_count = Column(Integer())
    expected_date_of_arrival = Column(DateTime())
    date_of_arrival = Column(DateTime())
    study_id = Column('study_id',
                      UUID(as_uuid=True),
                      ForeignKey('study.id'))
    partner_species_id = Column('partner_species_id',
                                UUID(as_uuid=True),
                                ForeignKey('partner_species_identifier.id'))
    partner_species = relationship("PartnerSpeciesIdentifier",
                                   backref=backref("batch",
                                                   uselist=True))
    description = Column(Text())
    source = Column(Text())
    shipment_notes = Column(Text())

    @staticmethod
    def get_or_create(db, e_sample, study_id, user):

        expected_sample = None
        if e_sample is None or e_sample.batch_id is None:
            expected_sample = Batch(sample_count=e_sample.sample_count,
                                              date_of_arrival=e_sample.date_of_arrival,
                                              study_id=study_id,
                                              created_by=user)
            psi = PartnerSpeciesIdentifier.get_or_create(db,
                                                         e_sample.expected_species,
                                                         study_id, user)
            expected_sample.partner_species_id = psi.id
            expected_sample.partner_species = psi
            db.add(expected_sample)
            db.commit()
        else:
            expected_sample = db.query(Batch).filter_by(id=e_sample.expected_sample_id).first()
            expected_sample.sample_count = e_sample.sample_count
            expected_sample.date_of_arrival = e_sample.date_of_arrival
            expected_sample.study_id = study_id
            psi = PartnerSpeciesIdentifier.get_or_create(db,
                                                         e_sample.expected_species,
                                                         study_id, user)
            expected_sample.partner_species_id = psi.id
            expected_sample.partner_species = psi

        return expected_sample

    openapi_class = ApiBatch

    def submapped_items(self):
        return {
            'partner_species': PartnerSpeciesIdentifier,
            'study_name': 'study'
        }

    def __repr__(self):
        return f'''<Batch ID {self.id}
    Study {self.study_id}
    Partner Species {self.partner_species}
    Partner Species Id {self.partner_species_id}
    {self.sample_count}
    {self.date_of_arrival}
    >'''

class StudyCountry(Base):

    __tablename__ = 'study_country'

    id = None
    created_by = None
    updated_by = None
    action_date = None

    study_id = Column(UUID(as_uuid=True),
                      ForeignKey('study.id'),
                      primary_key=True)
    country_id = Column(String(3),
                        ForeignKey('country.alpha3'), primary_key=True)


class Study(Base, Versioned):

    name = Column(String(64), index=True, unique=True)
    title = Column(String())
    status = Column(String(16), index=True)
    rag_status = Column(String(8), index=True)
    code = Column(String(4), index=True, unique=True)
    sequencescape_code = Column(ARRAY(String(64)), index=True)
    legacy_id = Column(String(16))
    web_study = Column('web_study',
                       UUID(as_uuid=True),
                       ForeignKey('study.id'),
                       index=True)
    ethics_expiry = Column(Date())
    study_ethics = Column(String())
    web_title = Column(String())
    web_title_approved = Column(Boolean())
    description = Column(String())
    description_approved = Column(Boolean())
    notes = Column(String())
    sample_types = Column(String(32))

#    documents = relationship("Document")
    partner_species = relationship('PartnerSpeciesIdentifier',
                                   backref=backref('study', uselist=True))
    batches = relationship("Batch", backref=backref("study", uselist=True))
    countries = relationship("Country",
                             secondary=StudyCountry.__table__)
    @staticmethod
    def get_or_create_study(db, study_name, user):

        study = db.query(Study).filter_by(code=study_name[:4]).first()

        if study is None:
            study = Study(name=study_name, code=study_name[:4], created_by=user)
            db.add(study)
            db.commit()
            study = db.query(Study).filter_by(code=study_name[:4]).first()

        return study

    openapi_class = ApiStudy
    openapi_multiple_class = ApiStudies

    def openapi_map_actions(self, api_item):
        # print('openapi_map_actions')
        # print(api_item)
        db_item = self
        # print(db_item)

        api_item.partner_species = []
        for psi in db_item.partner_species:
            ps_item = psi.map_to_openapi()
            ps_item.partner_taxonomies = []

            if not ps_item.taxa:
                ps_item.taxa = []
            api_item.partner_species.append(ps_item)
        if api_item.batches:
            # print(api_item.batches)
            for es in api_item.batches:
                for db_es in db_item.batches:
                    # print(f'db_es {db_es}')
                    if str(db_es.id) == es.batch_id:
                        ps_item = PartnerSpecies()
                        if not db_es.partner_species:
                            db_es.partner_species = PartnerSpeciesIdentifier()
                        ps_item = db_es.partner_species.map_to_openapi()
                        ps_item.partner_taxonomies = []

                        if not ps_item.taxa:
                            ps_item.taxa = []
                        es.expected_species = ps_item.partner_species
                        es.expected_taxonomies = ps_item.taxa
        # print(f'Study openapi_map_actions {api_item}')

    def submapped_items(self):
        return {
            'partner_species': PartnerSpeciesIdentifier,
            'batches': Batch,
            'countries': None
        }

    def __repr__(self):
        return f'''<Study {self.name} {self.code}
    {self.partner_species}
    {self.batches}
    {self.ethics_expiry}
    {self.countries}
    >'''

class BaseStudy(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=[
            'study',
            'partner_species_identifier'
        ])

        self.db_class = Study

    def convert_to_id(self, db, item_id):

        db_item = db.query(self.db_class).filter_by(code=item_id[:4]).first()
        if not db_item:
            raise MissingKeyException(f'No such study {item_id}')

        item_id = db_item.id

        return item_id

    def convert_from_id(self, db, item_id):

        db_item = db.query(self.db_class.code).filter_by(id=item_id).first()

        return db_item

    def order_by(self):

        return self.db_class.code

    def db_map_countries(self, db, db_item, api_item, user):
        if hasattr(api_item, 'countries') and api_item.countries:
            countries = []
            for country in api_item.countries:
                if country.alpha3 in countries:
                    raise DuplicateKeyException(f'Error duplicate country {country}')
                countries.append(country.alpha3)
                db_country = db.query(Country).filter_by(alpha3=country.alpha3).first()
                if db_country not in db_item.countries:
                    db_item.countries.append(db_country)
            if countries:
                countries_to_remove = []
                for country in db_item.countries:
                    if country.alpha3 not in countries:
                        countries_to_remove.append(country)
                for country in countries_to_remove:
                    db_item.countries.remove(country)
        elif hasattr(db_item, 'countries'):
            countries_to_remove = []
            for country in db_item.countries:
                countries_to_remove.append(country)
            for country in countries_to_remove:
                db_item.countries.remove(country)

    def db_map_expected_samples(self, db, db_item, api_item, user):
        if hasattr(api_item, 'batches') and api_item.batches:
            new_batches = []
            for expected_sample in api_item.batches:
                db_expected_sample = Batch.get_or_create(db,
                                                                   expected_sample,
                                                                   db_item.id,
                                                                   user=user)
                if db_expected_sample in new_batches:
                    raise DuplicateKeyException(f'Error duplicate expected_sample {expected_sample}')
                new_batches.append(db_expected_sample)
            # [] or None
            if new_batches:
                db_item.batches.extend(new_batches)
            expected_sample_to_remove = []
            for expected_sample in db_item.batches:
                if expected_sample not in new_batches:
                    expected_sample_to_remove.append(expected_sample)
            for expected_sample in expected_sample_to_remove:
                db_item.batches.remove(expected_sample)
                delete_item = db.query(Batch).get(expected_sample.id)
                db.delete(delete_item)
        elif hasattr(db_item, 'batches'):
            expected_sample_to_remove = []
            for expected_sample in db_item.batches:
                expected_sample_to_remove.append(expected_sample)
            for expected_sample in expected_sample_to_remove:
                db_item.batches.remove(expected_sample)
                delete_item = db.query(Batch).get(expected_sample.id)
                db.delete(delete_item)

    def db_map_partner_species(self, db, db_item, api_item, user):

        for ps in api_item.partner_species:
            found = False
            for db_ps in db_item.partner_species:
                if db_ps.partner_species == ps.partner_species:
                    found = True
                    taxa_found = False
                    missing_taxa = []
                    all_taxa = []
                    remove_taxa = []
                    if ps.taxa:
                        for taxa in ps.taxa:
                            for db_taxa in db_ps.taxa:
                                if db_taxa not in all_taxa:
                                    all_taxa.append(db_taxa)
                                if db_taxa.id == taxa.taxonomy_id:
                                    taxa_found = True
                            if not taxa_found:
                                new_taxa = db.query(Taxonomy).get(taxa.taxonomy_id)
                                if not new_taxa:
                                    raise MissingKeyException(f'No such taxonomy {taxa.taxonomy_id}')
                                if new_taxa not in missing_taxa:
                                    missing_taxa.append(new_taxa)
                                if new_taxa not in all_taxa:
                                    all_taxa.append(new_taxa)
                        db_ps.taxa.extend(missing_taxa)
                        for db_taxa in db_ps.taxa:
                            if db_taxa not in all_taxa:
                                remove_taxa.append(db_taxa)
                    # Assumption not to change if null
                    # Empty array would remove all
                    elif ps.taxa is not None:
                        for db_taxa in db_ps.taxa:
                            if db_taxa not in remove_taxa:
                                remove_taxa.append(db_taxa)
                    for taxa in remove_taxa:
                        db_ps.taxa.remove(taxa)

    def expand_results(self, db, simple_results, studies):

        results = self.collect_counts(None)

        for study in simple_results.studies:
            self.map_counts(study, results)

        return simple_results

    def map_count(self, api_item):
        results = self.collect_counts(api_item)

        self.map_counts(api_item, results)

    def map_counts(self, api_item, results):

        for count in [
                'num_collections',
                'num_original_samples',
                'num_derivative_samples',
                'num_assay_data',
                'num_original_derivative_samples',
                'num_original_assay_data',
                'num_released'
        ]:
            if api_item.code in results and count in results[api_item.code]:
                setattr(api_item, count, results[api_item.code][count])


    def collect_counts(self, api_item):

        results = {}

        api_item_code = None
        if api_item:
            api_item_code = "'" + str(api_item.code) + "'"

        stmt = '''SELECT COUNT(*), code FROM
            (SELECT code, COUNT(*) FROM sampling_event se
            LEFT JOIN original_sample os ON os.sampling_event_id = se.id
            LEFT JOIN study s ON s.id = os.study_id group by code, doc) AS
            collections'''

        if api_item_code:
            stmt += ' WHERE code = ' + api_item_code
        stmt += ' GROUP BY code'

        result = self.engine.execute(text(stmt))

        for (count, code) in result:
            results[code] = {}
            results[code]['num_collections'] = count

        stmt = '''SELECT COUNT(*), code FROM original_sample os
                    JOIN study s ON s.id = os.study_id'''

        if api_item_code:
            stmt += ' WHERE code = ' + api_item_code
        stmt += ' GROUP BY code'

        result = self.engine.execute(text(stmt))

        for (count, code) in result:
            if code not in results:
                results[code] = {}
            results[code]['num_original_samples'] = count

        stmt = '''SELECT COUNT(*), code FROM derivative_sample ds
                    JOIN original_sample os ON os.id = ds.original_sample_id
                    JOIN study s ON s.id = os.study_id'''

        if api_item_code:
            stmt += ' WHERE code = ' + api_item_code
        stmt += ' GROUP BY code'

        result = self.engine.execute(text(stmt))

        for (count, code) in result:
            results[code]['num_derivative_samples'] = count

        stmt = '''SELECT COUNT(*), code FROM assay_datum ad
                    JOIN derivative_sample ds ON ds.id = ad.derivative_sample_id
                    JOIN original_sample os ON os.id = ds.original_sample_id
                    JOIN study s ON s.id = os.study_id'''

        if api_item_code:
            stmt += ' WHERE code = ' + api_item_code
        stmt += ' GROUP BY code'

        result = self.engine.execute(text(stmt))

        for (count, code) in result:
            results['num_assay_data'] = count


        stmt = '''SELECT COUNT(*), code FROM original_sample os
                    JOIN study s ON os.study_id = s.id
                    JOIN (SELECT distinct ON (original_sample_id)
                          original_sample_id FROM derivative_sample) AS ds ON
                    ds.original_sample_id = os.id'''

        if api_item_code:
            stmt += ' WHERE code = ' + api_item_code
        stmt += ' GROUP BY code'

        result = self.engine.execute(text(stmt))

        for (count, code) in result:
            results[code]['num_original_derivative_samples'] = count

        stmt = '''SELECT COUNT(*), code FROM original_sample os
            JOIN study s ON os.study_id = s.id
            JOIN (SELECT distinct ON (original_sample_id) original_sample_id, id FROM derivative_sample) AS ds ON ds.original_sample_id = os.id
            JOIN (SELECT distinct ON (derivative_sample_id) derivative_sample_id FROM assay_datum) AS ad
                    ON ad.derivative_sample_id = ds.id'''

        if api_item_code:
            stmt += ' WHERE code = ' + api_item_code
        stmt += ' GROUP BY code'

        result = self.engine.execute(text(stmt))

        for (count, code) in result:
            results[code]['num_original_assay_data'] = count

        stmt = '''SELECT COUNT(*), code FROM
                    (SELECT DISTINCT ON (original_sample_id) original_sample_id FROM manifest_item mi
                    JOIN manifest m ON m.id = mi.manifest_id
                    WHERE manifest_type='release') AS released
                JOIN original_sample os ON released.original_sample_id = os.id
                JOIN study s ON s.id = os.study_id'''
        if api_item_code:
            stmt += ' WHERE code = ' + api_item_code
        stmt += ' GROUP BY code'

        result = self.engine.execute(text(stmt))

        for (count, code) in result:
            results[code]['num_released'] = count

        return results

    def db_map_actions(self, db, db_item, api_item, studies, user, **kwargs):

        if api_item.web_study:
            web_study_item = db.query(Study).filter_by(code=api_item.web_study[:4]).first()
            if web_study_item:
                db_item.web_study = web_study_item.id
            else:
                raise MissingKeyException(f'web study {api_item.web_study} does not exist')
        self.db_map_partner_species(db, db_item, api_item, user)
        self.db_map_expected_samples(db, db_item, api_item, user)
        self.db_map_countries(db, db_item, api_item, user)
        # print('db_map_actions')
        # print(api_item)
        # print(db_item)


    def post_get_action(self, db, db_item, api_item, studies, multiple=False):

        if multiple:
            return api_item

        if db_item.web_study:
            web_study_item = db.query(Study).get(db_item.web_study)
            api_item.web_study = web_study_item.name
        self.map_count(api_item)
        from backbone_server.model.location import Location, BaseLocation
        locs = BaseLocation(self.engine, self.session)

        study_name = api_item.name

        api_item.locations = locs.get_by_study(study_name, None, None, studies)

        return api_item
