import json
from sqlalchemy import MetaData, Column
from sqlalchemy import Integer, String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base

from openapi_server.models.document import Document as Doc
from openapi_server.models.documents import Documents

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.model.scope import session_scope
from backbone_server.model.mixins import Base
from backbone_server.model.attr import Attr
from backbone_server.document.file_util import FileUtil
from backbone_server.model.study import Study

from backbone_server.model.history_meta import Versioned
from backbone_server.model.base import SimsDbBase

class DocumentAttr(Base):

    __tablename__ = 'document_attr'

    id = None
    created_by = None
    updated_by = None
    action_date = None

    document_id = Column(UUID(as_uuid=True),
                         ForeignKey('document.id'),
                         primary_key=True)
    attr_id = Column(UUID(as_uuid=True),
                     ForeignKey('attr.id'), primary_key=True)

class Document(Versioned, Base):

    study_id = Column('study_id',
                      UUID(as_uuid=True),
                      ForeignKey('study.id'))
    doc_name = Column(String(50))
    doc_type = Column(String(50))
    doc_version = Column(String(50))
    mimetype = Column(String(256))
    content_type = Column(String(256))
    file_reference = Column(String(256))
    note = Column(String(256))


    __table_args__ = (UniqueConstraint('doc_name', 'doc_type',
                                       name='uniq_doc'),)
    study = relationship("Study", backref=backref("document", uselist=False))
    attrs = relationship("Attr", secondary='document_attr')

    openapi_class = Doc
    openapi_multiple_class = Documents

    def submapped_items(self):
        return {
            'study_name': 'study',
            'attrs': Attr
        }

    def __repr__(self):
        return f'''<Document Name {self.doc_name}
    Study Id {self.study_id}
    Study {self.study}
    Type {self.doc_type}
    Doc Version {self.doc_version}
    Version {self.version}
    Created by {self.created_by}
    Updated by {self.updated_by}
    >'''

class BaseDocument(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=['study'])

        self.db_class = Document
        self.attr_link = DocumentAttr

    def db_map_actions(self, db, db_item, api_item, studies, user, **kwargs):

        # Create
        if api_item.study_name:
            study = Study.get_or_create_study(db, api_item.study_name, user)
            db_item.study_id = study.id

    def post_get_action(self, db, db_item, api_item, studies, multiple=False):

        api_item.study_name = db_item.study.name

        return api_item

    def delete_extra_actions(self, db, delete_item, api_item):

        api_item.study_name = delete_item.study.name
        util = FileUtil()

        util.delete_file(delete_item)

    def delete_get_study_name(self, delete_item):

        return delete_item.study.study_name


    def get_content(self, document_id, studies):

        doc = None
        with session_scope(self.session) as db:
            doc = db.query(Document).filter_by(id=document_id).first()

            if not doc:
                raise MissingKeyException(f"Could not find {self.db_class.__table__} to get {document_id}")

            self.has_study_permission(studies,
                                      doc.study.code,
                                      self.GET_PERMISSION)

            util = FileUtil()

            return util.get_content(doc)

        return None

    def save_file(self, db_item, **kwargs):
        has_file = False
        file_storage = None
        doc_content = None
        validate_only = False
        if 'file_storage' in kwargs and kwargs['file_storage']:
            file_storage = kwargs['file_storage']
            has_file = True
        if 'doc_content' in kwargs and kwargs['doc_content']:
            doc_content = kwargs['doc_content']
            has_file = True
        if 'validate_only' in kwargs and kwargs['validate_only']:
            validate_only = kwargs['validate_only']
        if has_file:
            util = FileUtil()

            util.save_file(db_item, file_storage, doc_content, validate_only)

        return has_file

    def post_extra_actions(self, document, db_item, **kwargs):

        self.save_file(db_item, **kwargs)

    def put_extra_actions(self, api_item, db_item, **kwargs):

        has_file = self.save_file(db_item, **kwargs)

        #Only changed the metadata so make sure we keep document related values
        if not has_file:
            old_values = json.loads(db_item.pre_update_json)
            db_item.doc_name = old_values['doc_name']
            if 'content_type' in old_values:
                db_item.content_type = old_values['content_type']
            if 'mimetype' in old_values:
                db_item.mimetype = old_values['mimetype']
