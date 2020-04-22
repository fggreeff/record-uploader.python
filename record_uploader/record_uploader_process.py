import logging

from record_uploader.parse_file import ParseFile


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def parse_and_validate_file(bucket, key):
    """
    Validate CSV file extension, parse file and file contents
    """

    s3_file_path = f'{bucket}/{key}'

    parse_file_client = ParseFile(s3_file_path)
    file_contents = parse_file_client.read_csv()

    return file_contents
