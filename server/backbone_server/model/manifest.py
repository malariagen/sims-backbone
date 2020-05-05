import json

from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy import and_, Sequence
from sqlalchemy.types import JSON
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
from backbone_server.model.derivative_sample import DerivativeSample, BaseDerivativeSample
from backbone_server.model.assay_data import AssayDatum, BaseAssayDatum
from backbone_server.model.history_meta import Versioned
from backbone_server.model.base import SimsDbBase

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

class ManifestItemAttr(Base):

    __tablename__ = 'manifest_item_attr'

    id = None
    created_by = None
    updated_by = None
    action_date = None

    manifest_item_id = Column(UUID(as_uuid=True),
                              ForeignKey('manifest_item.id'),
                              primary_key=True)
    attr_id = Column(UUID(as_uuid=True),
                     ForeignKey('attr.id'), primary_key=True)

class ManifestAttr(Base):

    __tablename__ = 'manifest_attr'

    id = None
    created_by = None
    updated_by = None
    action_date = None

    manifest_id = Column(UUID(as_uuid=True),
                         ForeignKey('manifest.id'),
                         primary_key=True)
    attr_id = Column(UUID(as_uuid=True),
                     ForeignKey('attr.id'), primary_key=True)


class ManifestItem(Versioned, Base):


    @declared_attr
    def __tablename__(cls):
        return 'manifest_item'

    original_sample_id = Column('original_sample_id',
                                UUID(as_uuid=True),
                                ForeignKey('original_sample.id'))
    derivative_sample_id = Column('derivative_sample_id',
                                  UUID(as_uuid=True),
                                  ForeignKey('derivative_sample.id'))
    derivative_sample_version = Column(Integer)
    manifest_id = Column('manifest_id',
                         UUID(as_uuid=True),
                         ForeignKey('manifest.id'))
    original_sample_version = Column(Integer)
    original_sample = Column(JSON)
    assay_data = Column(JSON)


    attrs = relationship("Attr", secondary='manifest_item_attr')

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
    manifest id {self.manifest_id}
    OS id {self.original_sample_id}
    OS version {self.original_sample_version}
    {self.original_sample}
    DS id {self.derivative_sample_id}
    DS version {self.derivative_sample_version}
    assay data {self.assay_data}
    {self.attrs}
    >'''

class ManifestDocument(Base):

    __tablename__ = 'manifest_document'

    id = None
    created_by = None
    updated_by = None
    action_date = None

    manifest_id = Column(UUID(as_uuid=True),
                         ForeignKey('manifest.id'),
                         primary_key=True)
    document_id = Column(UUID(as_uuid=True),
                         ForeignKey('document.id'),
                         primary_key=True)

class Manifest(Versioned, Base):

    manifest_name = Column(String(128), index=True)
    manifest_type = Column(String(32), index=True)
    manifest_date = Column(Date)
    studies = Column(JSON)

    manifest_number = Column(Integer, Sequence('sims_manifest_num'), autoincrement="auto")

    manifest_file = Column('document_id',
                           UUID(as_uuid=True),
                           ForeignKey('document.id'))

    attrs = relationship("Attr", secondary='manifest_attr')
    notes = relationship("ManifestNote",
                         backref=backref('manifest'))

    related_docs = relationship("Document",
                                secondary=ManifestDocument.__table__)

    openapi_class = ApiManifest
    openapi_multiple_class = Manifests

    def submapped_items(self):
        return {
            'manifest_item': ManifestItem,
            'attrs': Attr,
            'notes': ManifestNote,
            'related_docs': None
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
        self.attr_link = ManifestItemAttr
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

    def db_map_related_docs(self, db, db_item, api_item, user):
        if hasattr(api_item, 'related_docs') and api_item.related_docs:
            related_docs = []
            for related_doc in api_item.related_docs:
                if related_doc.document_id in related_docs:
                    raise DuplicateKeyException(f'Error duplicate related_docs {related_doc}')
                related_docs.append(related_doc.document_id)
                db_related_doc = db.query(Document).filter_by(id=related_doc.document_id).first()
                if db_related_doc not in db_item.related_docs:
                    db_item.related_docs.append(db_related_doc)
            if related_docs:
                related_docs_to_remove = []
                for related_doc in db_item.related_docs:
                    if related_doc.id not in related_docs:
                        related_docs_to_remove.append(related_doc)
                for related_doc in related_docs_to_remove:
                    db_item.related_docs.remove(related_doc)
        elif hasattr(db_item, 'related_docs'):
            related_docs_to_remove = []
            for related_doc in db_item.related_docs:
                related_docs_to_remove.append(related_doc)
            for related_doc in related_docs_to_remove:
                db_item.related_docs.remove(related_doc)

    def db_map_actions(self, db, db_item, api_item, studies, user, **kwargs):

        self.db_map_related_docs(db, db_item, api_item, user)

        if 'update_samples' in kwargs and kwargs['update_samples']:

            os_base = BaseOriginalSample(self.engine, self.session)
            os_item = os_base.get_no_close(db, api_item.original_sample_id, studies)
            os_json = json.dumps(os_item, ensure_ascii=False, cls=JSONEncoder)
            db_item.original_sample = os_json

            if db_item.derivative_sample_id:
                db_items = db.query(AssayDatum.id).\
                        filter(AssayDatum.derivative_sample_id == db_item.derivative_sample_id)
            else:
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
        self.attr_link = ManifestAttr
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

    def db_map_actions(self, db, db_item, api_item, studies, user, **kwargs):
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

        self.db_map_notes(db, db_item, api_item, user)

    def db_map_notes(self, db, db_item, api_item, user):

        if api_item.notes:
            new_notes = []
            new_existing_notes = []
            note_ids = []
            notes = []
            remove_notes = []
            for note in api_item.notes:
                if note.note_name in notes:
                    raise DuplicateKeyException(f"Duplicate note {note.note_name}")
                db_note = db.query(ManifestNote).filter(and_(ManifestNote.note_name == note.note_name,
                                                             ManifestNote.manifest_id == db_item.id)).first()
                if db_note:
                    note_ids.append(db_note.id)
                    if db_note not in db_item.notes:
                        new_existing_notes.append(db_note)
                else:
                    new_note = ManifestNote()
                    new_note.note_name = note.note_name
                    new_note.note_text = note.note_text
                    new_note.created_by = user
                    new_notes.append(new_note)
            if new_existing_notes:
                db_item.notes.extend(new_existing_notes)
            for note in db_item.notes:
                if note.id not in note_ids:
                    remove_notes.append(note)
            for note in remove_notes:
                db_item.notes.remove(note)
            if new_notes:
                db_item.notes.extend(new_notes)


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

    def post_member(self, manifest_name, manifest_item, user, studies):

        ri_item_id = None
        os_base = BaseOriginalSample(self.engine, self.session)
        ds_base = BaseDerivativeSample(self.engine, self.session)
        bse = BaseManifestItem(self.engine, self.session)

        with session_scope(self.session) as db:

            manifest_id = self.convert_to_id(db, manifest_name)

            if manifest_item.derivative_sample_id:
                ds_item = ds_base.get_no_close(db, manifest_item.derivative_sample_id, studies)

                if not ds_item:
                    raise MissingKeyException(f"derivative_sample does not exist {manifest_item.derivative_sample_id}")

                if manifest_item.derivative_sample_version:
                    if manifest_item.derivative_sample_version > ds_item.version:
                        msg = f"derivative sample version does not exist {manifest_item.derivative_sample_id} {manifest_item.derivative_sample_version}"
                        raise MissingKeyException(msg)
                else:
                    manifest_item.derivative_sample_version = ds_item.version

                member = db.query(ManifestItem).filter(and_(ManifestItem.derivative_sample_id == manifest_item.derivative_sample_id,
                                                            ManifestItem.manifest_id == manifest_id)).first()
                if member:
                    raise DuplicateKeyException(f"{manifest_item.derivative_sample_id} already in {manifest_name}")

                if not manifest_item.original_sample_id:
                    manifest_item.original_sample_id = ds_item.original_sample_id

            if manifest_item.original_sample_id:
                os_item = os_base.get_no_close(db, manifest_item.original_sample_id, studies)

                if not os_item:
                    raise MissingKeyException(f"original sample does not exist {manifest_item.original_sample_id}")

                if manifest_item.original_sample_version:
                    if manifest_item.original_sample_version > os_item.version:
                        msg = f"original sample version does not exist {manifest_item.original_sample_id} {manifest_item.original_sample_version}"
                        raise MissingKeyException(msg)

                else:
                    manifest_item.original_sample_version = os_item.version

                member = db.query(ManifestItem).filter(and_(ManifestItem.original_sample_id == manifest_item.original_sample_id,
                                                            ManifestItem.manifest_id == manifest_id)).first()
                if member:
                    raise DuplicateKeyException(f"{manifest_item.original_sample_id} already in {manifest_name}")

            ri_item = ManifestItem()
            ri_item.manifest_id = manifest_id
            ri_item.created_by = user
            bse.db_map_actions(db, ri_item, manifest_item, studies, user,
                               update_samples=True)
            ri_item.original_sample_id = manifest_item.original_sample_id
            ri_item.original_sample_version = manifest_item.original_sample_version
            ri_item.derivative_sample_id = manifest_item.derivative_sample_id
            ri_item.derivative_sample_version = manifest_item.derivative_sample_version

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


    def delete_member(self, manifest_name, manifest_item_id, studies):

        with session_scope(self.session) as db:
            db_item = db.query(self.db_class).filter_by(manifest_name=manifest_name).first()

            if not db_item:
                raise MissingKeyException(f"event set does not exist {manifest_name}")

            os_item = db.query(ManifestItem).get(manifest_item_id)

            if not os_item:
                raise MissingKeyException(f"manifest_item does not exist {manifest_item_id}")

            db.delete(os_item)

        return None
