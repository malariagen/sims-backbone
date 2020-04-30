
import os

from sqlalchemy import Column

from sqlalchemy import event
#from sqlalchemy.event import listen
from sqlalchemy import Integer, String

from openapi_server.models.country import Country as ApiCountry
from backbone_server.model.mixins import Base

class Country(Base):

    id = None
    english = Column(String())
    french = Column(String())
    alpha2 = Column(String(2))
    alpha3 = Column(String(3), primary_key=True)
    numeric_code = Column(Integer())

    openapi_class = ApiCountry

    def __repr__(self):
        return f'''<Country
    {self.alpha3}
    {self.alpha2}
    {self.english}
    >'''


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
