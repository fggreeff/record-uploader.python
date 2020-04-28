import unittest

from record_uploader import validation_rules
from record_uploader.errors import (MismatchingExtension, MismatchingValueType, MismatchingLetterType,
                                    MismatchingHeaders)


class ValidationRulesTestCase(unittest.TestCase):

    @staticmethod
    def _create_client():
        return validation_rules.ValidationRules()

    def test_extension(self):
        """
        Using file extensions other than csv will raise exceptions
        """
        file_path = 's3_location/my_file.txt'
        validation_rules_client = self._create_client()

        with self.assertRaises(MismatchingExtension):
            validation_rules_client.validate_extension(file_path)

    def test_value_type(self):
        """
        Using value types other than expected will raise exceptions
        """
        row_value = '5'
        expected_type = int
        validation_rules_client = self._create_client()

        with self.assertRaises(MismatchingValueType):
            validation_rules_client.validate_value_type(
                row_value, expected_type)

    def test_validate_value_content(self):
        """
        Using empty values will raise exceptions
        """
        row_value_empty = '   '

        validation_rules_client = self._create_client()

        with self.assertRaises(MismatchingValueType):
            validation_rules_client.validate_value_content(
                row_value_empty)

    def test_validate_parsing_value(self):
        """
        Parsing value types other than expected type 'int', will raise exceptions
        """
        row_value = 'five'
        validation_rules_client = self._create_client()

        with self.assertRaises(MismatchingValueType):
            validation_rules_client.validate_parsing_value(row_value)

    def test_letter(self):
        """
        Using letters other than expected, Mr or MS, will raise exceptions
        """
        row_letter = 'DR'
        validation_rules_client = self._create_client()

        with self.assertRaises(MismatchingLetterType):
            validation_rules_client.validate_letter(row_letter)

    def test_header(self):
        """
        Using headers other than expected, will raise exceptions
        """
        headers = ["filename", "authorizer", "sad_face_tiger",
                   "expected_row_count", "title"]

        validation_rules_client = self._create_client()

        with self.assertRaises(MismatchingHeaders):
            validation_rules_client.validate_header(headers)
