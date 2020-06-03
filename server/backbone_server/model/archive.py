import os

from sqlalchemy.sql import func
from sqlalchemy import MetaData, Column
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy import event
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

    openapi_class = LogItem
    openapi_multiple_class = LogItems

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
        self.api_id = 'id'

@event.listens_for(Archive.__table__, "after_create")
def setup_alembic(mapper, connection, checkfirst, _ddl_runner,
                  _is_metadata_operation):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    from alembic.config import Config
    from alembic import command
    file_path = os.path.join(dir_path, '..', 'alembic.ini')
    alembic_cfg = Config(file_path)
    script_path = os.path.join(dir_path, '..', 'alembic')
    alembic_cfg.set_main_option("script_location", script_path)
    from backbone_server.controllers.base_controller import BaseController
    url = BaseController.get_connection_url()
    alembic_cfg.set_main_option("sqlalchemy.url", url)

    command.stamp(alembic_cfg, "head")
