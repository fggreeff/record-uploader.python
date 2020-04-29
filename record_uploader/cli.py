"""A command line interface to processes files."""
import click
import logging

from record_uploader.record_uploader_process import main_process

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@click.command()
@click.option('-s', '--source-bucket',
              help='S3 Bucket name which contain the files to upload. '
              'This file contains a collection of the files to upload.', default='./record_uploader/test/resources'
              )
@click.option('-k', '--source-key', help='Key path of the master file to upload.', default='collection_of_s3_files.csv')
@click.option('-u', '--user', help='Postgres user to make changes.', default='my_user',
              show_default=True
              )
@click.option('-d', '--database', help='Target Postgres Database.', default='my_db', show_default=True)
@click.option('-i', '--cluster-id', help='Target Postgres cluster ID.', required=True)
@click.option('-b', '--bucket', help='S3 Bucket location for where the files are uploaded from.',
              required=True)
def cli(source_bucket, source_key, cluster_id, bucket, user, database):
    log.debug('Parsing arguments.')
    main_process(source_bucket, source_key, cluster_id, bucket, user, database)


def main():     # pragma: nocover
    cli(auto_envvar_prefix='UPLOADER', obj={}  # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
        )


if __name__ == "__main__":  # pragma: nocover
    main()
