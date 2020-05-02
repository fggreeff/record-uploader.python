import logging

from record_uploader.parse_file import ParseFile
from record_uploader.validation_rules import ValidationRules
from record_uploader.validate_file import ValidateFile
from record_uploader.db_connector import RelationalDBClient
from record_uploader.s3 import S3Client

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

    # Connect to DB for each cluster
    log.info("Connecting to DB...")
    db_clients = [RelationalDBClient(
        user,
        database,
        cluster
    ) for cluster in cluster_ids]

    for client in db_clients:
        log.info(client.cluster_id)

    # redshift_orchestrator = RedshiftOrchestrator(db_clients, query_client)

    results = []


def main_process(source_bucket, source_key, cluster_ids, bucket, user, database):

    results = []
    uploaded_file_success, uploaded_model_success = False, False

    try:
        s3_client = S3Client(bucket)

        # Validate file
        validated_rows = parse_and_validate_file(source_bucket, source_key)

        # Read contents (records) of file to get the files that needs to be uploaded
        for row in validated_rows:
            uploaded_file_success, uploaded_model_success = s3_client.move_processed_archives(row["filename"])
            results.append(f"Status: {uploaded_file_success} {uploaded_model_success} Row: {row}")
            log.info(f"Status: {uploaded_file_success} {uploaded_model_success} Row: {row}")

        # Connect to DB
        connect(cluster_ids, user, database)

    except Exception as ex:  # pylint: disable=W0703
        log.info(f'Found error {ex}')

    finally:
        # Write results file to S3
        # s3_client.write_to_s3(source_bucket, 'results.txt', results)
        log.info(f'Results {results}')
