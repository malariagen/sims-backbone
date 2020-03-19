from datetime import datetime

from sqlalchemy import Table, MetaData, Column
from sqlalchemy import Integer, String, ForeignKey, DateTime, Date, func, UniqueConstraint
from sqlalchemy import or_, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, aliased

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from openapi_server.models.assay_datum import AssayDatum as ApiAssayDatum
from openapi_server.models.assay_data import AssayData

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.nested_edit_exception import NestedEditException
from backbone_server.errors.invalid_date_exception import InvalidDateException
from backbone_server.errors.permission_exception import PermissionException

from backbone_server.model.scope import session_scope

from backbone_server.model.mixins import Base
from backbone_server.model.attr import Attr
from backbone_server.model.study import Study
from backbone_server.model.derivative_sample import DerivativeSample
from backbone_server.model.original_sample import OriginalSample

from backbone_server.model.history_meta import Versioned
from backbone_server.model.base import SimsDbBase

assay_datum_attr_table = Table('assay_datum_attr', Base.metadata,
                                  Column('assay_datum_id', UUID(as_uuid=True),
                                         ForeignKey('assay_datum.id')),
                                  Column('attr_id', UUID(as_uuid=True),
                                         ForeignKey('attr.id'))
                                  )



class AssayDatum(Versioned, Base):

    @declared_attr
    def __tablename__(cls):
        return 'assay_datum'

    derivative_sample_id = Column('derivative_sample_id',
                               UUID(as_uuid=True),
                               ForeignKey('derivative_sample.id'))
    acc_date = Column(DateTime)
    ebi_run_acc = Column(String(20))

    attrs = relationship("Attr", secondary=assay_datum_attr_table)
    derivative_sample = relationship("DerivativeSample",
                                   backref=backref("assay_datum"))
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
        return f'''<AssayDatum ID {self.id}
    {self.ebi_run_acc}
    {self.acc_date}
    {self.attrs}
    >'''

class BaseAssayDatum(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=['original_sample',
                                            'assay_datum_attr',
                                            'attr'])

        self.db_class = AssayDatum
        self.openapi_class = ApiAssayDatum
        self.openapi_multiple_class = AssayData
        self.attr_link = assay_datum_attr_table
        self.api_id = 'assay_datum_id'
        self.duplicate_attrs = []

    def expand_results(self, db, simple_results, studies):

        derivative_samples = []
        for ds in simple_results.assay_data:
            if ds.derivative_sample_id not in derivative_samples:
                derivative_samples.append(ds.derivative_sample_id)

        from backbone_server.model.derivative_sample import BaseDerivativeSample
        from openapi_server.models.derivative_sample import DerivativeSample as ApiDerivativeSample

        if derivative_samples:
            simple_results.derivative_samples = {}
            db_query = db.query(DerivativeSample).filter(DerivativeSample.id.in_((derivative_samples)))
            ds = BaseDerivativeSample(self.engine, self.session)
            for db_item in db_query.all():
                api_item = ApiDerivativeSample()
                db_item.map_to_openapi(api_item)
                ds.openapi_map_actions(api_item, db_item)

                study_code = ds.get_study_code(db_item)
                self.has_study_permission(studies,
                                          study_code,
                                          self.GET_PERMISSION)
                if 'study_name' in api_item.openapi_types:
                    api_item.study_name = db_item.study.name
                simple_results.derivative_samples[api_item.derivative_sample_id] = api_item

        return simple_results
