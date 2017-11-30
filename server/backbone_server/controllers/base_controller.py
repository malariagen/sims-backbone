import logging
import os

class BaseController():

    _connection = None
    _logger = None

    def __init__ (self):
#        logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)
        self._connection = self._init_connection()

    def __del__(self):
        if self._connection:
            self._connection.close()

    def get_connection(self):
        return self._connection

    def _init_connection(self):
        _postgres = True

        if _postgres:
            import psycopg2
            from psycopg2.extras import register_uuid
            from psycopg2.extras import LoggingConnection

            config = {
                'user': os.getenv('DB_USER',os.getenv('USER')),
                'database': os.getenv('DATABASE','backbone_service'),
                'password': os.getenv('DB_PASSWORD',None),
                'host': os.getenv('DB_HOST','localhost'),
            }

            psycopg2.extensions.register_type(register_uuid())
            psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
            psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
            conn = psycopg2.connect(connection_factory=LoggingConnection, **config )
            conn.initialize(self._logger)
    #        cur = conn.cursor()
    #        cur.execute("SET search_path TO " + 'backbone,public,contrib')
    #        cur.close()
        else:
            import mysql.connector
            from mysql.connector import errorcode
            config = {
                'user': 'iwright',
                'database': 'backbone_service'
            }

            try:
                conn = mysql.connector.connect(**config)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    self._logger.critical("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self._logger.critical("Database does not exist")
                else:
                    self._logger.critical(err)
        return conn

    """
    Convert the connexion token_info (OAuth) response into something that can be made consistent
    with AWS Custom Auth details
    """
    def token_info(self, tok_info):
        resp = []
        for auth_grp in tok_info['memberOf']:
            dns = auth_grp.split(',')
            cn = dns[0].split('=')[1]
            resp.append(cn)

        return resp

    """
    Throw an exception if no permission
    """
    def check_permissions(self, study_id, perms):

        pass
