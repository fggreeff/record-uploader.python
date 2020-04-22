import os
import unittest

from record_uploader.parse_file import ParseFile


class ParseCSVTestCase(unittest.TestCase):
    @staticmethod
    def _create_client():
        mock_s3_file_path = f'{os.path.dirname(__file__)}/resources/collection_of_s3_files.csv'  # noqa: E501
        return ParseFile(mock_s3_file_path)

    def test_read_csv(self):
        """
        Parse csv file and read rows, row mismatch will raise exceptions
        """

        expected_file_contents = [{'filename': 'some_file_in_s3.csv',
                                   'authorizer': 'Joe Blogs',
                                   'expected_row_count': '5'},
                                  {'filename': 'example_file.csv',
                                   'authorizer': 'Steve ',
                                   'expected_row_count': '10'}]

        parse_csv_client = self._create_client()
        parsed_row_collection = parse_csv_client.read_csv()

        self.assertEqual(parsed_row_collection,
                         expected_file_contents)


# if __name__ == '__main__':
#     unittest.main()
