import os

from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy import event, and_

from openapi_server.models.study import Study as ApiStudy
from openapi_server.models.studies import Studies as ApiStudies
from openapi_server.models.partner_species import PartnerSpecies
from openapi_server.models.taxonomy import Taxonomy as ApiTaxonomy

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.model.history_meta import Versioned
from backbone_server.model.base import SimsDbBase
from backbone_server.model.mixins import Base

taxonomy_identifier_table = Table('taxonomy_identifier', Base.metadata,
                                  Column('taxonomy_id', Integer(), ForeignKey('taxonomy.id')),
                                  Column('partner_species_identifier_id', UUID(as_uuid=True), ForeignKey('partner_species_identifier.id'))
                                  )

class ExpectedSamples(Base):
    @declared_attr
    def __tablename__(cls):
        return 'expected_samples'

    sample_count = Column(Integer())
    date_of_arrival = Column(DateTime())
    study_id = Column('study_id',
                      UUID(as_uuid=True),
                      ForeignKey('study.id'))
    partner_species_id = Column('partner_species_id',
                                UUID(as_uuid=True),
                                ForeignKey('partner_species_identifier.id'))
    partner_species = relationship("PartnerSpeciesIdentifier", backref=backref("expected_sample", uselist=False))

    @staticmethod
    def get_or_create(db, e_sample, study_id):

        expected_sample = None
        if e_sample is None or e_sample.expected_samples_id is None:
            expected_sample = ExpectedSamples(sample_count=e_sample.sample_count,
                                             date_of_arrival=e_sample.date_of_arrival,
                                             study_id=study_id)
            psi = PartnerSpeciesIdentifier.get_or_create(db, e_sample.expected_species, study_id)
            expected_sample.partner_species_id = psi.id
            expected_sample.partner_species = psi
            db.add(expected_sample)
            db.commit()
        else:
            expected_sample = db.query(ExpectedSamples).filter_by(id=e_sample.expected_sample_id).first()
            expected_sample.sample_count = e_sample.sample_count
            expected_sample.date_of_arrival = e_sample.date_of_arrival
            expected_sample.study_id = study_id
            psi = PartnerSpeciesIdentifier.get_or_create(db, e_sample.expected_species, study_id)
            expected_sample.partner_species_id = psi.id
            expected_sample.partner_species = psi

        return expected_sample

    def submapped_items(self):
        return {
            'partner_species': PartnerSpeciesIdentifier,
            'study_name': 'study'
        }

    def __repr__(self):
        return f'''<ExpectedSamples ID {self.id}
    Study {self.study_id}
    Partner Species {self.partner_species}
    Partner Species {self.partner_species_id}
    {self.sample_count}
    {self.date_of_arrival}
    >'''

class Taxonomy(Base):

    id = Column(Integer(), primary_key=True)
    rank = Column(String(32))
    name = Column(String(128))

    @staticmethod
    def get_or_create(db, tid):

        taxa = db.query(Taxonomy).filter_by(id=tid).first()

        if taxa is None:
            taxa = Taxonomy(id=tid)
            db.add(taxa)
            db.commit()
            taxa = db.query(Taxonomy).filter_by(id=tid).first()

        return taxa

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


class Study(Base):

    name = Column(String(64))
    code = Column(String(4), index=True)
    ethics_expiry = Column(Date())

#    documents = relationship("Document")
    partner_species = relationship('PartnerSpeciesIdentifier',
                                   back_populates='study')
    expected_samples = relationship("ExpectedSamples",
                                    backref=backref("study"))
    def __repr__(self):
        return f'''<Study {self.name} {self.code}
    {self.partner_species}
    {self.expected_samples}
    {self.ethics_expiry}>'''

    @staticmethod
    def get_or_create_study(db, study_name):

        study = db.query(Study).filter_by(code=study_name[:4]).first()

        if study is None:
            study = Study(name=study_name, code=study_name[:4])
            db.add(study)
            db.commit()
            study = db.query(Study).filter_by(code=study_name[:4]).first()

        return study

    def submapped_items(self):
        return {
            'partner_species': PartnerSpeciesIdentifier,
            'expected_samples': ExpectedSamples
        }


