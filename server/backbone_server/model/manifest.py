import json

from sqlalchemy import Integer, String, ForeignKey, DateTime, Date, func, UniqueConstraint
from sqlalchemy import Table, MetaData, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, foreign
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from sqlalchemy.types import ARRAY, JSON
from sqlalchemy.ext.declarative import declared_attr

from openapi_server.encoder import JSONEncoder

from openapi_server.models.manifest import Manifest as ApiManifest
from openapi_server.models.manifests import Manifests
from openapi_server.models.manifest_item import ManifestItem as ManifestItemApi
from openapi_server.models.manifest_items import ManifestItems
from openapi_server.models.original_sample import OriginalSample as OriginalSampleApi
from openapi_server.models.derivative_sample import DerivativeSample as ApiDerivativeSample
from openapi_server.models.assay_data import AssayData
from openapi_server.models.studies import Studies

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.model.scope import session_scope

from backbone_server.model.mixins import Base
from backbone_server.model.attr import Attr
from backbone_server.model.document import Document
from backbone_server.model.manifest_note import ManifestNote

from backbone_server.model.derivative_sample import DerivativeSample
from backbone_server.model.original_sample import OriginalSample, BaseOriginalSample
from backbone_server.model.assay_data import AssayDatum, BaseAssayDatum
from backbone_server.model.history_meta import Versioned, versioned_session
from backbone_server.model.base import SimsDbBase

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

manifest_attr_table = Table('manifest_attr', Base.metadata,
                           Column('manifest_id', UUID(as_uuid=True),
                                  ForeignKey('manifest.id')),
                           Column('attr_id', UUID(as_uuid=True),
                                  ForeignKey('attr.id'))
                           )


manifest_item_attr_table = Table('manifest_item_attr', Base.metadata,
                                Column('manifest_item_id', UUID(as_uuid=True),
                                       ForeignKey('manifest_item.id')),
                                Column('attr_id', UUID(as_uuid=True),
                                       ForeignKey('attr.id'))
                                )


class ManifestItem(Versioned, Base):


    @declared_attr
    def __tablename__(cls):
        return 'manifest_item'

    original_sample_id = Column('original_sample_id',
                                UUID(as_uuid=True),
                                ForeignKey('original_sample.id'))
    manifest_id = Column('manifest_id',
                         UUID(as_uuid=True),
                         ForeignKey('manifest.id'))
    original_sample_version = Column(Integer)
    original_sample = Column(JSON)
    assay_data = Column(JSON)


    attrs = relationship("Attr", secondary=manifest_item_attr_table)

    openapi_class = ManifestItemApi
    openapi_multiple_class = ManifestItems

    def submapped_items(self):
        return {
            'attrs': Attr,
            'original_sample': str,
            'assay_data': str
        }

    def __repr__(self):
        return f'''<Manifest Item ID {self.id}
    {self.manifest_id}
    {self.original_sample_id}
    {self.original_sample_version}
    {self.original_sample}
    assay data {self.assay_data}
    {self.attrs}
    >'''

class Manifest(Versioned, Base):

    manifest_name = Column(String(128), index=True)
    manifest_type = Column(String(32), index=True)
    manifest_date = Column(Date)
    studies = Column(JSON)

    manifest_number = Column(Integer, autoincrement=True)

    manifest_doc = Column('document_id',
                          UUID(as_uuid=True),
                          ForeignKey('document.id'))

    attrs = relationship("Attr", secondary=manifest_attr_table)
    notes = relationship("ManifestNote",
                         backref=backref('manifest'))

    openapi_class = ApiManifest
    openapi_multiple_class = Manifests

    def submapped_items(self):
        return {
            'manifest_item': ManifestItem,
            'attrs': Attr,
            'notes': ManifestNote
        }

    def __repr__(self):
        return f'''<Manifest ID {self.id}
    {self.manifest_name}
    {self.manifest_date}
    {self.studies}
    {self.attrs}
    Notes {self.notes}
    >'''


