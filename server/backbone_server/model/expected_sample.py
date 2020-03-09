from sqlalchemy import Table, MetaData, Column
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from backbone_server.model.mixins import Base
from backbone_server.original_sample.base import PartnerSpeciesIdentifier

class ExpectedSample(Base):
    @declared_attr
    def __tablename__(cls):
        return 'expected_sample'

    sample_count = Column(Integer())
    date_of_arrival = Column(DateTime())
    study_id = Column('study_id',
                      UUID(as_uuid=True),
                      ForeignKey('study.id'))
    partner_species_id = Column('partner_species_id',
                                UUID(as_uuid=True),
                                ForeignKey('partner_species_identifier.id'))
    study = relationship("Study", backref=backref("expected_sample",
                                                  uselist=False))
    partner_species = relationship("PartnerSpeciesIdentifier", backref=backref("expected_sample", uselist=False))

    def submapped_items(self):
        return {
            'partner_species': 'partner_species_identifier',
            'study_name': 'study'
        }

    def __repr__(self):
        return f'''<ExpectedSample ID {self.id}
    Study {self.study}
    Partner Species {self.partner_species}
    {self.sample_count}
    {self.date_of_arrival}
    >'''
