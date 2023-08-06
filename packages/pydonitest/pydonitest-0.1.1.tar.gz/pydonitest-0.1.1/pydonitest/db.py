import logging
import pydonitest


logging.setLoggerClass(pydonitest.ExtendedLogger)
logger = logging.getLogger(__name__)

if not logger.handlers:
    logger_fmt = '%(asctime)s : %(levelname)-8s : %(name)s : %(message)s'
    formatter = logging.Formatter(logger_fmt)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class Postgres(object):
    """
    Interact with PostgreSQL database through Python.
    """
    def __init__(self, pg_user=None, pg_dbname=None):
        self.dbuser = pg_user
        self.dbname = pg_dbname

        logger.logvars(locals())
