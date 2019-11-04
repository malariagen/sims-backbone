
from pprint import pprint
from pprint import pformat

import logging

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

        if report_type == "Location name":
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


