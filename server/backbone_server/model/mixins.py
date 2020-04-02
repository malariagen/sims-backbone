import logging
import uuid
import typing
import inspect
import json
from typing import List, Dict  # noqa: F401

from sqlalchemy import Column
from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base


from openapi_server.encoder import JSONEncoder

from openapi_server.models.base_model_ import Model

class Base(object):

    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(UUID(as_uuid=True), default=uuid.uuid4,
                primary_key=True)

    created_by = Column(String(64))
    updated_by = Column(String(64))
    action_date = Column(DateTime(), server_default=func.now())

    openapi_class = None
    openapi_multiple_class = None
    pre_update_json = None

    def get_id_key(self):
        name = self.__tablename__

        return name + '_id'

    def to_json(self, recurse=True):
        item = self.map_to_openapi(recurse)
        item_json = json.dumps(item, ensure_ascii=False, cls=JSONEncoder)

        return item_json

    def submapped_items(self):
        return {}

    def map_from_openapi_actions(self, api_item, user=None, **kwargs):
        pass

    def map_from_openapi(self, openapi_type, user=None, **kwargs):
        if not openapi_type:
            return
        id_val = self.get_id_key()
        if hasattr(openapi_type, id_val):
            setattr(self, 'id', getattr(openapi_type, id_val))
        if not hasattr(openapi_type, 'openapi_types'):
            return
        for key, value in openapi_type.openapi_types.items():
            if key in self.submapped_items().keys():
                subitem_descrip = self.submapped_items()[key]
                if hasattr(self, key):
                    self.logger.debug(f'{key} {value} {subitem_descrip}')
                    if isinstance(subitem_descrip, str):
                        self.logger.debug(f'String mapping {subitem_descrip}')
                        if hasattr(openapi_type, key):
                            if '[' in value:
                                self.logger.debug(f'Mapping List {key} {value}')
                                for item in getattr(openapi_type, key):
                                    db_item = subitem_descrip()
                                    db_item.map_from_openapi(item, user=user, **kwargs)
                            else:
                                self.logger.debug(f'Mapping {key} {value}')
                                setattr(self, key, getattr(openapi_type,
                                                           subitem_descrip))
                    elif not key == 'attr' and\
                            not isinstance(value, str) and issubclass(value, Model) and\
                            subitem_descrip and issubclass(subitem_descrip, Base):
                        db_item = subitem_descrip()
                        val = getattr(openapi_type, key)
                        if isinstance(val, object):
                            db_item.map_from_openapi(val, user=user, **kwargs)
                        else:
                            db_item.map_from_openapi(openapi_type, user=user, **kwargs)
                        self.logger.debug(f'Recurse {key} {subitem_descrip} {type(val)} {val} {db_item}')
                        if val:
                            setattr(self, key, db_item)
                    elif key not in ['attrs', 'members', 'partner_species'] and\
                             ((isinstance(value, str) and value.startswith('list['))
                              or (inspect.isclass(value) and issubclass(value, typing.List))):
                        self.logger.debug(f'Recurse list {key} {subitem_descrip} {type(getattr(openapi_type, key))} {value}')
                        sub_items = getattr(openapi_type, key)
                        self.logger.debug(f'{openapi_type} sub_items {sub_items}')
                        if sub_items:
                            sub_item_list = []
                            for api_subitem in sub_items:
                                self.logger.debug(api_subitem)
                                if isinstance(api_subitem, object):
                                    db_subitem = subitem_descrip()
                                    db_subitem.map_from_openapi(api_subitem,
                                                                user=user, **kwargs)
                                    sub_item_list.append(db_subitem)
                                    self.logger.debug(db_subitem)
                                self.logger.debug(db_subitem)
                            self.logger.debug(sub_item_list)
                            if sub_item_list:
                                setattr(self, key, sub_item_list)
                    else:
                        self.logger.debug(f'Mapping failed for {key} {value} {type(value)}')
            elif key not in ['version'] and (hasattr(self, key) and
                                             getattr(openapi_type, key)):
                setattr(self, key, getattr(openapi_type, key))
            elif hasattr(self, key):
                # if it's None
                setattr(self, key, getattr(openapi_type, key))
            else:
                self.logger.debug(f'No mapping: {self.__class__.__name__}:' + key)
        self.map_from_openapi_actions(openapi_type, user=user, **kwargs)

    def openapi_map_actions(self, api_item):
        pass

    def map_to_openapi(self, recurse=True):

        if not self.openapi_class:
            print(f'No class defined for {self.__class__.__name__}')
        openapi_type = self.openapi_class()

        # print(f'Mapping d2a: {self.__class__.__name__} {openapi_type}')
        # print(self)
        for key, value in openapi_type.openapi_types.items():
#            print(f'Looking for {key}')
            if key in self.submapped_items().keys():
#                print('submapped')
                subitem_descrip = self.submapped_items()[key]
                if isinstance(subitem_descrip, str):
                    sbi = subitem_descrip
                    sbk = key
                    if '.' in subitem_descrip:
                        (sbi, sbk) = subitem_descrip.split('.')
                    if hasattr(self, sbi):
                        item = getattr(self, sbi)
                        if hasattr(item, sbk):
                            setattr(openapi_type, key, getattr(item, sbk))
                elif issubclass(value, typing.List):
                   # and issubclass(subitem_descrip, Base):
                    # print('List map')
                    if recurse or key == 'attrs':
                        db_subitems = getattr(self, key)
                        api_list = []
                        for db_subitem in db_subitems:
                            # Slightly hacky to get the type of the list members
                            api_subitem = db_subitem.map_to_openapi()
                            # print(f'Recurse in list {key} {subitem_descrip} {type(api_subitem)}')
                            api_list.append(api_subitem)
                        # [] or None
                        if api_list:
                            setattr(openapi_type, key, api_list)
                elif issubclass(value, Model) and subitem_descrip and issubclass(subitem_descrip, Base):
                    if recurse or key == 'attrs':
                        db_item = subitem_descrip()
                        db_subitem = getattr(self, key)
                        # print(f'Recurse {key} {subitem_descrip} {type(getattr(openapi_type, key))} {value}')
                        if db_subitem:
                            api_subitem = db_subitem.map_to_openapi()
                            setattr(openapi_type, key, api_subitem)
                else:
                    # print(f'No mapped key mapping d2a: {self.__class__.__name__}:' + key)
                    pass
            elif hasattr(self, key) and getattr(self, key):
                if isinstance(getattr(self, key), uuid.UUID):
                    setattr(openapi_type, key, str(getattr(self, key)))
                else:
                    setattr(openapi_type, key, getattr(self, key))
            elif key == 'attr_value':
                for value_type in ['attr_value_str', 'attr_value_int',
                                   'attr_value_float', 'attr_value_date',
                                   'attr_value_datetime',
                                   'attr_value_list_int', 'attr_value_object']:
                    if getattr(self, value_type):
                        setattr(openapi_type, key, getattr(self, value_type))
            else:
                # print(f'No mapping d2a: {self.__class__.__name__}:' + key)
                pass

        id_val = self.get_id_key()

        if hasattr(openapi_type, id_val):
            if isinstance(getattr(self, 'id'), uuid.UUID):
                setattr(openapi_type, id_val, str(getattr(self, 'id')))
            else:
                setattr(openapi_type, id_val, getattr(self, 'id'))
        # else:
        #     print(f'No attr {id_val} {self} {openapi_type}')

        self.openapi_map_actions(openapi_type)

        return openapi_type

Base = declarative_base(cls=Base)