class BaseManifestItem(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.db_class = ManifestItem
        self.attr_link = manifest_item_attr_table
        self.api_id = 'manifest_item_id'


    def convert_to_id(self, db, item_id, **kwargs):

        if 'manifest_id' in kwargs and kwargs['manifest_id'] and\
            'original_sample_id' in kwargs and kwargs['original_sample_id']:

            manifest_name = kwargs['manifest_id']
            manifest_id = None

            db_query = db.query(Manifest).filter_by(manifest_name=manifest_name)
            db_item = db_query.first()
            if db_item:
                manifest_id = db_item.id
            else:
                raise MissingKeyException(f"Error manifest does not exist {manifest_name}")

            orig_samp_id = kwargs['original_sample_id']

            db_item = db.query(ManifestItem).filter(and_(ManifestItem.manifest_id == manifest_id,
                                                        ManifestItem.original_sample_id == orig_samp_id)).first()

            if db_item:
                item_id = db_item.id
            else:
                raise MissingKeyException(f"Error manifest does not exist {manifest_name}")

        return item_id

    def post_get_action(self, db, db_item, api_item, studies, multiple=False):

        api_item.original_sample = OriginalSampleApi.from_dict(json.loads(db_item.original_sample))
        if db_item.assay_data:
            api_item.assay_data = AssayData.from_dict(json.loads(db_item.assay_data))

        return api_item

    def db_map_actions(self, db, db_item, api_item, studies, **kwargs):
        if 'update_samples' in kwargs and kwargs['update_samples']:
            os_base = BaseOriginalSample(self.engine, self.session)
            os_item = os_base.get_no_close(db, api_item.original_sample_id, studies)
            os_json = json.dumps(os_item, ensure_ascii=False, cls=JSONEncoder)
            db_item.original_sample = os_json

            db_items = db.query(AssayDatum.id).\
                    join(DerivativeSample).\
                    filter(DerivativeSample.original_sample_id == os_item.original_sample_id)

            ad_ids = []
            for ad_id in db_items.all():
                ad_ids.append(ad_id)
            bse = BaseAssayDatum(self.engine, self.session)
            ad_recs = bse.gets_in_noclose(db, ad_ids, studies=studies, start=None, count=None)
            if ad_recs.derivative_samples:
                for ds_id, ds in ad_recs.derivative_samples.items():
                    ds.original_sample = None
            os_json = json.dumps(ad_recs, ensure_ascii=False, cls=JSONEncoder)
            db_item.assay_data = os_json

    def put_premap(self, db, api_item, db_item):
        # This is to ensure not mapped and as shouldn't be updated by put
        if hasattr(api_item.openapi_types, 'original_sample'):
            del api_item.openapi_types['original_sample']
        if hasattr(api_item.openapi_types, 'assay_data'):
            del api_item.openapi_types['assay_data']

    def get_by_manifest(self, manifest_name, studies, start, count):

        if not manifest_name:
            raise MissingKeyException("No event_set_name {}".format(manifest_name))

        ret = None

        with session_scope(self.session) as db:

            manifest = db.query(Manifest).filter_by(manifest_name=manifest_name).first()
            if not manifest:
                raise MissingKeyException("No manifest_name {}".format(manifest_name))

            from backbone_server.model.study import Study
            db_items = db.query(ManifestItem).\
                    join(OriginalSample).\
                    join(Study, Study.id == OriginalSample.study_id).\
                    filter(ManifestItem.manifest_id == manifest.id)

            ret = self._get_multiple_results(db, db_items, start, count,
                                             studies=studies)

        return ret

class BaseManifest(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=['study',
                                            'manifest',
                                            'document',
                                            'manifest_attr',
                                            'attr'])

        self.db_class = Manifest
        self.attr_link = manifest_attr_table
        self.api_id = 'manifest_id'

    def pre_post_check(self, db, api_item, studies):

        db_item = db.query(self.db_class).filter_by(manifest_name=api_item).first()

        if db_item:
            raise DuplicateKeyException(f"Error inserting manifest already exists {api_item}")

        new_api_item = self.db_class.openapi_class()
        new_api_item.manifest_name = api_item

        return new_api_item

    def convert_to_id(self, db, item_id):

        db_item = db.query(self.db_class).filter_by(manifest_name=item_id).first()

        if db_item:
            item_id = db_item.id
        else:
            raise MissingKeyException(f"Error manifest does not exist {item_id}")

        return item_id

    def convert_from_id(self, db, item_id):

        db_item = db.query(self.db_class.manifest_name).filter_by(id=item_id)

        return db_item.first()

    def post_get_action(self, db, db_item, api_item, studies, multiple=False):

        if db_item.studies:
            api_item.studies = Studies.from_dict(json.loads(db_item.studies))

        return api_item

    def db_map_actions(self, db, db_item, api_item, studies, **kwargs):
        if 'update_studies' in kwargs and kwargs['update_studies']:
            from backbone_server.model.study import BaseStudy
            db_items = db.query(OriginalSample.study_id).\
                    join(ManifestItem).\
                    filter(ManifestItem.manifest_id == db_item.id)

            study_ids = []
            for study_id in db_items.all():
                study_ids.append(study_id)
            bse = BaseStudy(self.engine, self.session)
            study_recs = bse.gets_in_noclose(db, study_ids, studies=studies, start=None, count=None)
            os_json = json.dumps(study_recs, ensure_ascii=False, cls=JSONEncoder)
            db_item.studies = os_json


    def put_premap(self, db, api_item, db_item):
        # This is to ensure not mapped and as shouldn't be updated by put
        if hasattr(api_item.openapi_types, 'studies'):
            del api_item.openapi_types['studies']

    def get_with_members(self, item_id, studies, start, count):

        if not item_id:
            raise MissingKeyException(f"No item id to get {self.db_class.__table__}")

        orig_item_id = item_id

        with session_scope(self.session) as db:

            item_id = self.convert_to_id(db, item_id)

            db_item = db.query(self.db_class).filter_by(id=item_id).first()

            if not db_item:
                raise MissingKeyException(f"Could not find {self.db_class.__table__} to get {item_id}")

            api_item = db_item.map_to_openapi()

            study_code = self.get_study_code(db_item)

            self.has_study_permission(studies,
                                      study_code,
                                      self.GET_PERMISSION)
            api_item = self.post_get_action(db, db_item, api_item, studies,
                                            False)


        bse = BaseManifestItem(self.engine, self.session)
        api_item.members = bse.get_by_manifest(orig_item_id, studies, start, count)

        return api_item


    def post_member(self, manifest_name, original_sample_id, user, studies):

        ri_item_id = None
        os_base = BaseOriginalSample(self.engine, self.session)
        bse = BaseManifestItem(self.engine, self.session)

        with session_scope(self.session) as db:

            os_item = os_base.get_no_close(db, original_sample_id, studies)

            if not os_item:
                raise MissingKeyException(f"original sample does not exist {original_sample_id}")

            manifest_id = self.convert_to_id(db, manifest_name)

            member = db.query(ManifestItem).filter(and_(ManifestItem.original_sample_id == original_sample_id,
                                                       ManifestItem.manifest_id == manifest_id)).first()
            if member:
                raise DuplicateKeyException(f"{original_sample_id} already in {manifest_name}")

            ri_item = ManifestItem()
            ri_item.manifest_id = manifest_id
            ri_item.original_sample_id = os_item.original_sample_id
            ri_item.original_sample_version = os_item.version
            ri_item.created_by = user
            api_item = ManifestItemApi(None,
                                      original_sample_id=original_sample_id)
            bse.db_map_actions(db, ri_item, api_item, studies,
                               update_samples=True)


            db.add(ri_item)

            db.commit()

            ri_item_id = ri_item.id

        ret = bse.get(ri_item_id, studies=studies)

        return ret

    def get_member(self, item_id, os_item, studies):

        if not item_id:
            raise MissingKeyException(f"No item id to get manifest member")

        if studies:
            self.has_study_permission(studies,
                                      os_item.study_name,
                                      self.GET_PERMISSION)
        api_item = ManifestItemApi()

        with session_scope(self.session) as db:


            db_item = db.query(ManifestItem).get(item_id)

            if not db_item:
                raise MissingKeyException(f"Could not find manifest_item to get {item_id}")

            api_item = self.post_get_action(db, db_item, api_item, studies,
                                            False)

            # print(db_item)
            # print(api_item)
        return api_item


    def delete_member(self, manifest_name, original_sample_id, studies):

        with session_scope(self.session) as db:
            db_item = db.query(self.db_class).filter_by(manifest_name=manifest_name).first()

            if not db_item:
                raise MissingKeyException(f"event set does not exist {manifest_name}")

            os_item = db.query(ManifestItem).filter(and_(ManifestItem.original_sample_id == original_sample_id,
                                                        ManifestItem.manifest_id == db_item.id)).first()

            if not os_item:
                raise MissingKeyException(f"manifest_item does not exist {original_sample_id}")

            db.delete(os_item)

        return None
