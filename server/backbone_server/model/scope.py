from contextlib import contextmanager

import logging

logger = logging.getLogger('db session scope')

# https://docs.sqlalchemy.org/en/13/orm/session_basics.html
# https://docs.sqlalchemy.org/en/13/orm/contextual.html#unitofwork-contextual
@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as error:
        logger.error(error)
        session.rollback()
        raise error
    finally:
        session.close()
