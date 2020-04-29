import logging

import boto3
import psycopg2

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class RelationalDBClient(object):
    def __init__(self, user, database, cluster_id):
        self.client = boto3.client('rds', region_name='eu-west-1')

        self.user = user
        self.cluster_id = cluster_id
        self.database = database

    @property
    def endpoint(self):
        if not hasattr(self, '_endpoint'):
            self._endpoint = self.client.describe_clusters(
                ClusterIdentifier=self.cluster_id
            )['Clusters'][0]['Endpoint']

        return self._endpoint

    @property
    def host(self):
        return self.endpoint['Address']

    @property
    def port(self):
        return self.endpoint['Port']

    def create_connection(self):

        log.info(f'Connecting to {self.host}:{self.port}/{self.database}.')

        credentials = self.client.get_cluster_credentials(
            DbUser=self.user,
            DbName=self.database,
            ClusterIdentifier=self.cluster_id,
            DurationSeconds=3600,
            AutoCreate=False
        )

        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=credentials['DbUser'],
            password=credentials['DbPassword'],
            database=self.database
        )

        return conn
