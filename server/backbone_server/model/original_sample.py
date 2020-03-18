from sqlalchemy import Table, MetaData, Column
from sqlalchemy import Integer, String, ForeignKey, Date, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import and_
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import joinedload

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from openapi_server.models.partner_species import PartnerSpecies
from openapi_server.models.original_sample import OriginalSample as OS
from openapi_server.models.original_samples import OriginalSamples

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.incompatible_exception import IncompatibleException

from backbone_server.model.scope import session_scope

from backbone_server.model.mixins import Base
from backbone_server.model.attr import Attr
from backbone_server.model.study import Study, PartnerSpeciesIdentifier

from backbone_server.model.history_meta import Versioned
from backbone_server.model.base import SimsDbBase

original_sample_attr_table = Table('original_sample_attr', Base.metadata,
                                   Column('original_sample_id', UUID(as_uuid=True),
                                          ForeignKey('original_sample.id')),
                                   Column('attr_id', UUID(as_uuid=True),
                                          ForeignKey('attr.id'))
                                   )



class OriginalSample(Versioned, Base):

    @declared_attr
    def __tablename__(cls):
        return 'original_sample'

    study_id = Column('study_id',
                      UUID(as_uuid=True),
                      ForeignKey('study.id'),
                      index=True)
    sampling_event_id = Column('sampling_event_id',
                               UUID(as_uuid=True),
                               ForeignKey('sampling_event.id'))
    partner_species_id = Column('partner_species_id',
                                UUID(as_uuid=True),
                                ForeignKey('partner_species_identifier.id'))
    acc_date = Column(Date)
    days_in_culture = Column(Integer)

    study = relationship("Study", backref=backref("original_sample", uselist=False))
    attrs = relationship("Attr", secondary=original_sample_attr_table)
    partner_species = relationship("PartnerSpeciesIdentifier",
                                   backref=backref("original_sample",
                                                   uselist=False))

    def submapped_items(self):
        return {
            # 'partner_species': 'partner_species.partner_species',
            'partner_species': PartnerSpeciesIdentifier,
            'study_name': 'study.name',
            'attrs': Attr
        }

    def __repr__(self):
        return f'''<OriginalSample ID {self.id}
    Study {self.study}
    Acc Date {self.acc_date}
    DIC {self.days_in_culture}
    {self.partner_species}
    {self.attrs}
    >'''


