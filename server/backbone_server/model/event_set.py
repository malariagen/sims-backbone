from sqlalchemy import MetaData, Column
from sqlalchemy import Integer, String, ForeignKey, DateTime, Date, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, foreign
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from openapi_server.models.event_set import EventSet as ApiEventSet
from openapi_server.models.event_sets import EventSets
from openapi_server.models.sampling_events import SamplingEvents

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.model.scope import session_scope

from backbone_server.model.mixins import Base
from backbone_server.model.attr import Attr
from backbone_server.model.event_set_note import EventSetNote

from backbone_server.model.sampling_event import SamplingEvent, BaseSamplingEvent

from backbone_server.model.history_meta import Versioned, versioned_session
from backbone_server.model.base import SimsDbBase

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

class EventSetAttr(Base):

    __tablename__ = 'event_set_attr'

    id = None
    created_by = None
    updated_by = None
    action_date = None

    event_set_id = Column(UUID(as_uuid=True), ForeignKey('event_set.id'),
                          primary_key=True)
    attr_id = Column(UUID(as_uuid=True),
                     ForeignKey('attr.id'), primary_key=True)

#event_set_members_table = Table('event_set_member', Base.metadata,

class EventSetMember(Base):

    __tablename__ = 'event_set_member'

    event_set_id = Column(UUID(as_uuid=True), ForeignKey('event_set.id'),
                          primary_key=True)
    sampling_event_id = Column(UUID(as_uuid=True),
                               ForeignKey('sampling_event.id'), primary_key=True)

#event_set_members_table = Table('event_set_member', Base.metadata,
#                                Column('event_set_id', UUID(as_uuid=True),
#                                       ForeignKey('event_set.id')),
#                                Column('sampling_event_id', UUID(as_uuid=True),
#                                       ForeignKey('sampling_event.id'))
#                                )
#

class EventSet(Versioned, Base):

    @declared_attr
    def __tablename__(cls):
        return 'event_set'

    event_set_name = Column(String(128), index=True)


    attrs = relationship("Attr", secondary='event_set_attr')
    members = relationship("SamplingEvent",
                           secondary='event_set_member')
    notes = relationship("EventSetNote",
                         backref=backref('event_set'))

    openapi_class = ApiEventSet
    openapi_multiple_class = EventSets

    def submapped_items(self):
        return {
            'sampling_event': SamplingEvent,
            'members': SamplingEvents,
            'attrs': Attr,
            'notes': EventSetNote
        }

    def __repr__(self):
        return f'''<EventSet ID {self.id}
    {self.event_set_name}
    {self.attrs}
    {self.members}
    Notes {self.notes}
    >'''


