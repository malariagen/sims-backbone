
from pprint import pprint
from pprint import pformat

import logging

import openapi_client

class BaseEntityProperties(type):

    @property
    def message_buffer(self):
        return self._message_buffer

    @property
    def use_message_buffer(self):
        return self._use_message_buffer


class BaseEntity(object, metaclass=BaseEntityProperties):

    _message_buffer = []
    _use_message_buffer = False

    def __init__(self, dao, event_set):
        self._logger = logging.getLogger(__name__)
        self._dao = dao
        self._event_set = event_set
        self.attrs = []

    def attrs_from_values(self, values, study_name=None):
        idents = []
        for attr_descrip in self.attrs:
            if attr_descrip['from'] in values:
                from_key = attr_descrip['from']
                to_attr = from_key
                if 'to' in attr_descrip:
                    to_attr = attr_descrip['to']
                if values[from_key]:
                    attr = openapi_client.Attr(to_attr, values[from_key],
                                                  self._event_set)
                    if 'use_study' in attr_descrip and attr_descrip['use_study']:
                        if study_name:
                            attr.study_name = study_name
                    idents.append(attr)
        return idents

    @classmethod
    def set_use_message_buffer(cls, use_buffer):
        cls._use_message_buffer = use_buffer


    def report(self, message, values):

        if values:
            msg = "{}\t{}".format(message, sorted(values.items(), key=lambda x: x))
        else:
            msg = message

        if BaseEntity.use_message_buffer:
            self._logger.debug("using message buffer")
            BaseEntity._message_buffer.append(msg)
        else:
            print(msg)

    def report_conflict(self, sampling_event, report_type, old_val, new_val, message, values):

        old_value = old_val
        new_value = new_val

        if report_type == "Location":
            old_value = pformat(old_val.to_dict(), width=1000, compact=True)
            new_value = pformat(new_val.to_dict(), width=1000, compact=True)

        if report_type in ("Location name", "OriginalSample"):
            if old_val:
                old_value = pformat(old_val.to_dict(), width=1000, compact=True)
            if new_val:
                new_value = pformat(new_val.to_dict(), width=1000, compact=True)

        if report_type.startswith("Country"):
            loc = None
            if sampling_event:
                if 'proxy' in message:
                    loc = sampling_event.proxy_location
                else:
                    loc = sampling_event.location
            if loc:
                message = message + ' ' + pformat(loc.to_dict(), width=1000, compact=True)

        event_id = ''
        study_name = ''

        if sampling_event:
            event_id = sampling_event.sampling_event_id

        msg = "Conflicting {} value\t{}\t{}\t{}\t{}\t{}".format(report_type, message,
                                                                event_id, study_name,
                                                                old_value, new_value)
        self.report(msg, values)

    def set_additional_event(self, sampling_event_id, study_id):

        if study_id[:4] == '0000' or study_id[:4] == '1089':
            return

        event_set_id = 'Additional events: {}'.format(study_id)

        api_response = self._dao.create_event_set(event_set_id)

        self._dao.create_event_set_item(event_set_id, sampling_event_id)


    def merge_attrs(self, samp, existing, change_reasons):

        changed = False
        for new_ident in samp.attrs:
            found = False
            new_study = new_ident.study_name
            if new_study:
                new_study = new_ident.study_name[:4]
            for existing_ident in existing.attrs:
                existing_study = existing_ident.study_name
                if existing_study:
                    existing_study = existing_ident.study_name[:4]
                #Depending on the DAO used the attr can have a different type
                #so can't use ==
                if existing_ident.attr_source == new_ident.attr_source and \
                   existing_ident.attr_type == new_ident.attr_type and \
                   existing_ident.attr_value == new_ident.attr_value and \
                   existing_study == new_study:
                    found = True
                elif existing_ident.attr_type == new_ident.attr_type and \
                       existing_ident.attr_value == new_ident.attr_value and \
                       existing_study == new_study:
                    #This section ignores anything after _ in the attr_source
                    #This avoids having many duplicate attrs
                    #when the date is part of the source
                    parts = new_ident.attr_source.split('_')
                    if len(parts) > 0:
                        new_prefix = parts[0]
                        parts = existing_ident.attr_source.split('_')
                        if len(parts) > 0:
                            existing_ident_prefix = parts[0]
                            if new_prefix == existing_ident_prefix:
                                found = True
            if not found:
                changed = True
                change_reasons.append("Adding ident {}".format(new_ident))
                existing.attrs.append(new_ident)

        return changed
