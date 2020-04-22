import logging

from record_uploader.validation_rules import ValidationRules


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class ValidateFile:

    def __init__(self, file_contents):
        self.file_contents = file_contents

    @staticmethod
    def _create_validation_rules_client():
        return ValidationRules()

    def validate_file_content(self):
        """
        Validate file contents
        """

        log.info("Validating S3 file contents")
        self._validate_header()
        self._validate_rows()

    def _validate_header(self):
        """
        Validate file headers
        """

        header_keys = set([k for keys in
                           [item.keys() for item in self.file_contents]
                           for k in keys])

        self._create_validation_rules_client().validate_header(header_keys)

        log.info("Header validation successful")

    def _validate_rows(self):
        """
        Validate file rows
        - row value types
        - row containing the file extension
        - row value type str is able to convert to type int
        - row empty
        """

        # TODO: Show the row number where the failure occurred
        for dic in self.file_contents:
            self._create_validation_rules_client().validate_extension(
                dic['filename'])
            self._create_validation_rules_client().validate_parsing_value(
                dic['expected_row_count'])

            for header, row in dic.items():
                self._create_validation_rules_client().validate_value_type(
                    row, str)
                self._create_validation_rules_client().validate_value_content(row)

        log.info("Row validation successful")
