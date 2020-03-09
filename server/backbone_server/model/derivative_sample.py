from datetime import datetime

from sqlalchemy import Table, MetaData, Column
from sqlalchemy import Integer, String, ForeignKey, DateTime, Date, func, UniqueConstraint
from sqlalchemy import or_, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, aliased

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from openapi_server.models.partner_species import PartnerSpecies
from openapi_server.models.derivative_sample import DerivativeSample as ApiDerivativeSample
from openapi_server.models.derivative_samples import DerivativeSamples

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException

from backbone_server.model.scope import session_scope

from backbone_server.model.mixins import Base
from backbone_server.model.attr import Attr
from backbone_server.model.study import Study
from backbone_server.model.original_sample import OriginalSample
from backbone_server.model.location import Location

from backbone_server.model.history_meta import Versioned
from backbone_server.model.base import SimsDbBase

derivative_sample_attr_table = Table('derivative_sample_attr', Base.metadata,
                                     Column('derivative_sample_id', UUID(as_uuid=True),
                                            ForeignKey('derivative_sample.id')),
                                     Column('attr_id', UUID(as_uuid=True),
                                            ForeignKey('attr.id'))
                                     )



class DerivativeSample(Versioned, Base):

    @declared_attr
    def __tablename__(cls):
        return 'derivative_sample'

    original_sample_id = Column('original_sample_id',
                                UUID(as_uuid=True),
                                ForeignKey('original_sample.id'))
    parent_derivative_sample_id = Column('parent_derivative_sample_id',
                                         UUID(as_uuid=True),
                                         ForeignKey('derivative_sample.id'))
    acc_date = Column(DateTime)
    dna_prep = Column(String(20))

    attrs = relationship("Attr", secondary=derivative_sample_attr_table)
    original_sample = relationship("OriginalSample",
                                   backref=backref("derivative_sample"))
    #derivative_sample = relationship("DerivativeSample",
    #                                backref=backref("derivative_sample"))

    def submapped_items(self):
        return {
            # 'partner_species': 'partner_species.partner_species',
            'original_sample': OriginalSample,
            'derivative_sample': DerivativeSample,
            'attrs': Attr
        }

    def __repr__(self):
        return f'''<DerivativeSample ID {self.id}
    {self.dna_prep}
    {self.attrs}
    >'''

class BaseDerivativeSample(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=['original_sample',
                                            'derivative_sample_attr',
                                            'attr'])

        self.db_class = DerivativeSample
        self.openapi_class = ApiDerivativeSample
        self.openapi_multiple_class = DerivativeSamples
        self.attr_link = derivative_sample_attr_table
        self.api_id = 'derivative_sample_id'
        self.duplicate_attrs = ['plate_name', 'plate_position']


    def get_by_location(self, location_id, studies, start, count):

        if not location_id:
            raise MissingKeyException("No location_id {}".format(location_id))

        ret = None

        with session_scope(self.session) as db:

            from backbone_server.model.sampling_event import SamplingEvent
            db_items = db.query(self.db_class).\
                    join(self.db_class.original_sample).\
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
            from backbone_server.model.study import PartnerSpeciesIdentifier, Taxonomy

            db_items = None
            db_items = db.query(self.db_class).\
                    join(self.db_class.original_sample).\
                    join(OriginalSample.partner_species).\
                    join(PartnerSpeciesIdentifier.taxa).\
                    filter(Taxonomy.id == taxa_id)

            ret = self._get_multiple_results(db, db_items, studies, start, count)

            if ret.count == 0:
                db_item = db.query(Taxonomy).get(taxa_id)

                if not db_item:
                    raise MissingKeyException("No taxa_id {}".format(taxa_id))
        return ret

    def get_by_study(self, study_name, studies, start, count):

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
                    join(self.db_class.original_sample).\
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
            from sqlalchemy.orm import aliased
            from sqlalchemy import and_
            from backbone_server.model.event_set import EventSet, event_set_members_table

            event_set = db.query(EventSet).filter_by(event_set_name=event_set_name).first()
            if not event_set:
                raise MissingKeyException("No event_set_name {}".format(event_set_name))

            sampling_event = aliased(OriginalSample.sampling_event)
            db_items = db.query(self.db_class).\
                    join(self.db_class.original_sample).\
                    join(sampling_event).\
                    join(event_set_members_table, \
                    and_(event_set_members_table.c.event_set_id == str(event_set.id),
                         event_set_members_table.c.sampling_event_id == sampling_event.id)).\
                    distinct(self.db_class.id)

            ret = self._get_multiple_results(db, db_items, studies, start, count)

            if ret.count == 0:
                db_item = db.query(EventSet).filter(EventSet.event_set_name == event_set_name).first()
                if not db_item:
                    raise MissingKeyException("No event_set_name {}".format(event_set_name))
        return ret

    def get_by_os_attr(self, attr_type, attr_value, study_name, studies, start, count):

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
            if study_name:
                study_filter = False
                study_codes = self.study_filter(studies)

                if study_codes:
                    if study_name[:4] not in study_codes:
                        raise PermissionException(f'No allowed to access {study_name}')
                os_study = aliased(OriginalSample.study)
                db_items = db.query(self.db_class).\
                        join(self.db_class.original_sample).\
                        join(original_sample_attr_table).\
                        join(Attr).\
                        outerjoin(Study).\
                        outerjoin(os_study, OriginalSample.study_id == os_study.id).\
                        filter(and_(or_(Study.code == study_name[:4],
                                        os_study.code == study_name[:4]),\
                        Attr.attr_type == attr_type, \
                        Attr.attr_value == attr_value))
            else:
                db_items = db.query(self.db_class).\
                        join(self.db_class.original_sample).\
                        join(original_sample_attr_table).\
                        join(Attr).\
                        filter(Attr.attr_type == attr_type).\
                        filter(Attr.attr_value == attr_value)
            # db_item = db.query(self.db_class).filter_by(id=item_id).first()

            ret = self._get_multiple_results(db, db_items, studies, start,
                                             count, study_filter=study_filter)

        return ret
