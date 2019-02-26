from openapi_server.models.log_items import LogItems
from openapi_server.models.log_item import LogItem
from openapi_server.models.sampling_event import SamplingEvent  # noqa: E501
from openapi_server.models.sampling_events import SamplingEvents  # noqa: E501
from openapi_server import util

import logging

from openapi_server.encoder import JSONEncoder
import json

class History():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, record_type, record_id, action_types):

        resp = LogItems()
        resp.log_items = []

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = f"select action_id, input_value, output_value, action_date, result_code from archive where action_id like %s ESCAPE '' and output_value ->> '{record_type}_id' = %s"

                cursor.execute(stmt, ('%' + record_type + '%',
                                      record_id,))

                for (action_id, input_value, output_value, action_date,
                     result_code) in cursor:
                    if action_types and action_types != 'all':
                        if not ('create' in action_id or 'update' in action_id):
                                continue
                    log_item = LogItem()
                    log_item.action = action_id
                    log_item.input_value = str(input_value)
                    log_item.output_value = output_value
                    log_item.action_date = action_date
                    log_item.result = result_code
                    resp.log_items.append(log_item)

                stmt = "select action_id, input_value, output_value, action_date, result_code from archive where action_id = %s and input_value like %s AND result_code = 404"

                cursor.execute(stmt, ('download_' + record_type,
                                      '%' + record_id + '%' ,))

                for (action_id, input_value, output_value, action_date,
                     result_code) in cursor:
                    if action_types and action_types != 'all':
                        if not ('create' in action_id or 'update' in action_id):
                                continue
                    log_item = LogItem()
                    log_item.action = action_id
                    log_item.input_value = str(input_value)
                    log_item.output_value = output_value
                    log_item.action_date = action_date
                    log_item.result = result_code
                    resp.log_items.append(log_item)


        return resp
