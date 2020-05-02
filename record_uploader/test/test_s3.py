import unittest
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

from botocore.exceptions import ClientError
from record_uploader import s3


class S3TestCase(unittest.TestCase):
    BUCKET = 'test-bucket'

    def _patch_client(self, mock):
        """Patch this mock with the data of our choice"""
        mock_client = MagicMock()
        mock.return_value = mock_client
        return mock_client

    def _create_client(self):
        return s3.S3Client(self.BUCKET)

    @patch('boto3.resource')
    def test_perform_file_move(self, mock_boto3):
        """
        This test asserts that files are moving successfully in S3 to the
        correct location. Using boto3 S3 library, this is a two step process.
        1. copy the file from another S3 location and
        2. deleting the original file.
        Hence why there are 4 calls to S3 (as we are moving 2 objects
        and why it is required these calls are made in the correct order.
        """

        mock_aws = self._patch_client(mock_boto3)

        filename_model = 'myFilename_01022020_20200201124000.json.gz'
        filename_files = 'myFilename_01022020_20200201124000.csv'

        s3_client = self._create_client()

        expected_moved_file_result, expected_moved_model_result = True, True

        actual_moved_file_result, actual_moved_model_result = s3_client.move_processed_archives(filename_files)

        mock_aws.Object.assert_has_calls(
            [
                call(
                    self.BUCKET,
                    'Uploaded/Completed/ExampleFiles/{}'.format(filename_files)
                ),
                call().copy_from(
                    CopySource=(
                        '{}/Uploaded/ExampleFiles/{}'
                        .format(self.BUCKET, filename_files)
                    )
                ),
                call(
                    self.BUCKET,
                    'Uploaded/ExampleFiles/{}'.format(filename_files)
                ),
                call().delete(),
                call(
                    self.BUCKET,
                    'Uploaded/Completed/ExampleModel/'
                    '{}'.format(filename_model)
                ),
                call().copy_from(
                    CopySource=(
                        '{}/Uploaded/ExampleModel/{}'
                        .format(self.BUCKET, filename_model)
                    )
                ),
                call(
                    self.BUCKET,
                    'Uploaded/ExampleModel/{}'.format(filename_model)
                ),
                call().delete()
            ],
            any_order=False
        )

        self.assertEqual(
            (actual_moved_file_result, actual_moved_model_result),
            (expected_moved_file_result, expected_moved_model_result)
        )

    @patch('boto3.resource')
    def test_move_missing_file(self, mock_boto3):
        """
        Moving missing files will not raise exceptions
        """

        mock_aws = self._patch_client(mock_boto3)

        input_filename = 'input_key/my_filename.csv'
        output_filename = 'output_key/my_filename.csv'

        s3_client = self._create_client()

        mock_aws.Object().copy_from.side_effect = ClientError(
            error_response={}, operation_name='Test Move'
        )

        self.assertEqual(
            s3_client._move_file(input_filename, output_filename),
            False
        )

    @patch('boto3.resource')
    def test_read_s3_file(self, mock_boto3):
        """
        Read file from S3 will not raise exception
        """

        mock_aws = self._patch_client(mock_boto3)

        input_key = 'input_key/my_filename.csv'
        bucket = 'my_bucket'

        s3_client = self._create_client()

        s3_client.read_s3_file(bucket, input_key)

        mock_aws.Object.assert_has_calls(
            [
                call(
                    bucket,
                    input_key
                ),
                call().get()
            ],
        )

    @patch('boto3.client')
    def test_write_to_s3(self, mock_boto3):

        mock_aws = self._patch_client(mock_boto3)

        s3_client = self._create_client()

        bucket = 'bucket'
        key = 'key'
        output_filename = 'GZ_FILE'

        results = ['result1', 'result2']

        s3_client.write_to_s3(bucket, key, results)

        mock_aws.upload_file.assert_called_once_with(
            f'{output_filename}.gz',
            bucket,
            key
        )
