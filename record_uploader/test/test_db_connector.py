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
        return RelationalDBClientTestCase('joe', 'db-222', 'host.com', 1234)

    @patch('boto3.client')
    @patch('psycopg2.connect')
    def test_create_connection(self, mock_psycopg2):
        db = 'db-222'
        user = 'joe'
        password = 'password'
        host = 'host.com'
        port = 1234

        db_client = RelationalDBClient(user, db, host, port)

        db_client.create_connection()

        mock_psycopg2.assert_called_once_with(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db
        )
