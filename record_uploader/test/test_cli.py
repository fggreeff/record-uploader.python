from unittest.mock import patch

from click.testing import CliRunner

from record_uploader.cli import cli

INPUT_SOURCE_BUCKET = 'test-datastore'
INPUT_SOURCE_KEY = 'MasterFileRecordUploaderTemp/20210001000100.csv'
INPUT_BUCKET = 'one-test-datastore'


@patch("record_uploader.cli.main_process")
def test_cli_with_args(mock_main_process):
    """
    Parsing in required arguments only not throw exception
    """
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--source-bucket', INPUT_SOURCE_BUCKET,
                            '--source-key', INPUT_SOURCE_KEY,
                            '--bucket', INPUT_BUCKET], obj={})

    assert len(mock_main_process.call_args_list) == 1
    args, _ = mock_main_process.call_args_list[0]

    source_bucket, source_key, bucket, user, database, port, host = args

    assert source_bucket == INPUT_SOURCE_BUCKET
    assert source_key == INPUT_SOURCE_KEY
    assert bucket == INPUT_BUCKET

    assert result.exit_code == 0


def test_cli_no_args():
    """
    Not parsing in any arguments will bring up the help & usage descriptions
    """
    runner = CliRunner()
    result = runner.invoke(cli, [])

    assert result.exit_code > 0
    assert result.output.startswith('Usage:')
