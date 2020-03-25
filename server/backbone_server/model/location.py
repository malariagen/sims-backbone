import os

from sqlalchemy import and_
from sqlalchemy import MetaData, Column
from sqlalchemy import Integer, String, ForeignKey, DateTime, Date, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, foreign

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy import event, DDL
from sqlalchemy.event import listen

from geoalchemy2 import Geometry
from openapi_server.models.location import Location as ApiLocation
from openapi_server.models.locations import Locations

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.model.scope import session_scope

from backbone_server.model.mixins import Base
from backbone_server.model.attr import Attr
from backbone_server.model.study import Study, PartnerSpeciesIdentifier

from backbone_server.model.history_meta import Versioned, versioned_session
from backbone_server.model.base import SimsDbBase


class Country(Base):

    id = None
    english = Column(String())
    french = Column(String())
    alpha2 = Column(String(2))
    alpha3 = Column(String(3), primary_key=True)
    numeric_code = Column(Integer())


@event.listens_for(Country.__table__, "after_create")
def insert_countries(mapper, connection, checkfirst, _ddl_runner,
                     _is_metadata_operation):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'data', 'country_codes.tsv')

    with connection.connection.cursor() as cur:
        with open(file_path) as fp:
            fp.readline()
            # Default sep is tab
            cur.copy_from(fp, 'country', columns=('english', 'french', 'alpha2',
                                                  'alpha3', 'numeric_code'))
    connection.connection.commit()

class LocationAttr(Base):

    __tablename__ = 'location_attr'

    location_id = Column(UUID(as_uuid=True),
                         ForeignKey('location.id'),
                         primary_key=True)
    attr_id = Column(UUID(as_uuid=True),
                     ForeignKey('attr.id'), primary_key=True)

class Location(Versioned, Base):

    country = Column(String(3))
    location = Column(Geometry('POINT'), index=True)
    accuracy = Column(String())
    curated_name = Column(String())
    curation_method = Column(String())
    notes = Column(String())

    proxy_location_id = Column('proxy_location_id',
                               UUID(as_uuid=True),
                               ForeignKey('location.id'))

    attrs = relationship("Attr", secondary='location_attr')

    openapi_class = ApiLocation
    openapi_multiple_class = Locations

    def submapped_items(self):
        return {
            'attrs': Attr
        }

    def __repr__(self):
        return f'''<Location ID {self.id}
    {self.country}
    {self.curated_name}
    {self.location}
    >'''


event.listen(Location.__table__, 'before_create',
             DDL("CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;")
            )



class BaseLocation(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=['study',
                                            'location',
                                            'individual',
                                            'location_attr',
                                            'attr'])

        self.db_class = Location
        self.attr_link = LocationAttr
        self.api_id = 'location_id'
        self.duplicate_attrs = ['partner_name']


    def check_name(self, api_item, studies):

        api_studies = []
        if api_item.attrs:
            for attr in api_item.attrs:
                if attr.attr_type == 'partner_name':
                    if not attr.study_name:
                        raise MissingKeyException(f'partner name attr must have a study code')
                    if attr.study_name[:4] in api_studies:
                        raise DuplicateKeyException(f'Duplicate partner name for study {attr.study_name}')
                    api_studies.append(attr.study_name[:4])

                    # existing = self.get_by_attr('partner_name',
                    #                             attr.attr_value,
                    #                             attr.study_name, studies, None,
                    #                             None)

                    # for exists in existing.locations:
                    #     if api_item.location_id:
                    #         if exists.location_id == api_item.location_id:
                    #             continue
                    #     raise DuplicateKeyException(f'Duplicate partner name {attr.attr_value} for study {attr.study_name}')




    def check_gps(self, db, api_item):

        if api_item.location_id:
            db_item = self.lookup_query(db).filter(and_(func.ST_X(Location.location) == api_item.latitude,
                                                        func.ST_Y(Location.location) == api_item.longitude,
                                                        ~Location.id == api_item.id)).first()
        else:
            db_item = self.lookup_query(db).filter(and_(func.ST_X(Location.location) == api_item.latitude,
                                                        func.ST_Y(Location.location) == api_item.longitude)).first()

        if db_item:
            raise DuplicateKeyException(f'Duplicate of {api_item.latitude} {api_item.longitude}')

    def pre_post_check(self, db, api_item, studies):
        self.check_name(api_item, studies)
        # self.check_gps(db, api_item)

        return api_item

    def pre_put_check(self, db, api_item, studies):
        self.check_name(api_item, studies)
        # self.check_gps(db, api_item)

        return api_item


    def db_map_actions(self, db, db_item, api_item, studies):

        if api_item.latitude == None or api_item.longitude == None:
            return

        db_item.location = f'POINT({api_item.latitude} {api_item.longitude})'

    def lookup_query(self, db):

        return db.query(self.db_class,
                        func.ST_X(Location.location).label('latitude'),
                        func.ST_Y(Location.location).label('longitude'))

    def map_multiple_results(self, db_items):
        loc_item = db_items[0]
        api_item = loc_item.map_to_openapi()
        api_item.latitude = db_items[1]
        api_item.longitude = db_items[2]

        return api_item

    def get_by_gps(self, lat, lng, studies, start, count):

        if not lat or not lng:
            raise MissingKeyException(f"No item id to get {self.db_class.__table__}")

        ret = None

        with session_scope(self.session) as db:

            db_query = self.lookup_query(db).filter(and_(func.ST_X(Location.location) == lat, func.ST_Y(Location.location) == lng))

            ret = self._get_multiple_results(db, db_query, start, count,
                                             studies=studies)

            if ret.count == 0:
                raise MissingKeyException(f"GPS location not found {lat}, {lng}")

        return ret

    def gets(self, study_name, studies, start, count, order_by):

        ret = None

        with session_scope(self.session) as db:

            db_items = None
            db_items = self.lookup_query(db)

            ret = self._get_multiple_results(db, db_items, start, count,
                                             studies=studies)

        return ret

    def get_by_study(self, study_name, start, count, studies):

        if not study_name:
            raise MissingKeyException(f"No study_name to get {self.db_class.__table__}")

        if study_name and studies:
            self.has_study_permission(studies,
                                      study_name,
                                      self.GET_PERMISSION)

        ret = None

        with session_scope(self.session) as db:

            from sqlalchemy.orm import aliased
            from backbone_server.model.sampling_event import SamplingEvent
            from backbone_server.model.original_sample import OriginalSample
            os_study = aliased(OriginalSample.study)

            db_items = self.lookup_query(db).\
                    join(SamplingEvent, SamplingEvent.location_id == Location.id).\
                    join(OriginalSample).\
                    outerjoin(os_study, OriginalSample.study_id == os_study.id).\
                    filter(os_study.code == study_name[:4]).\
                    distinct(Location.id)

            ret = self._get_multiple_results(db, db_items, start, count,
                                             studies=studies)

            if ret.count == 0:
                db_item = db.query(Study).filter_by(code=study_name[:4]).first()
                if not db_item:
                    raise MissingKeyException(f'No such study {study_name}')


        return ret
