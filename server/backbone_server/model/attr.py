
from sqlalchemy import Column, Index
from sqlalchemy import String, Integer, Date, DateTime, Float, Numeric, ForeignKey
from sqlalchemy.types import ARRAY, JSON
from sqlalchemy import and_, or_
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship, backref

from backbone_server.model.mixins import Base
from backbone_server.model.study import Study

class Attr(Base):


    study_id = Column('study_id',
                      UUID(as_uuid=True),
                      ForeignKey('study.id'))
    attr_type = Column(String(256), index=True)
    attr_value_str = Column(String(256), index=True)
    attr_value_int = Column(Integer, index=True)
    attr_value_float = Column(Float, index=True)
    attr_value_decimal = Column(Numeric, index=True)
    attr_value_date = Column(Date, index=True)
    attr_value_datetime = Column(DateTime, index=True)
    attr_value_list_int = Column(ARRAY(Integer))
    attr_value_object = Column(JSON)
    attr_source = Column(String(256))

    study = relationship('Study',
                         backref=backref('attr'))

    def submapped_items(self):
        return {
            'study_name': 'study.name',
        }

    @staticmethod
    def get_query(db, api_attr, value_type=None):

        study_id = None
        if value_type:
            value_type = 'attr_value_' + value_type
        else:
            value_type = 'attr_value_' + type(api_attr.attr_value).__name__
            if value_type == 'attr_value_list':
                value_type = value_type + '_' + type(api_attr.attr_value[0]).__name__
        if isinstance(api_attr.attr_value, str):
            import urllib
            api_attr.attr_value = urllib.parse.unquote_plus(api_attr.attr_value)

        attr_query = db.query(Attr).filter(and_(Attr.attr_type == api_attr.attr_type,
                                                Attr.__table__.c[value_type] == api_attr.attr_value))
        if api_attr.attr_source:
            attr_query = attr_query.filter(or_(Attr.attr_source == api_attr.attr_source, Attr.attr_source == None))
        if api_attr.study_name:
            study = Study.get_or_create_study(db, api_attr.study_name)
            study_id = study.id
            attr_query = attr_query.filter(or_(Attr.study_id == study_id, Attr.study_id == None))

        return attr_query

    @staticmethod
    def get(db, api_attr, value_type=None):

        return Attr.get_query(db, api_attr, value_type).first()

    @staticmethod
    def get_or_create(db, api_attr, value_type=None):

        attr = Attr.get(db, api_attr, value_type)

        if attr is None:
            study_id = None
            if api_attr.study_name:
                study = Study.get_or_create_study(db, api_attr.study_name)
                study_id = study.id
            attr = Attr(attr_type=api_attr.attr_type,
                        attr_source=api_attr.attr_source,
                        study_id=study_id)
            if not value_type:
                value_type = 'attr_value_' + type(api_attr.attr_value).__name__
            setattr(attr, value_type, api_attr.attr_value)
            db.add(attr)
            db.commit()
            attr = Attr.get(db, api_attr)

        return attr

    @staticmethod
    def get_all(db, api_attr, value_type=None):

        for attr in Attr.get_query(db, api_attr, value_type).all():
            yield attr

    study = relationship("Study")
    def __repr__(self):
        return f'''<Attr Type {self.attr_type}
    Study Id {self.study_id}
    Value {self.attr_value_str}
    Value {self.attr_value_int}
    {self.attr_value_float}
    {self.attr_value_decimal}
    {self.attr_value_date}
    {self.attr_value_datetime}
    {self.attr_value_list_int}
    {self.attr_value_object}
    Source {self.attr_source}
    >'''

Index('idx_attr_index', Attr.attr_type, Attr.attr_value_str)