class PartnerSpeciesIdentifier(Base):
    @declared_attr
    def __tablename__(cls):
        return 'partner_species_identifier'

    partner_species = Column(String(128))
    study_id = Column('study_id',
                      UUID(as_uuid=True),
                      ForeignKey('study.id'))
    study = relationship('Study',
                         back_populates='partner_species')
    taxa = relationship('Taxonomy',
                              secondary=taxonomy_identifier_table)

    @staticmethod
    def get_or_create(db, partner_species, study_id):
        ps_item_query = db.query(PartnerSpeciesIdentifier).\
                            filter(and_(PartnerSpeciesIdentifier.partner_species == partner_species,
                                        PartnerSpeciesIdentifier.study_id == study_id))
        ps_item = ps_item_query.first()

        if not ps_item:
            ps_item = PartnerSpeciesIdentifier(partner_species=partner_species,
                                               study_id=study_id)
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

class BaseStudy(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=[
            'study',
            'partner_species_identifier'
        ])

        self.db_class = Study
        self.openapi_class = ApiStudy
        self.openapi_multiple_class = ApiStudies

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

    def db_map_expected_samples(self, db, db_item, api_item):
        if hasattr(api_item, 'expected_samples') and api_item.expected_samples:
            new_expected_samples = []
            for expected_sample in api_item.expected_samples:
                db_expected_sample = ExpectedSamples.get_or_create(db,
                                                                   expected_sample,
                                                                   db_item.id)
                if db_expected_sample in new_expected_samples:
                    raise DuplicateKeyException(f'Error duplicate expected_sample {expected_sample}')
                new_expected_samples.append(db_expected_sample)
            # [] or None
            if new_expected_samples:
                db_item.expected_samples.extend(new_expected_samples)
            expected_sample_to_remove = []
            for expected_sample in db_item.expected_samples:
                if expected_sample not in new_expected_samples:
                    expected_sample_to_remove.append(expected_sample)
            for expected_sample in expected_sample_to_remove:
                db_item.expected_samples.remove(expected_sample)
        elif hasattr(db_item, 'expected_samples'):
            expected_sample_to_remove = []
            for expected_sample in db_item.expected_samples:
                expected_sample_to_remove.append(expected_sample)
            for expected_sample in expected_sample_to_remove:
                db_item.expected_samples.remove(expected_sample)

    def db_map_actions(self, db, db_item, api_item):

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
                                new_taxa = Taxonomy.get_or_create(db,
                                                                  taxa.taxonomy_id)
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

        self.db_map_expected_samples(db, db_item, api_item)
        # print('db_map_actions')
        # print(api_item)
        # print(db_item)

    def openapi_map_actions(self, api_item, db_item):
        # print('openapi_map_actions')
        # print(db_item)
        # print(api_item)
        api_item.partner_species = []
        for psi in db_item.partner_species:
            ps_item = PartnerSpecies()
            psi.map_to_openapi(ps_item)
            ps_item.partner_taxonomies = []

            if not ps_item.taxa:
                ps_item.taxa = []
            api_item.partner_species.append(ps_item)
        if api_item.expected_samples:
            for es in api_item.expected_samples:
                for db_es in db_item.expected_samples:
                    if str(db_es.id) == es.expected_samples_id:
                        ps_item = PartnerSpecies()
                        db_es.partner_species.map_to_openapi(ps_item)
                        ps_item.partner_taxonomies = []

                        if not ps_item.taxa:
                            ps_item.taxa = []
                        es.expected_species = ps_item.partner_species
                        es.expected_taxonomies = ps_item.taxa
        # print(f'Study openapi_map_actions {api_item}')

    def post_get_action(self, db, db_item, api_item, studies, multiple=False):

        if multiple:
            return api_item

        from backbone_server.model.location import Location, BaseLocation
        locs = BaseLocation(self.engine, self.session)

        study_name = api_item.name

        api_item.locations = locs.get_by_study(study_name, studies, None,
                                               None)

        return api_item
