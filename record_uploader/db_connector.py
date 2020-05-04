import logging

import psycopg2

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class RelationalDBClient(object):
    def __init__(self, user, database, host, port):

        self.host = host
        self.port = port
        self.user = user
        self.database = database

    def create_connection(self):

        log.info(f'Connecting to {self.host}:{self.port}/{self.database}.')

        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password='password',  # TODO: make this env var
            database=self.database
        )

        return conn
