
from sqlalchemy import Column, Index
from sqlalchemy import String, ForeignKey
from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship, backref

from backbone_server.model.mixins import Base
from backbone_server.model.study import Study

class Attr(Base):


    study_id = Column('study_id',
                      UUID(as_uuid=True),
                      ForeignKey('study.id'))
    attr_type = Column(String(256), index=True)
    attr_value = Column(String(256), index=True)
    attr_source = Column(String(256))

    study = relationship('Study',
                         backref=backref('attr'))

    def submapped_items(self):
        return {
            'study_name': 'study.name',
        }

    @staticmethod
    def get(db, api_attr):

        study_id = None
        if api_attr.study_name:
            study = Study.get_or_create_study(db, api_attr.study_name)
            study_id = study.id
        attr = db.query(Attr).filter_by(attr_type=api_attr.attr_type,
                                        attr_value=api_attr.attr_value,
                                        study_id=study_id,
                                        attr_source=api_attr.attr_source).first()

        return attr

    @staticmethod
    def get_or_create(db, api_attr):

        attr = Attr.get(db, api_attr)

        if attr is None:
            study_id = None
            if api_attr.study_name:
                study = Study.get_or_create_study(db, api_attr.study_name)
                study_id = study.id
            attr = Attr(attr_type=api_attr.attr_type,
                        attr_value=api_attr.attr_value,
                        attr_source=api_attr.attr_source,
                        study_id=study_id)
            db.add(attr)
            db.commit()
            attr = Attr.get(db, api_attr)

        return attr

    @staticmethod
    def get_all(db, api_attr):

        db_attr = db.query(Attr).\
                filter(and_((Attr.attr_type == api_attr.attr_type),\
                (Attr.attr_value == api_attr.attr_value),\
                (Attr.attr_source == api_attr.attr_source))).all()
        for attr in db_attr:
            yield attr

    study = relationship("Study")
    def __repr__(self):
        return f'''<Attr Type {self.attr_type}
    Study Id {self.study_id}
    Value {self.attr_value}
    Source {self.attr_source}
    >'''

Index('idx_attr_index', Attr.attr_type, Attr.attr_value)
