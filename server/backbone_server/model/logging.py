import time
import logging
import os

from sqlalchemy import event
from sqlalchemy.engine import Engine
logging.basicConfig()
logger = logging.getLogger("backbone.sqltime")

if os.getenv("QUERY_LOG"):
    logger.setLevel(logging.DEBUG)

threshold = float(os.getenv("QUERY_LOG_THRESHOLD", "0.009"))

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                          parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    if total > threshold and 'pg_' not in statement:
        logger.debug("Query: %s %s", statement, parameters)
        logger.debug("Total Time: %f", total)
