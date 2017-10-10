import logging

def get_connection():
    _postgres = True
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    if _postgres:
        import psycopg2
        from psycopg2.extras import register_uuid
        from psycopg2.extras import LoggingConnection

        config = {
            'user': 'iwright',
            'database': 'backbone_service'
        }

        psycopg2.extensions.register_type(register_uuid())
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
        conn = psycopg2.connect(connection_factory=LoggingConnection, **config )
        conn.initialize(logger)
        cur = conn.cursor()
#        cur.execute("SET search_path TO " + 'backbone,public,contrib')
        cur.close()
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
                logger.critical("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.critical("Database does not exist")
            else:
                logger.critical(err)
    return conn

