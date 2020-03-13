from datetime import datetime

from sqlalchemy import Table, Column
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy import or_, and_
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, aliased

from sqlalchemy.ext.declarative import declared_attr

from openapi_server.models.partner_species import PartnerSpecies
from openapi_server.models.sampling_event import SamplingEvent as ApiSamplingEvent
from openapi_server.models.sampling_events import SamplingEvents

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.nested_edit_exception import NestedEditException
from backbone_server.errors.invalid_date_exception import InvalidDateException
from backbone_server.errors.incompatible_exception import IncompatibleException
from backbone_server.errors.permission_exception import PermissionException

from backbone_server.model.scope import session_scope

from backbone_server.model.mixins import Base
from backbone_server.model.attr import Attr
from backbone_server.model.individual import Individual
from backbone_server.model.study import Study
from backbone_server.model.original_sample import OriginalSample
from backbone_server.model.location import Location, BaseLocation

from backbone_server.model.history_meta import Versioned
from backbone_server.model.base import SimsDbBase

sampling_event_attr_table = Table('sampling_event_attr', Base.metadata,
                                  Column('sampling_event_id', UUID(as_uuid=True),
                                         ForeignKey('sampling_event.id')),
                                  Column('attr_id', UUID(as_uuid=True),
                                         ForeignKey('attr.id'))
                                  )



class SamplingEvent(Versioned, Base):

    @declared_attr
    def __tablename__(cls):
        return 'sampling_event'

    individual_id = Column('individual_id',
                           UUID(as_uuid=True),
                           ForeignKey('individual.id'))
    location_id = Column('location_id',
                         UUID(as_uuid=True),
                         ForeignKey('location.id'))
    proxy_location_id = Column('proxy_location_id',
                               UUID(as_uuid=True),
                               ForeignKey('location.id'))
    doc = Column(Date)
    acc_date = Column(Date)
    doc_accuracy = Column(String(20))

    location = relationship('Location',
                            foreign_keys='SamplingEvent.location_id')
    proxy_location = relationship('Location',
                                  foreign_keys='SamplingEvent.proxy_location_id')
    attrs = relationship("Attr", secondary=sampling_event_attr_table)
    original_samples = relationship("OriginalSample",
                                    backref=backref("sampling_event"))
#    study = relationship("Study",
#                         primaryjoin="and_(foreign(OriginalSample.sampling_event_id) == SamplingEvent.id, foreign(OriginalSample.study_id) == Study.id)")
    individual = relationship("Individual", backref=backref("sampling_event", uselist=False))

    def submapped_items(self):
        return {
            # 'partner_species': 'partner_species.partner_species',
            'location': Location,
            'proxy_location': Location,
            'study_name': 'study.name',
            'individual': Individual,
            'attrs': Attr
        }

    def __repr__(self):
        return f'''<SamplingEvent ID {self.id}
    Acc Date {self.acc_date}
    DOC {self.doc} {self.doc_accuracy}
    location {self.location_id}
    proxy_location {self.proxy_location_id}
    {self.attrs}
    >'''

