import typing

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy import MetaData, join
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, subqueryload

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.permission_exception import PermissionException
from backbone_server.errors.integrity_exception import IntegrityException

from backbone_server.controllers.base_controller import BaseController
from backbone_server.model.scope import session_scope
from backbone_server.model.mixins import Base

class SimsDbBase():

    CREATE_PERMISSION = 'create'
    UPDATE_PERMISSION = 'update'
    GET_PERMISSION = 'get'
    DELETE_PERMISSION = 'delete'

    def __init__(self, engine, session):

        self.session = session
        self.engine = engine

        self.metadata = MetaData(bind=engine)
        Base.metadata.create_all(bind=engine)

        self.openapi_class = None
        self.openapi_multiple_class = None
        self.db_class = None
        self.attr_link = None
        self.api_id = None
        self.duplicate_attrs = []

    def has_study_permission(self, studies, study_code, perm_type):

        found = False

        if isinstance(study_code, list):
            for sc in study_code:
                self.has_study_permission(studies, sc, perm_type)
            return True
        if studies is not None:
            for study in studies:
                if 'all' in study['study']:
                    found = True
                    break
                if study['study'].startswith(study_code[:4]):
                    found = True
                    break

        if not found:
            raise PermissionException(f'No permission for study {study_code}')

        return found

    def pre_post_check(self, db, api_item, studies):
        return api_item

    def post_duplicate_attr_check(self, db, api_item):
        if hasattr(api_item, 'attrs') and api_item.attrs:
            for attr in api_item.attrs:
                if attr.attr_type not in self.duplicate_attrs:
                    from backbone_server.model.attr import Attr
                    from backbone_server.model.study import Study
                    for db_attr in Attr.get_all(db, attr):
                        if db_attr.study:
                            if db.query(self.attr_link).\
                               join(Attr).\
                               join(Study).\
                               filter(and_(self.attr_link.c.attr_id == db_attr.id,\
                                           Study.code == attr.study_name[:4])).first():
                                raise DuplicateKeyException(f"Error inserting {self.api_id} attr {attr.attr_type} {api_item}")
                        else:
                            if db.query(self.attr_link).filter(self.attr_link.c.attr_id == db_attr.id).first():
                                raise DuplicateKeyException(f"Error inserting {self.api_id} attr {attr.attr_type} {api_item}")

    def post_extra_actions(self, api_item):
        pass

    def db_map_attrs(self, db, db_item, api_item):
        if hasattr(api_item, 'attrs') and api_item.attrs:
            new_attrs = []
            from backbone_server.model.attr import Attr
            for attr in api_item.attrs:
                db_attr = Attr.get_or_create(db, attr)
                if db_attr in new_attrs:
                    raise DuplicateKeyException(f'Error duplicate attr {attr}')
                new_attrs.append(db_attr)
            # [] or None
            if new_attrs:
                db_item.attrs.extend(new_attrs)
            attr_to_remove = []
            for attr in db_item.attrs:
                if attr not in new_attrs:
                    attr_to_remove.append(attr)
            for attr in attr_to_remove:
                db_item.attrs.remove(attr)
        elif hasattr(db_item, 'attrs'):
            attr_to_remove = []
            for attr in db_item.attrs:
                attr_to_remove.append(attr)
            for attr in attr_to_remove:
                db_item.attrs.remove(attr)

    def db_map_actions(self, db, db_item, api_item):
        pass

    def openapi_map_actions(self, api_item, db_item):
        pass

    def post(self, api_item, study_name, studies, user):

        if study_name and studies:
            self.has_study_permission(studies,
                                      study_name,
                                      self.CREATE_PERMISSION)

        ret = None

        with session_scope(self.session) as db:

            api_item = self.pre_post_check(db, api_item, studies)
            self.post_duplicate_attr_check(db, api_item)

            db_item = self.db_class()
            db_item.map_from_openapi(api_item)

            self.db_map_actions(db, db_item, api_item)
            self.db_map_attrs(db, db_item, api_item)

            db_item.created_by = user

            db.add(db_item)

            self.post_extra_actions(api_item)
            try:
                db.commit()
            except IntegrityError as int_error:
                if 'already exists' in str(int_error):
                    raise DuplicateKeyException(f'{str(int_error)}')
                raise int_error

            ret = self.get(self.convert_from_id(db, db_item.id), studies)

        return ret

    def convert_to_id(self, db, item_id):

        return item_id

    def convert_from_id(self, db, item_id):

        return item_id

    def pre_put_check(self, db, api_item, studies):
        pass

    def put_duplicate_attr_check(self, db, api_item):

        if hasattr(api_item, 'attrs') and api_item.attrs:
            for attr in api_item.attrs:
                if attr.attr_type not in self.duplicate_attrs:
                    from backbone_server.model.attr import Attr
                    from backbone_server.model.study import Study
                    for db_attr in Attr.get_all(db, attr):
                        my_db_id = getattr(self.attr_link.c, self.api_id)
                        my_api_id = getattr(api_item, self.api_id)
                        if db_attr.study:
                            i_with_attr = db.query(self.attr_link).\
                                     join(Attr).\
                                     join(Study).\
                                     filter(and_(self.attr_link.c.attr_id == db_attr.id, \
                                     my_db_id != my_api_id, \
                                     Study.code == attr.study_name[:4]))
                            if i_with_attr.first():
                                raise DuplicateKeyException(f"Error updating {self.api_id} attr {attr.attr_type} {api_item}")
                        else:
                            i_with_attr = db.query(self.attr_link).\
                                     filter(and_(self.attr_link.c.attr_id == db_attr.id),\
                                     my_db_id != my_api_id)
                            if i_with_attr.first():
                                raise DuplicateKeyException(f"Error updating {self.api_id} attr {attr.attr_type} {attr.attr_value} {my_db_id} {api_item}")

    def put_extra_actions(self, api_item):

        pass

    def put_premap(self, db, api_item, db_item):
        pass

    def put(self, input_item_id, api_item, study_name, studies, user):

        if study_name and studies:
            self.has_study_permission(studies,
                                      study_name,
                                      self.UPDATE_PERMISSION)
        ret = None

        if not input_item_id:
            raise MissingKeyException(f"No item id to update {self.db_class.__table__}")

        with session_scope(self.session) as db:

            item_id = self.convert_to_id(db, input_item_id)

            self.pre_put_check(db, api_item, studies)
            self.put_duplicate_attr_check(db, api_item)
            #print(f'Looking for {item_id}')
            update_item = db.query(self.db_class).get(item_id)

            if not update_item:
                raise MissingKeyException(f"Could not find {self.db_class.__table__} to update {item_id}")

            self.put_premap(db, api_item, update_item)

            update_item.map_from_openapi(api_item)

            if update_item.id != item_id:
                raise MissingKeyException(f"Id in item does not match id in call {self.db_class.__table__} {item_id} {update_item.id}")

            self.db_map_actions(db, update_item, api_item)
            self.db_map_attrs(db, update_item, api_item)
            update_item.updated_by = user

            self.put_extra_actions(api_item)

            try:
                db.commit()
            except IntegrityError as int_error:
                if 'already exists' in str(int_error):
                    raise DuplicateKeyException(f'{str(int_error)}')
                raise int_error

            ret = self.get(input_item_id, studies)

        # print(f'Return from put {ret}')
        return ret


    def delete_extra_actions(self, db, delete_item, api_delete):
        pass

    def delete(self, input_item_id, studies):

        if not input_item_id:
            raise MissingKeyException(f"No item id to delete {self.db_class.__table__}")

        try:
            with session_scope(self.session) as db:

                item_id = self.convert_to_id(db, input_item_id)
                delete_item = db.query(self.db_class).get(item_id)

                if not delete_item:
                    raise MissingKeyException(f"Could not find {self.db_class.__table__} to delete {item_id}")

                api_delete = self.openapi_class()
                delete_item.map_to_openapi(api_delete)
                if studies:
                    study_code = self.get_study_code(delete_item)
                    BaseController.has_study_permission(studies,
                                                        study_code,
                                                        BaseController.DELETE_PERMISSION)

                self.delete_extra_actions(db, delete_item, api_delete)

                db.delete(delete_item)
        except IntegrityError as int_error:
            raise IntegrityException(f"Could not delete {self.db_class.__table__} to delete {item_id} {str(int_error)}")


    def get_study_code(self, db_item):
        if hasattr(db_item, 'study'):
            return db_item.study.code
        ret = []
        if hasattr(db_item, 'original_samples'):
            for orig_samp in db_item.original_samples:
                if orig_samp.study.code not in ret:
                    ret.append(orig_samp.study.code)
        if hasattr(db_item, 'original_sample'):
            if db_item.original_sample and db_item.original_sample.study:
                ret = db_item.original_sample.study.code
        if len(ret) == 1:
            return ret[0]
        else:
            return ret

    def post_get_action(self, db, db_item, api_item, studies, multiple=False):

        return api_item

    def lookup_query(self, db):
        return db.query(self.db_class)

    def get(self, item_id, studies):

        if not item_id:
            raise MissingKeyException(f"No item id to get {self.db_class.__table__}")

        api_item = self.openapi_class()

        with session_scope(self.session) as db:

            item_id = self.convert_to_id(db, item_id)

            if 'study_name' in api_item.openapi_types:
                db_item = self.lookup_query(db).filter_by(id=item_id).options(joinedload('study')).first()
            else:
                db_item = self.lookup_query(db).filter_by(id=item_id).first()

            if not db_item:
                raise MissingKeyException(f"Could not find {self.db_class.__table__} to get {item_id}")

            # determine if the result contains just the object or more
            # or if self.result_fields()
            if isinstance(db_item, self.db_class):
                db_item.map_to_openapi(api_item)
            self.openapi_map_actions(api_item, db_item)

            study_code = self.get_study_code(db_item)

            self.has_study_permission(studies,
                                      study_code,
                                      self.GET_PERMISSION)

            api_item = self.post_get_action(db, db_item, api_item, studies,
                                            False)

            # print(db_item)
            # print(api_item)
        return api_item


    def expand_results(self, db, simple_results, studies):

        return simple_results

    def study_filter(self, studies):

        study_filter = None
        study_codes = None

        if studies is not None:
            study_codes = [i['study'] for i in studies if i['bucket'] == 'pi' or i['bucket'] == 'data' or i['bucket'] == 'all']

        if 'all' in study_codes:
            return None

        return study_codes

    def order_by(self):
        return self.db_class.id

    def _get_multiple_results(self, db, db_query, studies, start, count,
                              order_by=None, study_filter=True):

        response_items = []

        study_codes = self.study_filter(studies)

        if study_filter and study_codes:
            from backbone_server.model.study import Study
            db_query = db_query.filter(Study.code.in_(study_codes))

        if order_by:
            db_query = db_query.distinct(order_by)
        else:
            db_query = db_query.distinct(self.db_class.id)

        ret = self.openapi_multiple_class()
        ret.count = db_query.count()

        if hasattr(ret, 'attr_types'):
            from backbone_server.model.attr import Attr
            attr_items = db.query(self.db_class, Attr,
                                  Attr.attr_type).\
                        join(self.db_class.attrs).\
                        distinct(Attr.attr_type)
            if attr_items:
                ret.attr_types = []
                for attr in attr_items:
                    ret.attr_types.append(attr.attr_type)

        if order_by:
            db_query = db_query.order_by(order_by)

        if start:
            db_query = db_query.offset(start)

        if count:
            db_query = db_query.limit(count)

        # print(study_codes)
        # print(db_query)
        # print(f'start {start} count {count} order_by {order_by}')
        for db_item in db_query.all():
            api_item = self.openapi_class()
            if isinstance(db_item, self.db_class):
                db_item.map_to_openapi(api_item, recurse=False)
            self.openapi_map_actions(api_item, db_item)

            study_code = self.get_study_code(db_item)

            try:
                self.has_study_permission(studies,
                                          study_code,
                                          self.GET_PERMISSION)
            except PermissionException:
                # Just skip if no permission
                continue

            if 'study_name' in api_item.openapi_types:
                api_item.study_name = db_item.study.name

            api_item = self.post_get_action(db, db_item, api_item, studies,
                                            multiple=True)
            response_items.append(api_item)

        for key, value in ret.openapi_types.items():
            if issubclass(value, typing.List):
                # Slightly hacky to get the type of the list members
                (api_subitem_class,) = value.__args__
                if api_subitem_class == self.openapi_class:
                    setattr(ret, key, response_items)

        return self.expand_results(db, ret, studies)


    # Note that study_name applies to the attr not the entity
    def get_by_attr(self, attr_type, attr_value, study_name, value_type, start,
                    count, studies=None):

        if not attr_type:
            raise MissingKeyException(f"No attr_type to get {self.db_class.__table__}")

        if study_name and studies:
            self.has_study_permission(studies,
                                      study_name,
                                      self.GET_PERMISSION)

        ret = None

        with session_scope(self.session) as db:

            db_items = None
            from backbone_server.model.attr import Attr
            my_db_id = getattr(self.attr_link.c, self.api_id)
            attr_filter = None
            from openapi_server.models.attr import Attr as AttrApi

            api_attr = AttrApi(attr_type=attr_type,
                               attr_value=attr_value,
                               study_name=study_name)
            attrs = []
            for db_attr in Attr.get_all(db, api_attr, value_type):
                attrs.append(db_attr.id)

            if attrs:
                attr_filter = db.query(my_db_id).\
                         join(Attr).\
                         filter(Attr.id.in_(attrs)).\
                        distinct(my_db_id)

                db_items = self.lookup_query(db).\
                        filter(self.db_class.id.in_(attr_filter))

                ret = self._get_multiple_results(db, db_items, studies, start, count)
            else:
                ret = self.openapi_multiple_class()
                ret.count = 0
                for key, value in ret.openapi_types.items():
                    if issubclass(value, typing.List):
                        # Slightly hacky to get the type of the list members
                        (api_subitem_class,) = value.__args__
                        if api_subitem_class == self.openapi_class:
                            setattr(ret, key, [])

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

            db_items = None
            db_items = self.lookup_query(db).filter(self.db_class.study.has(code=study_name[:4])).options(joinedload('study'))

            ret = self._get_multiple_results(db, db_items, studies, start, count)

            if ret.count == 0:
                from backbone_server.model.study import Study
                db_item = db.query(Study).filter_by(code=study_name[:4]).first()
                if not db_item:
                    raise MissingKeyException(f'No such study {study_name}')


        return ret

    def gets(self, studies, start, count):

        ret = None

        with session_scope(self.session) as db:

            db_items = self.lookup_query(db)

            ret = self._get_multiple_results(db, db_items, studies, start,
                                             count, self.order_by())

        return ret

    def gets_in(self, ids, studies, start, count):

        ret = None

        with session_scope(self.session) as db:

            db_items = self.lookup_query(db).filter(self.db_class.id.in_(ids))

            ret = self._get_multiple_results(db, db_items, studies, start, count)

        return ret
