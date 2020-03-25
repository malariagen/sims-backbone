from sqlalchemy import MetaData, Column
from sqlalchemy import Integer, String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base

from openapi_server.models.document import Document as Doc
from openapi_server.models.documents import Documents
from backbone_server.model.mixins import Base
from backbone_server.model.attr import Attr
from backbone_server.document.file_util import FileUtil
from backbone_server.model.study import Study

from backbone_server.model.history_meta import Versioned
from backbone_server.model.base import SimsDbBase

class DocumentAttr(Base):

    __tablename__ = 'document_attr'

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
    created_by = Column(String(50))
    updated_by = Column(String(50))
    note = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


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
    Version {self.doc_version}
    >'''

class BaseDocument(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=['study'])

        self.db_class = Document
        self.attr_link = DocumentAttr

    def db_map_actions(self, db, db_item, api_item, studies):

        study = Study.get_or_create_study(db, api_item.study_name)
        db_item.study_id = study.id

    def post_get_action(self, db, db_item, api_item, studies, multiple=False):

        api_item.study_name = db_item.study.name

        return api_item

    def delete_extra_actions(self, db, delete_item, api_item):

        api_item.study_name = delete_item.study.name
        util = FileUtil()

        util.delete_file(api_item)

    def delete_get_study_name(self, delete_item):

        return delete_item.study.study_name


    def get_content(self, document_id, studies):

        doc = super().get(document_id, studies)

        util = FileUtil()

        return util.get_content(doc)

    def post_extra_actions(self, document):

        util = FileUtil()

        util.save_file(document)

    def put_content(self, document_id, studies):

        #doc = super().put(document_id, None, studies=studies)

        util = FileUtil()

        #return util.put_content(doc)
