from sqlalchemy.sql import func
from sqlalchemy import Table, MetaData, Column
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.types import JSON


from openapi_server.models.log_item import LogItem
from openapi_server.models.log_items import LogItems
from openapi_server.models.output_value import OutputValue

from backbone_server.model.scope import session_scope

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.model.mixins import Base

class Archive(Base):

    id = Column(Integer(), primary_key=True)
    submitter = Column(String(64))
    action_id = Column(String(64))
    entity_id = Column(String(64))
    input_value = Column(Text())
    output_value = Column(JSON())
    result_code = Column(Integer())
    action_date = Column(DateTime(), server_default=func.now())

    def __repr__(self):
        return f'''<Archive ID {self.id}
    {self.submitter}
    {self.action_date}
    {self.action_id}
    {self.result_code}
    >'''

class BaseArchive():

    def __init__(self, engine, session):

        self.session = session
        self.engine = engine

        self.metadata = MetaData(bind=engine)
        Base.metadata.create_all(bind=engine)

        self.metadata.reflect(engine, only=[
            'archive'
        ])

        self.db_class = Archive
        self.openapi_class = LogItem
        self.openapi_multiple_class = LogItems
        self.api_id = 'id'
