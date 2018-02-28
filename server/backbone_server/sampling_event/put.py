from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.sampling_event.edit import SamplingEventEdit
from backbone_server.sampling_event.fetch import SamplingEventFetch

from swagger_server.models.sampling_event import SamplingEvent

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging

class SamplingEventPut():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def put(self, sampling_event_id, sampling_event):

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT id FROM sampling_events WHERE  id = %s'''
                cursor.execute( stmt, (sampling_event_id,))

                existing_sampling_event = None

                for (sampling_event_id, ) in cursor:
                    existing_sampling_event = SamplingEvent(sampling_event_id)

                if not existing_sampling_event:
                    raise MissingKeyException("Could not find sampling_event to update {}".format(sampling_event_id))

                study_id = SamplingEventEdit.fetch_study_id(cursor, sampling_event.study_name, True)
                partner_species = SamplingEventEdit.fetch_partner_species(cursor, sampling_event, study_id)
                stmt = '''UPDATE sampling_events 
                            SET study_id = %s, doc = %s, doc_accuracy = %s,
                            location_id = %s, proxy_location_id = %s, partner_species_id = %s
                            WHERE id = %s'''
                args = (study_id, sampling_event.doc, sampling_event.doc_accuracy,
                        sampling_event.location_id, sampling_event.proxy_location_id,
                        partner_species, sampling_event_id)

                try:
                    cursor.execute(stmt, args)
                    rc = cursor.rowcount

                    cursor.execute('DELETE FROM identifiers WHERE sampling_event_id = %s',
                                   (sampling_event_id,))

                    SamplingEventEdit.add_identifiers(cursor, sampling_event_id, sampling_event)

                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        raise DuplicateKeyException("Error updating sampling_event {}".format(sampling_event)) from err
                    else:
                        self._logger.fatal(repr(error))
                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error updating sampling_event {}".format(sampling_event)) from err
                except DuplicateKeyException as err:
                    raise err


                sampling_event = SamplingEventFetch.fetch(cursor, sampling_event_id)

        if rc != 1:
            raise MissingKeyException("Error updating sampling_event {}".format(sampling_event_id))


        return sampling_event