class BaseEventSet(SimsDbBase):

    def __init__(self, engine, session):

        super().__init__(engine, session)

        self.metadata.reflect(engine, only=['study',
                                            'event_set',
                                            'individual',
                                            'event_set_attr',
                                            'attr'])

        self.db_class = EventSet
        self.attr_link = EventSetAttr

    def pre_post_check(self, db, api_item, studies):

        db_item = db.query(self.db_class).filter_by(event_set_name=api_item).first()

        if db_item:
            raise DuplicateKeyException(f"Error inserting event set already exists {api_item}")

        new_api_item = self.db_class.openapi_class()
        new_api_item.event_set_name = api_item

        return new_api_item

    def convert_to_id(self, db, item_id):

        db_item = db.query(self.db_class).filter_by(event_set_name=item_id).first()

        if db_item:
            item_id = db_item.id
        else:
            raise MissingKeyException(f"Error event set does not exist {item_id}")

        return item_id

    def convert_from_id(self, db, item_id):

        db_item = db.query(self.db_class.event_set_name).filter_by(id=item_id)

        return db_item.first()

    # This is more complicated than usual
    # Possible to add sampling event members via post/put
    # Possible to create/remove new notes via post/put
    def db_map_actions(self, db, db_item, api_item, studies):

        if api_item.members:
            new_members = []
            member_ids = []
            members = []
            remove_members = []
            for sampling_event in api_item.members.sampling_events:
                if sampling_event.sampling_event_id in members:
                    raise DuplicateKeyException(f"Duplicate member {sampling_event.sampling_event_id}")
                member_ids.append(sampling_event.sampling_event_id)
                se = db.query(SamplingEvent).filter(SamplingEvent.id == sampling_event.sampling_event_id).first()
                if se:
                    if se not in db_item.members:
                        new_members.append(se)
                else:
                    raise MissingKeyException(f"No such member {sampling_event.sampling_event_id}")
            if new_members:
                db_item.members.extend(new_members)
            for sampling_event in db_item.members:
                if str(sampling_event.id) not in member_ids:
                    remove_members.append(sampling_event)
            for sampling_event in remove_members:
                db_item.members.remove(sampling_event)

        # print(api_item)
        # print(db_item)
        # self.db_map_notes(db, db_item, api_item)

    def db_map_notes(self, db, db_item, api_item):

        if api_item.notes:
            new_notes = []
            new_existing_notes = []
            note_ids = []
            notes = []
            remove_notes = []
            for note in api_item.notes:
                if note.note_name in notes:
                    raise DuplicateKeyException(f"Duplicate note {note.note_name}")
                db_note = db.query(EventSetNote).filter(and_(EventSetNote.note_name == note.note_name,
                                                             EventSetNote.event_set_id == db_item.id)).first()
                if db_note:
                    note_ids.append(db_note.id)
                    if db_note not in db_item.notes:
                        new_existing_notes.append(se)
                else:
                    new_note = EventSetNote()
                    new_note.note_name = note.note_name
                    new_note.note_text = note.note_text
                    new_notes.append(new_note)
            if new_existing_notes:
                db_item.notes.extend(new_existing_notes)
            for note in db_item.notes:
                if note.id not in note_ids:
                    remove_notes.append(note)
            for note in remove_notes:
                db_item.notes.remove(note)
            if new_notes:
                db_item.notes.extend(new_notes)


    def get_with_members(self, item_id, studies, start, count):

        if not item_id:
            raise MissingKeyException(f"No item id to get {self.db_class.__table__}")

        orig_item_id = item_id

        with session_scope(self.session) as db:

            item_id = self.convert_to_id(db, item_id)

            db_item = db.query(self.db_class).filter_by(id=item_id).first()

            if not db_item:
                raise MissingKeyException(f"Could not find {self.db_class.__table__} to get {item_id}")

            api_item = db_item.map_to_openapi()

            study_code = self.get_study_code(db_item)

            self.has_study_permission(studies,
                                      study_code,
                                      self.GET_PERMISSION)

            api_item = self.post_get_action(db, db_item, api_item, studies,
                                            False)

        bse = BaseSamplingEvent(self.engine, self.session)
        api_item.members = bse.get_by_event_set(orig_item_id, studies, start,
                                                count)
        return api_item


    def post_member(self, event_set_name, sampling_event_id, studies):

        with session_scope(self.session) as db:
            db_item = db.query(self.db_class).filter_by(event_set_name=event_set_name).first()

            if not db_item:
                raise MissingKeyException(f"event set does not exist {event_set_name}")

            se_item = db.query(SamplingEvent).get(sampling_event_id)

            if not se_item:
                raise MissingKeyException(f"event set does not exist {sampling_event_id}")

            member = db.query(EventSetMember).\
                                filter(and_(EventSetMember.sampling_event_id == sampling_event_id,
                                            EventSetMember.event_set_id == db_item.id)).first()
            if member:
                raise DuplicateKeyException(f"{sampling_event_id} already in {event_set_name}")

            member_item = EventSetMember(sampling_event_id=sampling_event_id,
                                         event_set_id=db_item.id)
            db.add(member_item)

            db.commit()

        return None


    def delete_member(self, event_set_name, sampling_event_id, studies):

        with session_scope(self.session) as db:
            db_item = db.query(self.db_class).filter_by(event_set_name=event_set_name).first()

            if not db_item:
                raise MissingKeyException(f"event set does not exist {event_set_name}")

            se_item = db.query(SamplingEvent).get(sampling_event_id)

            if not se_item:
                raise MissingKeyException(f"sampling_event does not exist {sampling_event_id}")

            if se_item not in db_item.members:
                raise MissingKeyException(f'Sampling event not found in event set {event_set_name}')

            db_item.members.remove(se_item)
            try:
                db.commit()
            except IntegrityError:
                raise MissingKeyException(f"sampling_event does not exist {sampling_event_id} {event_set_name}")

        return None
