import gzip
import logging
import os

import boto3
import botocore

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

BASE_PREFIX = 'Uploaded'
FILES_PREFIX = 'ExampleFiles'
MODEL_PREFIX = 'ExampleModel'
FILES_SUFFIX = '.csv'
MODEL_SUFFIX = '.json.gz'


class S3Client(object):
    def __init__(self, bucket):
        self.resource = boto3.resource('s3')
        self.client = boto3.client('s3')
        self.bucket = bucket

    def move_processed_archives(self, filename):
        """
        Move archived files & models to another location

        :return boolean tuple for whether the file and model were moved
        """
        moved_file_result = self._main_move_file(
            filename, FILES_PREFIX,
            FILES_SUFFIX
        )

        moved_model_result = self._main_move_file(
            filename, MODEL_PREFIX,
            MODEL_SUFFIX
        )

        return moved_file_result, moved_model_result

    def _main_move_file(self, filename, key_prefix, key_suffix):
        """
        Move file from a key prefix to another location with a suffix

        :return boolean result for whether the file was moved successfully
        """
        filename_without_suffix = filename.strip(FILES_SUFFIX)

        input_key = self._get_input_key(key_prefix, filename_without_suffix,
                                        key_suffix)

        output_key = self._get_output_key(key_prefix, filename_without_suffix,
                                          key_suffix)

        result = self._move_file(
            input_key,
            output_key
        )

        return result

    def _move_file(self, input_key, output_key):
        """
        Move
        :param input_key:
        :param output_key:
        :return boolean result for whether the move was successful
        """
        log.info(
            f'Moving file from s3://{self.bucket}/{input_key} to s3://{self.bucket}/{output_key}'
        )

        try:
            self.resource.Object(self.bucket, output_key).copy_from(
                CopySource='{}/{}'.format(self.bucket, input_key)
            )
            self.resource.Object(self.bucket, input_key).delete()
            return True

        except botocore.exceptions.ClientError as ex:
            log.warning(
                f'Error moving file s3://{self.bucket}/{input_key}. {ex}'
            )
            return False

    def _get_output_key(self, prefix, filename, suffix):
        """
        Creates the output key for S3 operations. The BASE_PREFIX is common
        for both the files and model keys whilst the prefix differs. The
        purpose is to create an output key which mirrors the input key, except
        for the Deleted which is interjected.

        I.e. a/b/c/d.z -> a/Completed/b/c/d.z
        """
        output_key = '{}/Completed/{}/{}{}'.format(
            BASE_PREFIX,
            prefix,
            filename,
            suffix
        )

        return output_key

    def _get_input_key(self, prefix, filename, suffix):
        """
        Creates the input key for S3 operations. The BASE_PREFIX is common for
        the files whilst the prefix & suffix differ.
        """
        input_key = '{}/{}/{}{}'.format(
            BASE_PREFIX,
            prefix,
            filename,
            suffix
        )

        return input_key

    def read_s3_file(self, bucket, input_key):
        """
        Reads file in S3
        :param bucket: name of bucket
        :param input_key: path & filename
        :return: contents of the file in the bucket
        """
        obj = self.resource.Object(bucket, input_key)
        object_body = obj.get()['Body']
        object_content = object_body.read()
        return object_content.decode('utf-8')

    def write_to_s3(self, bucket, key, results):

        output_filename = 'GZ_FILE'

        results = list(map(lambda x: f'{x}\n', results))

        with gzip.open(f'{output_filename}.gz', 'wt') as f:
            f.writelines(results)
            f.close()

        self.client.upload_file(
            f'{output_filename}.gz',
            bucket,
            key
        )

        os.remove(f'{output_filename}.gz')
