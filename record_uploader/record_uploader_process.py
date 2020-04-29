import logging

from record_uploader.parse_file import ParseFile
from record_uploader.validation_rules import ValidationRules
from record_uploader.validate_file import ValidateFile
from record_uploader.db_connector import RelationalDBClient


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def parse_and_validate_file(bucket, key):
    """
    Validate CSV file extension, parse file and file contents
    """

    s3_file_path = f'{bucket}/{key}'

    validation_rules_client = ValidationRules()
    validation_rules_client.validate_extension(s3_file_path)

    parse_file_client = ParseFile(s3_file_path)
    file_contents = parse_file_client.read_csv()

    validate_file_client = ValidateFile(file_contents)
    validate_file_client.validate_file_content()

    return file_contents


def connect(cluster_ids, user, database):
    cluster_ids = list(set(cluster_ids))

    db_clients = [RelationalDBClient(
        user,
        database,
        cluster
    ) for cluster in cluster_ids]


def main_process(source_bucket, source_key):
    validated_rows = parse_and_validate_file(source_bucket, source_key)

    for row in validated_rows:
        log.info(row)




