from datetime import datetime

from sqlalchemy import and_
from sqlalchemy import Table, MetaData, Column
from sqlalchemy import Integer, String, ForeignKey, DateTime, Date, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, foreign

from openapi_server.models.individual import Individual as ApiIndividual
from openapi_server.models.individuals import Individuals

from backbone_server.model.scope import session_scope

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.model.mixins import Base
from backbone_server.model.attr import Attr
from backbone_server.model.study import Study

from backbone_server.model.history_meta import Versioned
from backbone_server.model.base import SimsDbBase

individual_attr_table = Table('individual_attr', Base.metadata,
                              Column('individual_id', UUID(as_uuid=True),
                                     ForeignKey('individual.id')),
                              Column('attr_id', UUID(as_uuid=True),
                                     ForeignKey('attr.id'))
                              )

class Individual(Versioned, Base):

    individual_ident = Column(String(30))

    attrs = relationship("Attr", secondary=individual_attr_table)

    def submapped_items(self):
        return {
            # 'partner_species': 'partner_species.partner_species',
#            'location': Location,
#            'study_name': 'study.name',
            'attrs': Attr
        }

    def __repr__(self):
        return f'''<Individual ID {self.id}
    {self.individual_id}
    >'''

class BaseIndividual(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=[
            'sampling_event'
        ])

        self.db_class = Individual
        self.openapi_class = ApiIndividual
        self.openapi_multiple_class = Individuals
        self.attr_class = Attr
        self.study_class = Study
        self.attr_link = individual_attr_table
        self.api_id = 'individual_id'
        self.duplicate_attrs = []

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
                    join(individual_attr_table).\
                    join(Attr).\
                    filter(Attr.study.has(code=study_name[:4]))

            ret = self._get_multiple_results(db, db_items, studies, start, count)

        return ret

    def merge(self, into, merged, studies):

        ret = None

        with session_scope(self.session) as db:

            individual1 = self.lookup_query(db).filter_by(id=into).first()

            if not individual1:
                raise MissingKeyException("No individual {}".format(into))

            if into == merged:
                return self.get(into, studies)

            individual2 = self.lookup_query(db).filter_by(id=merged).first()

            if not individual2:
                raise MissingKeyException("No individual {}".format(merged))

            if individual2.attrs:
                for new_ident in individual2.attrs:
                    found = False
                    for existing_ident in individual1.attrs:
                        if new_ident == existing_ident:
                            found = True
                    if not found:
                        new_ident_value = True
                        individual1.attrs.append(new_ident)

            db.commit()
            self.delete(merged, studies)


        return self.get(into, studies)
