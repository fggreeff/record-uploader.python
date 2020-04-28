import unittest

from record_uploader import validate_file


class ValidateFileTestCase(unittest.TestCase):

    file_contents = [{'filename': 'example.csv', 'authorizer': 'fred',
                      'expected_row_count': '10', 'title': 'Mr'},
                     {'filename': 'another_example.csv', 'authorizer': 'jenny',
                      'expected_row_count': '5', 'title': 'ms'}]

    def _create_client(self):
        return validate_file.ValidateFile(self.file_contents)

    def test_validate_header(self):
        """
        Validate file header
        """

        self._create_client()._validate_header()

    def test_validate_rows(self):
        """
        Validate file rows
        - row value types
        - row containing the file extension
        - row value type str is able to convert to type int
        """

        self._create_client()._validate_rows()
