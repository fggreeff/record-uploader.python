import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from record_uploader.db_connector import RelationalDBClient


class RelationalDBClientTestCase(unittest.TestCase):

    def _patch_client(self, mock):
        """Patch this mock with the data of our choice"""
        mock_client = MagicMock()
        mock.return_value = mock_client
        return mock_client

    def _create_client(self):
        return RelationalDBClientTestCase('joe', 'db-222', 'cluster-id-111')

    @patch('boto3.client')
    @patch('psycopg2.connect')
    def test_create_connection(self, mock_psycopg2, mock_boto3):
        cluster_id = 'cluster-id-111'
        db = 'db-222'
        user = 'joe'
        password = 'secret'
        endpoint = 'host.com'
        port = 1234

        mock_aws = self._patch_client(mock_boto3)

        mock_aws.get_cluster_credentials.return_value = {
            'DbUser': user,
            'DbPassword': password
        }

        mock_aws.describe_clusters.return_value = {
            'Clusters': [
                {
                    'Endpoint': {
                        'Address': endpoint,
                        'Port': port
                    }
                }
            ]
        }

        db_client = RelationalDBClient(user, db, cluster_id)

        db_client.create_connection()

        mock_psycopg2.assert_called_once_with(
            host=endpoint,
            port=port,
            user=user,
            password=password,
            database=db
        )

        mock_aws.get_cluster_credentials.assert_called_once_with(
            DbUser=user,
            DbName=db,
            ClusterIdentifier=cluster_id,
            DurationSeconds=3600,
            AutoCreate=False
        )