#
#     def get_by_location(self, location_id, studies, start, count):
#
#         if not location_id:
#             raise MissingKeyException("No location_id {}".format(location_id))
#
#         ret = None
#
#         with session_scope(self.session) as db:
#
#             db_items = db.query(self.db_class).\
#                     join(self.db_class.original_sample).\
#                     filter(or_(SamplingEvent.location_id == location_id, SamplingEvent.proxy_location_id == location_id))
#
#             ret = self._get_multiple_results(db, db_items, start, count,
#             studies=studies)
#
#             if ret.count == 0:
#                 db_item = db.query(Location).get(location_id)
#
#                 if not db_item:
#                     raise MissingKeyException("No location_id {}".format(location_id))
#         return ret
#
#     def get_by_taxa(self, taxa_id, studies, start, count):
#
#         if not taxa_id:
#             raise MissingKeyException("No taxa {}".format(taxa_id))
#
#         ret = None
#
#         with session_scope(self.session) as db:
#             from backbone_server.study.base import PartnerSpeciesIdentifier,Taxonomy
#
#             db_items = None
#             db_items = db.query(self.db_class).\
#                     join(self.db_class.original_sample).\
#                     join(OriginalSample.partner_species).\
#                     join(PartnerSpeciesIdentifier.taxa).\
#                     filter(Taxonomy.id==taxa_id)
#
#             ret = self._get_multiple_results(db, db_items, start, count,
#             studies=studies)
#
#             if ret.count == 0:
#                 db_item = db.query(Taxonomy).get(taxa_id)
#
#                 if not db_item:
#                     raise MissingKeyException("No taxa_id {}".format(taxa_id))
#         return ret
#
#     def get_by_study(self, study_name, studies, start, count):
#
#         if not study_name:
#             raise MissingKeyException(f"No study_name to get {self.db_class.__table__}")
#
#         if study_name and studies:
#             self.has_study_permission(studies,
#                                       study_name,
#                                       self.GET_PERMISSION)
#
#         ret = None
#
#         with session_scope(self.session) as db:
#
#             db_items = None
#             db_items = db.query(self.db_class).\
#                     join(self.db_class.original_sample).\
#                     filter(OriginalSample.study.has(code=study_name[:4]))
#
#             ret = self._get_multiple_results(db, db_items, start, count,
#             studies=studies)
#
#             if ret.count == 0:
#                 db_item = db.query(Study).filter_by(code=study_name[:4]).first()
#                 if not db_item:
#                     raise MissingKeyException(f'No such study {study_name}')
#
#         return ret
#
#     def get_by_event_set(self, event_set_name, studies, start, count):
#
#         if not event_set_name:
#             raise MissingKeyException("No event_set_name {}".format(event_set_name))
#
#         ret = None
#
#         with session_scope(self.session) as db:
#             from backbone_server.event_set.base import EventSet
#
#             db_items = db.query(self.db_class).\
#                     join(self.db_class.original_sample).\
#                     join(EventSet.members).\
#                     filter(EventSet.event_set_name==event_set_name)
#
#             ret = self._get_multiple_results(db, db_items, start, count,
#             studies=studies)
#
#             if ret.count == 0:
#                 db_item = db.query(EventSet).filter(EventSet.event_set_name==event_set_name).first()
#
#                 if not db_item:
#                     raise MissingKeyException("No event_set_name {}".format(event_set_name))
#         return ret
#
    def get_by_os_attr(self, attr_type, attr_value, study_name, value_type, start,
                       count, studies):

        if not attr_type:
            raise MissingKeyException(f"No attr_type to get {self.db_class.__table__}")

        if study_name and studies:
            self.has_study_permission(studies,
                                      study_name,
                                      self.GET_PERMISSION)

        ret = None

        with session_scope(self.session) as db:
            from backbone_server.model.original_sample import original_sample_attr_table

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

            db_items = None
            if study_name:
                study_codes = self.study_filter(studies)

                if study_codes:
                    if study_name[:4] not in study_codes:
                        raise PermissionException(f'No allowed to access {study_name}')

                os_study = aliased(OriginalSample.study)
                db_items = db.query(self.db_class).\
                        join(self.db_class.derivative_sample).\
                        join(OriginalSample).\
                        join(original_sample_attr_table,
                             and_(original_sample_attr_table.c.original_sample_id == DerivativeSample.original_sample_id,
                                  original_sample_attr_table.c.attr_id.in_(attrs))).\
                        outerjoin(Study).\
                        outerjoin(os_study, OriginalSample.study_id == os_study.id).\
                        filter(or_(Study.code == study_name[:4],
                                   os_study.code == study_name[:4]))
            else:
                db_items = db.query(self.db_class).\
                        join(self.db_class.derivative_sample).\
                        join(OriginalSample).\
                        join(original_sample_attr_table,
                             and_(original_sample_attr_table.c.original_sample_id == DerivativeSample.original_sample_id,
                                  original_sample_attr_table.c.attr_id.in_(attrs)))
            # db_item = db.query(self.db_class).filter_by(id=item_id).first()

            ret = self._get_multiple_results(db, db_items, start, count,
                                             studies=studies)

        return ret
