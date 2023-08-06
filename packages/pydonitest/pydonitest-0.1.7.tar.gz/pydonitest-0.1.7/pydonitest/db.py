import os
import logging
import pydonitest
import sqlalchemy


logger = pydonitest.logger_setup(__name__, pydonitest.module_loglevel)


class Postgres(object):
    """
    Interact with PostgreSQL database through Python.
    """
    def __init__(self, pg_user=None, pg_dbname=None):
        self.dbuser = pg_user
        self.dbname = pg_dbname
        self.dbcon = self.connect()

    def read_pgpass(self):
        """
        Read ~/.pgpass file if it exists and extract Postgres credentials. Return tuple
        in format:

            hostname, port, pg_dbname, pg_user, pg_pass
        """
        pgpass_file = os.path.expanduser('~/.pgpass')
        if os.path.isfile(pgpass_file):
            with open(pgpass_file, 'r') as f:
                pgpass_contents = f.read().split(':')

            # Ensure proper ~/.pgpass format, should be a tuple of length 5
            assert len(pgpass_contents) == 5, \
                'Invalid ~/.pgpass contents format. Should be `hostname:port:pg_dbname:pg_user:pg_pass`'

            return pgpass_contents

    def connect(self):
        """
        Connect to Postgres database and return the database connection.
        """
        if self.dbuser is None and self.dbname is None:
            # Attempt to parse ~/.pgpass file
            logger.info('No credentials supplied, attempting to parse ~/.pgpass file')
            pgpass_contents = self.read_pgpass()
            if pgpass_contents is not None:
                hostname, port, pg_dbname, pg_user, pg_pass = pgpass_contents

                if pg_dbname > '' and pg_user > '':
                    self.dbuser = pg_user
                    self.dbname = pg_dbname
            else:
                raise Exception(pydonitest.advanced_strip("""
                Could not connect to Postgres database! Check the Postgres credentials you
                supplied and/or your ~/.pgpass file if it exists.
                """))

        con_str = f'postgresql://{self.dbuser}@localhost:5432/{self.dbname}'
        return sqlalchemy.create_engine(con_str)