class BaseOriginalSample(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=['study',
                                            'partner_species_identifier',
                                            'original_sample_attr',
                                            'sampling_event',
                                            'attr'])
        Base.metadata.create_all(engine)
        self.db_class = OriginalSample
        self.openapi_class = OS
        self.openapi_multiple_class = OriginalSamples
        self.attr_link = original_sample_attr_table
        self.duplicate_attrs = [
            'partner_id',
            'individual_id'
        ]
        self.api_id = 'original_sample_id'
        self.old_study_id = None

    def put_premap(self, db, api_item, db_item):
        if db_item.study.code != api_item.study_name[:4]:
            self.old_study_id = db_item.study.id


    def db_map_actions(self, db, db_item, api_item, studies):
        # print('db_map_actions')
        # print(api_item)

        study = Study.get_or_create_study(db, api_item.study_name)
        db_item.study_id = study.id

        # If we change the study then need to update all the attributes
        # which reference it
        if self.old_study_id:
            for attr in db_item.attrs:
                if attr.study_id and attr.study_id == self.old_study_id:
                    attr.study_id = study.id
            if db_item.sampling_event_id:
                u = text('''UPDATE attr SET study_id = :new_study_id WHERE
                         study_id = :old_study_id AND id IN (SELECT
                         attr_id FROM sampling_event_attr WHERE
                         sampling_event_id = :sampling_event_id)''')
                self.engine.execute(u, new_study_id=study.id,
                                    old_study_id=self.old_study_id,
                                    sampling_event_id=db_item.sampling_event_id)
                u = text('''UPDATE attr SET study_id = :new_study_id WHERE
                         study_id = :old_study_id AND id IN (SELECT attr_id
                         FROM location_attr WHERE location_id IN
                            (SELECT location_id FROM sampling_event WHERE id = :sampling_event_id))''')
                self.engine.execute(u, new_study_id=study.id,
                                    old_study_id=self.old_study_id,
                                    sampling_event_id=db_item.sampling_event_id)
                u = text('''UPDATE attr SET study_id = :new_study_id WHERE
                         study_id = :old_study_id AND id IN (SELECT attr_id
                         FROM individual_attr WHERE individual_id IN
                            (SELECT individual_id FROM sampling_event WHERE id = :sampling_event_id))''')
                self.engine.execute(u, new_study_id=study.id,
                                    old_study_id=self.old_study_id,
                                    sampling_event_id=db_item.sampling_event_id)

        if api_item.partner_species:
            db_item.partner_species = PartnerSpeciesIdentifier.get_or_create(db, api_item.partner_species, study.id)

        # print('db_map_actions')
        # print(api_item)
        # print(db_item)

    def openapi_map_actions(self, api_item, db_item):

        db_ps_item = db_item.partner_species
        if db_ps_item:
            ps_item = PartnerSpecies()
            # print('Mapping db_ps_item to ps_item')
            db_ps_item.map_to_openapi(ps_item)
            api_item.partner_species = ps_item.partner_species
            api_item.partner_taxonomies = ps_item.taxa
            # print(ps_item)
        # print(f'BaseOriginalSample.openapi_map_actions {db_item}')
        # print(f'BaseOriginalSample.openapi_map_actions {api_item}')

    def expand_results(self, db, simple_results, studies):

        sampling_events = []
        for os in simple_results.original_samples:
            if os.sampling_event_id not in sampling_events:
                sampling_events.append(os.sampling_event_id)

        from backbone_server.model.sampling_event import SamplingEvent, BaseSamplingEvent
        from backbone_server.model.location import BaseLocation
        from openapi_server.models.sampling_event import SamplingEvent as ApiSamplingEvent

        if sampling_events:
            location_ids = []
            simple_results.sampling_events = {}
            db_query = db.query(SamplingEvent).filter(SamplingEvent.id.in_((sampling_events)))
            se = BaseSamplingEvent(self.engine, self.session)
            for db_item in db_query.all():
                api_item = ApiSamplingEvent()
                db_item.map_to_openapi(api_item)
                se.openapi_map_actions(api_item, db_item)

                study_code = se.get_study_code(db_item)
                self.has_study_permission(studies,
                                          study_code,
                                          self.GET_PERMISSION)
                if 'study_name' in api_item.openapi_types:
                    api_item.study_name = db_item.study.name

                if api_item.location_id and api_item.location_id not in location_ids:
                    location_ids.append(api_item.location_id)
                if api_item.proxy_location_id and api_item.proxy_location_id not in location_ids:
                    location_ids.append(api_item.proxy_location_id)
                simple_results.sampling_events[api_item.sampling_event_id] = api_item

            # Lat/lng not filled in
            # Should probably have a location map as well to be more efficient
            bl = BaseLocation(self.engine, self.session)
            locations = bl.gets_in(location_ids, studies, None, None)
            locations_map = {}
            for location in locations.locations:
                locations_map[location.location_id] = location
            for sampling_event in simple_results.sampling_events.values():
                if sampling_event.location_id:
                    sampling_event.location = locations_map[sampling_event.location_id]
                if sampling_event.proxy_location_id:
                    sampling_event.proxy_location = locations_map[sampling_event.proxy_location_id]

        return simple_results

    def merge(self, into, merged, studies):

        ret = None

        with session_scope(self.session) as db:

            original_sample1 = self.lookup_query(db).filter_by(id=into).options(joinedload(OriginalSample.study)).first()
            original_sample2 = self.lookup_query(db).filter_by(id=merged).options(joinedload(OriginalSample.study)).first()

            if not original_sample1:
                raise MissingKeyException("No original_sample {}".format(into))

            if into == merged:
                return self.get(into, studies)

            if not original_sample2:
                raise MissingKeyException("No original_sample {}".format(merged))

            if original_sample1.study:
                self.has_study_permission(studies,
                                          original_sample1.study.code,
                                          self.GET_PERMISSION)
                if original_sample2.study:
                    if original_sample1.study.name[:4] == '0000':
                        original_sample1.study.name = original_sample2.study.name
                    elif original_sample2.study.name[:4] == '0000':
                        pass
                    elif original_sample1.study.name != original_sample2.study.name:
                        msg = 'Incompatible study_name {} {}'.format(original_sample1.study.name,
                                                                     original_sample2.study.name)
                        raise IncompatibleException(msg)
            else:
                self.has_study_permission(studies,
                                          original_sample2.study.name,
                                          self.GET_PERMISSION)
                original_sample1.study_id = original_sample2.study_id

            if original_sample1.days_in_culture:
                if original_sample2.days_in_culture:
                    if original_sample1.days_in_culture != original_sample2.days_in_culture:
                        msg = 'Incompatible days_in_culture {} {}'.format(original_sample1.days_in_culture,
                                                                          original_sample2.days_in_culture)
                        raise IncompatibleException(msg)
            else:
                original_sample1.days_in_culture = original_sample2.days_in_culture

            if original_sample1.partner_species and original_sample1.partner_species.partner_species:
                if original_sample2.partner_species and original_sample2.partner_species.partner_species:
                    if original_sample1.partner_species.partner_species != original_sample2.partner_species.partner_species:
                        msg = 'Incompatible partner_species {} {}'.format(original_sample1.partner_species,
                                                                          original_sample2.partner_species)
                        raise IncompatibleException(msg)
            else:
                original_sample1.partner_species = original_sample2.partner_species

            if original_sample2.attrs:
                for new_ident in original_sample2.attrs:
                    found = False
                    for existing_ident in original_sample1.attrs:
                        if new_ident == existing_ident:
                            found = True
                    if not found:
                        new_ident_value = True
                        original_sample1.attrs.append(new_ident)


            if original_sample1.sampling_event_id:
                if original_sample2.sampling_event_id:
                    from backbone_server.model.sampling_event import BaseSamplingEvent
                    merge = BaseSamplingEvent(self.engine, self.session)
                    # Otherwise can't delete after merge
                    os2_samp_event = original_sample2.sampling_event_id
                    original_sample2.sampling_event_id = None
                    merged_se = merge.run_merge(db, original_sample1.sampling_event_id,
                                                os2_samp_event,
                                                studies)
                    original_sample1 = self.lookup_query(db).filter_by(id=into).options(joinedload(OriginalSample.study)).first()
                    original_sample1.sampling_event_id = merged_se.sampling_event_id
                    db.commit()
            else:
                original_sample1.sampling_event_id = original_sample2.sampling_event_id

            u = text("UPDATE derivative_sample SET original_sample_id = :into WHERE original_sample_id = :os2")
            self.engine.execute(u, into=into, os2=merged)
            self.delete(merged, studies)
            db.commit()

        ret = self.get(into, studies)

        return ret

    def get_by_location(self, location_id, studies, start, count):

        if not location_id:
            raise MissingKeyException("No location_id {}".format(location_id))

        ret = None

        with session_scope(self.session) as db:
            from backbone_server.model.sampling_event import SamplingEvent
            from backbone_server.model.location import Location

            db_items = None
            db_items = db.query(self.db_class).\
                    join(self.db_class.sampling_event).\
                    join(SamplingEvent.location).\
                    filter(Location.id == location_id)

            ret = self._get_multiple_results(db, db_items, studies, start, count)

            if ret.count == 0:
                db_item = db.query(Location).get(location_id)

                if not db_item:
                    raise MissingKeyException("No location_id {}".format(location_id))
        return ret

    def get_by_taxa(self, taxa_id, studies, start, count):

        if not taxa_id:
            raise MissingKeyException("No taxa {}".format(taxa_id))

        ret = None

        with session_scope(self.session) as db:
            from backbone_server.model.study import Taxonomy, taxonomy_identifier_table

            db_items = db.query(self.db_class).\
                        join(taxonomy_identifier_table,
                             and_(taxonomy_identifier_table.c.partner_species_identifier_id == OriginalSample.partner_species_id,
                                  taxonomy_identifier_table.c.taxonomy_id == taxa_id))

            ret = self._get_multiple_results(db, db_items, studies, start, count)

            if ret.count == 0:
                if not db.query(Taxonomy).get(taxa_id):
                    raise MissingKeyException(f'No such taxa {taxa_id}')

        return ret



    def get_by_event_set(self, event_set_name, studies, start, count):

        if not event_set_name:
            raise MissingKeyException("No event_set_name {}".format(event_set_name))

        ret = None

        with session_scope(self.session) as db:
            from sqlalchemy.orm import aliased
            from backbone_server.model.event_set import EventSet, event_set_members_table

            event_set = db.query(EventSet).filter_by(event_set_name=event_set_name).first()
            if not event_set:
                raise MissingKeyException("No event_set_name {}".format(event_set_name))

            sampling_event = aliased(OriginalSample.sampling_event)
            db_items = db.query(self.db_class).\
                    join(sampling_event).\
                    join(event_set_members_table).\
                    filter(event_set_members_table.c.event_set_id == event_set.id).\
                    distinct(self.db_class.id)

            ret = self._get_multiple_results(db, db_items, studies, start, count)

            if ret.count == 0:
                db_item = db.query(EventSet).filter(EventSet.event_set_name == event_set_name).first()
                if not db_item:
                    raise MissingKeyException("No event_set_name {}".format(event_set_name))
        return ret
