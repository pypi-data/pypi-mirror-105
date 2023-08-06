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
                pgpass_contents = f.read()

            return pgpass_contents.split(':')

    def connect(self):
        """
        Connect to Postgres database and return the database connection.
        """
        if self.dbuser is None and self.dbname is None:
            # Attempt to parse ~/.pgpass file
            hostname, port, pg_dbname, pg_user, pg_pass = self.read_pgpass()
            if pg_dbname > '' and pg_user > '':
                self.dbuser = pg_user
                self.dbname = pg_dbname
            else:
                logger.exception(pydonitest.advanced_strip("""
                Could not connect to Postgres database! Check the Postgres credentials you
                supplied and/or your ~/.pgpass file if it exists.
                """))

        print('Here')
        con_str = f'postgresql://{self.dbuser}@localhost:5432/{self.dbname}'
        return sqlalchemy.create_engine(con_str)
