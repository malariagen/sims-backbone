from sqlalchemy import MetaData, Column
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Date, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, foreign
from sqlalchemy import and_

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from openapi_server.models.manifest_note import ManifestNote as ApiManifestNote

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.model.mixins import Base


from backbone_server.model.history_meta import Versioned
from backbone_server.model.base import SimsDbBase
from backbone_server.model.scope import session_scope

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException


class ManifestNote(Versioned, Base):

    @declared_attr
    def __tablename__(cls):
        return 'manifest_note'

    note_name = Column(String(128))
    note_text = Column(Text())

    manifest_id = Column('manifest_id',
                        UUID(as_uuid=True),
                        ForeignKey('manifest.id'))

    openapi_class = ApiManifestNote

    def submapped_items(self):
        return {
        }

    def __repr__(self):
        return f'''<ManifestNote
      {self.note_name}
      {self.note_text}
      '''

class BaseManifestNote(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=['manifest'])

        self.db_class = ManifestNote

    def pre_post_check(self, db, manifest_id, api_item, studies):

        db_item = db.query(self.db_class).filter(and_(ManifestNote.note_name == api_item.note_name,
                                                      ManifestNote.manifest_id == manifest_id)).first()

        if db_item:
            raise DuplicateKeyException(f"Error inserting event set note already exists {db_item.manifest.manifest_name} {api_item.note_name}")

        return api_item

    def post(self, manifest_id, api_item, study_name, studies, user):

        ret = None

        with session_scope(self.session) as db:

            api_item = self.pre_post_check(db, manifest_id, api_item, studies)

            db_item = self.db_class()
            db_item.map_from_openapi(api_item)

            self.db_map_actions(db, db_item, api_item, studies)
            self.db_map_attrs(db, db_item, api_item)

            db_item.manifest_id = manifest_id
            db_item.created_by = user

            db.add(db_item)

            self.post_extra_actions(api_item)
            db.commit()

            ret = self.get(self.convert_from_id(db, db_item.id), studies)

        return ret

    def pre_put_check(self, db, api_item, update_item):

        db_item = db.query(self.db_class).filter(and_(ManifestNote.note_name == api_item.note_name,
                                                      ManifestNote.manifest_id == update_item.manifest_id,
                                                      ~(ManifestNote.id == update_item.id))).first()

        if db_item:
            raise DuplicateKeyException(f"Error inserting event set note already exists {db_item.manifest.manifest_name} {api_item.note_name}")

        return api_item

    def put(self, manifest_id, input_item_id, api_item, studies, user):

        ret = None

        if not input_item_id:
            raise MissingKeyException(f"No item id to update {self.db_class.__table__}")

        with session_scope(self.session) as db:

            item_id = self.convert_to_id(db, input_item_id)

            #print(f'Looking for {item_id}')
            update_item = db.query(self.db_class).filter(and_(ManifestNote.note_name == item_id,
                                                              ManifestNote.manifest_id == manifest_id)).first()

            if not update_item:
                raise MissingKeyException(f"Could not find {self.db_class.__table__} to update {item_id}")

            self.pre_put_check(db, api_item, update_item)

            update_item.map_from_openapi(api_item)

            self.db_map_actions(db, update_item, api_item, studies)
            self.db_map_attrs(db, update_item, api_item)
            update_item.updated_by = user

            self.put_extra_actions(api_item)

            db.commit()

        # print(f'Return from put {ret}')
        return ret


    def delete(self, manifest_id, input_item_id, studies):

        if not input_item_id:
            raise MissingKeyException(f"No item id to delete {self.db_class.__table__}")

        with session_scope(self.session) as db:

            delete_item = db.query(self.db_class).filter(and_(ManifestNote.note_name == input_item_id,
                                                              ManifestNote.manifest_id == manifest_id)).first()

            if not delete_item:
                raise MissingKeyException(f"Could not find {self.db_class.__table__} to delete {input_item_id}")

            api_delete = delete_item.map_to_openapi()

            self.delete_extra_actions(db, delete_item, api_delete)

            db.delete(delete_item)