class BaseSamplingEvent(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=['study',
                                            'location',
                                            'individual',
                                            'sampling_event_attr',
                                            'attr'])

        self.db_class = SamplingEvent
        self.openapi_class = ApiSamplingEvent
        self.openapi_multiple_class = SamplingEvents
        self.attr_link = sampling_event_attr_table
        self.api_id = 'sampling_event_id'
        self.duplicate_attrs = ['partner_id', 'individual_id']
        self.locations = []

    def check_date(self, sampling_event):
        present = datetime.date(datetime.now())

        if sampling_event.doc:
            if sampling_event.doc > present:
                raise InvalidDateException("The date of collection is in the future {}".format(sampling_event.doc))

    def check_location_integrity(self, db, api_location_id, api_location):

        if api_location_id and api_location and api_location.location_id:
            location = db.query(Location).get(api_location_id)
            from openapi_server.models.location import Location as ApiLocation
            api_item = ApiLocation()
            location.map_to_openapi(api_item)
            self.openapi_map_actions(api_item, location)

            if api_item != api_location:
                raise NestedEditException(f"Implied location edit not allowed for {api_location_id}")


    def pre_post_check(self, db, api_item, studies):
        self.check_date(api_item)
        self.check_location_integrity(db, api_item.location_id, api_item.location)
        self.check_location_integrity(db, api_item.proxy_location_id,
                                      api_item.proxy_location)

        return api_item

    def pre_put_check(self, db, api_item, studies):
        self.check_date(api_item)
        self.check_location_integrity(db, api_item.location_id, api_item.location)
        self.check_location_integrity(db, api_item.proxy_location_id,
                                      api_item.proxy_location)

        return api_item

    def expand_results(self, db, simple_results, studies):

        bl = BaseLocation(self.engine, self.session)
        locations = bl.gets_in(self.locations, studies, None, None)

        simple_results.locations = {}
        for location in locations.locations:
            simple_results.locations[location.location_id] = location
        return simple_results




    def post_get_action(self, db, db_item, api_item, studies, multiple):

        if api_item.location_id:
            api_item.location_id = str(api_item.location_id)
            api_item.public_location_id = str(api_item.location_id)
            if multiple:
                if api_item.location_id not in self.locations:
                    self.locations.append(api_item.location_id)
                api_item.location = None
            else:
                bl = BaseLocation(self.engine, self.session)
                api_item.location = bl.get(api_item.location_id, studies)
        if api_item.proxy_location_id:
            api_item.proxy_location_id = str(api_item.proxy_location_id)
            api_item.public_location_id = str(api_item.proxy_location_id)
            if multiple:
                if api_item.proxy_location_id not in self.locations:
                    self.locations.append(api_item.proxy_location_id)
                api_item.location = None
            else:
                bl = BaseLocation(self.engine, self.session)
                api_item.proxy_location = bl.get(api_item.proxy_location_id, studies)

        from backbone_server.model.event_set import EventSet, event_set_members_table

        event_sets = db.query(EventSet).\
                join(event_set_members_table).\
                filter(event_set_members_table.c.sampling_event_id.in_((api_item.sampling_event_id,)))

        api_item.event_sets = []
        for event_set in event_sets.all():
            api_item.event_sets.append(event_set.event_set_name)

        # No empty array
        if not api_item.event_sets:
            api_item.event_sets = None
        return api_item

    def get_by_location(self, location_id, studies, start, count):

        if not location_id:
            raise MissingKeyException("No location_id {}".format(location_id))

        ret = None

        with session_scope(self.session) as db:

            db_items = db.query(self.db_class).\
                    join(self.db_class.original_samples).\
                    filter(or_(SamplingEvent.location_id == location_id, SamplingEvent.proxy_location_id == location_id))

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

            db_items = None
            db_items = db.query(self.db_class).\
                    join(self.db_class.original_samples).\
                    join(taxonomy_identifier_table,
                         and_(taxonomy_identifier_table.c.partner_species_identifier_id == OriginalSample.partner_species_id,
                              taxonomy_identifier_table.c.taxonomy_id == taxa_id))

            ret = self._get_multiple_results(db, db_items, studies, start, count)

            if ret.count == 0:
                db_item = db.query(Taxonomy).get(taxa_id)

                if not db_item:
                    raise MissingKeyException("No taxa_id {}".format(taxa_id))
        return ret

    def get_by_study(self, study_name, start, count, studies):

        if not study_name:
            raise MissingKeyException(f"No study_name to get {self.db_class.__table__}")

        if study_name and studies:
            self.has_study_permission(studies,
                                      study_name,
                                      self.GET_PERMISSION)

        ret = None

        with session_scope(self.session) as db:

            db_items = None
            db_items = db.query(self.db_class).\
                    join(self.db_class.original_samples).\
                    filter(OriginalSample.study.has(code=study_name[:4]))

            ret = self._get_multiple_results(db, db_items, studies, start, count)

            if ret.count == 0:
                db_item = db.query(Study).filter_by(code=study_name[:4]).first()
                if not db_item:
                    raise MissingKeyException(f'No such study {study_name}')

        return ret

    def get_by_event_set(self, event_set_name, studies, start, count):

        if not event_set_name:
            raise MissingKeyException("No event_set_name {}".format(event_set_name))

        ret = None

        with session_scope(self.session) as db:
            from backbone_server.model.event_set import EventSet, event_set_members_table

            event_set = db.query(EventSet).filter_by(event_set_name=event_set_name).first()
            if not event_set:
                raise MissingKeyException("No event_set_name {}".format(event_set_name))

            db_items = db.query(self.db_class).\
                    join(event_set_members_table, \
                    and_(event_set_members_table.c.event_set_id == event_set.id,
                         event_set_members_table.c.sampling_event_id == SamplingEvent.id)).\
                    join(self.db_class.original_samples).\
                    filter(EventSet.event_set_name == event_set_name)

            ret = self._get_multiple_results(db, db_items, studies, start, count)

            if ret.count == 0:
                db_item = db.query(EventSet).filter(EventSet.event_set_name == event_set_name).first()

                if not db_item:
                    raise MissingKeyException("No event_set_name {}".format(event_set_name))
        return ret

    def get_by_os_attr(self, attr_type, attr_value, study_name, value_type,
                       start, count, studies):

        if not attr_type:
            raise MissingKeyException(f"No attr_type to get {self.db_class.__table__}")

        if study_name and studies:
            self.has_study_permission(studies,
                                      study_name,
                                      self.GET_PERMISSION)

        ret = None

        with session_scope(self.session) as db:

            from backbone_server.model.original_sample import original_sample_attr_table
            db_items = None
            study_filter = True
            from openapi_server.models.attr import Attr as AttrApi

            api_attr = AttrApi(attr_type=attr_type,
                               attr_value=attr_value,
                               study_name=study_name)
            attrs = []
            for db_attr in Attr.get_all(db, api_attr, value_type):
                attrs.append(db_attr.id)

            if not attrs:
                ret = self.openapi_multiple_class()
                ret.count = 0
                return ret

            if study_name:
                study_filter = False
                study_codes = self.study_filter(studies)

                if study_codes:
                    if study_name[:4] not in study_codes:
                        raise PermissionException(f'No allowed to access {study_name}')

                os_study = aliased(OriginalSample.study)
                db_items = db.query(self.db_class).\
                        join(OriginalSample.sampling_event).\
                        join(original_sample_attr_table,
                             and_(original_sample_attr_table.c.original_sample_id == OriginalSample.id,
                                  original_sample_attr_table.c.attr_id.in_(attrs))).\
                        outerjoin(Study).\
                        outerjoin(os_study, OriginalSample.study_id == os_study.id).\
                        filter(or_(Study.code == study_name[:4],
                                   os_study.code == study_name[:4]))
            else:
                db_items = db.query(self.db_class).\
                        join(OriginalSample.sampling_event).\
                        join(original_sample_attr_table,
                             and_(original_sample_attr_table.c.original_sample_id == OriginalSample.id,
                                  original_sample_attr_table.c.attr_id.in_(attrs)))

            print(db_items)
            # db_item = db.query(self.db_class).filter_by(id=item_id).first()
            ret = self._get_multiple_results(db, db_items, studies, start,
                                             count, study_filter=study_filter)

        return ret


    def merge(self, into, merged, studies):

        with session_scope(self.session) as db:
            self.run_merge(db, into, merged, studies)


    def run_merge(self, db, into, merged, studies):
        sampling_event1 = self.lookup_query(db).filter_by(id=into).first()

        if not sampling_event1:
            raise MissingKeyException("No sampling_event {}".format(into))

        if into == merged:
            return self.get(into, studies)

        sampling_event2 = self.lookup_query(db).filter_by(id=merged).first()

        if not sampling_event2:
            raise MissingKeyException("No sampling_event {}".format(merged))

        if sampling_event1.doc:
            if sampling_event2.doc:
                if sampling_event1.doc != sampling_event2.doc:
                    msg = 'Incompatible doc {} {}'.format(sampling_event1.doc,
                                                          sampling_event2.doc)
                    raise IncompatibleException(msg)
        else:
            sampling_event1.doc = sampling_event2.doc

        if sampling_event1.doc_accuracy:
            if sampling_event2.doc_accuracy:
                if sampling_event1.doc_accuracy != sampling_event2.doc_accuracy:
                    msg = 'Incompatible doc_accuracy {} {}'.format(sampling_event1.doc_accuracy,
                                                                   sampling_event2.doc_accuracy)
                    raise IncompatibleException(msg)
        else:
            if sampling_event2.doc_accuracy:
                sampling_event1.doc_accuracy = sampling_event2.doc_accuracy

        if sampling_event1.location_id:
            if sampling_event2.location_id:
                if sampling_event1.location_id != sampling_event2.location_id:
                    msg = 'Incompatible location_id {} {}'.format(sampling_event1.location_id,
                                                                  sampling_event2.location_id)
                    raise IncompatibleException(msg)
        else:
            sampling_event1.location_id = sampling_event2.location_id

        if sampling_event1.proxy_location_id == 'None':
            sampling_event1.proxy_location_id = None
        if sampling_event2.proxy_location_id == 'None':
            sampling_event2.proxy_location_id = None

        if sampling_event1.proxy_location_id:
            if sampling_event2.proxy_location_id:
                if sampling_event1.proxy_location_id != sampling_event2.proxy_location_id:
                    msg = 'Incompatible proxy_location_id {} {}'.format(sampling_event1.proxy_location_id,
                                                                        sampling_event2.proxy_location_id)
                    raise IncompatibleException(msg)
        else:
            sampling_event1.proxy_location_id = sampling_event2.proxy_location_id

        if sampling_event2.attrs:
            for new_ident in sampling_event2.attrs:
                found = False
                for existing_ident in sampling_event1.attrs:
                    if new_ident == existing_ident:
                        found = True
                if not found:
                    new_ident_value = True
                    sampling_event1.attrs.append(new_ident)

        u = text("UPDATE event_set_member SET sampling_event_id = :into WHERE sampling_event_id = :os2")
        self.engine.execute(u, into=into, os2=merged)
        db.commit()

        self.delete(merged, studies)

        return self.get(into, studies)
