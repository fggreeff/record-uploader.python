from os.path import splitext
from record_uploader.errors import (MismatchingExtension, MismatchingValueType,
                                    MismatchingLetterType, MismatchingHeaders)


class ValidationRules:
    """
    Validate file fields for allowed types and headers of the uploaded files.

    Initialization parameters:
       ALLOWED_EXTENSIONS_TYPES: iterable with allowed file extensions
           ie. ['csv']
       ALLOWED_TITLE_TYPES: iterable with allowed validate_letter types, Ms Mr
           ie. ['MR', 'MS']
       ALLOWED_HEADERS_TYPES: iterable list with expected headers,
                                                    the order is of importance
           ie. ['filename', 'authorizer', ...]
    """

    ALLOWED_EXTENSIONS_TYPES = ['csv']
    ALLOWED_TITLE_TYPES = ['MR', 'MS']
    ALLOWED_HEADERS_TYPES = ['filename', 'authorizer', 'expected_row_count', 'title']

    def validate_extension(self, file_path):
        ext = splitext(file_path)[1][1:].lower()
        if ext.lower() not in self.ALLOWED_EXTENSIONS_TYPES:
            message = (
                f"Extension '{ext}' not allowed.\n"
                f"Allowed extensions '{self.ALLOWED_EXTENSIONS_TYPES}' for file {file_path}"
            )
            raise MismatchingExtension(message)

    def validate_value_type(self, row_value, expected_type):
        if not isinstance(row_value, expected_type):
            message = f"Value '{row_value}' type mismatch, expected type '{expected_type}'"
            raise MismatchingValueType(message)

    def validate_value_content(self, row_value):
        if len(row_value.strip()) == 0:
            message = f"Value '{row_value}' is empty, expected to have a value"
            raise MismatchingValueType(message)

    def validate_parsing_value(self, row_value):
        try:
            int(row_value)
        except Exception:
            message = f"Value '{row_value}' is not able to parse, expected parse type 'int'"
            raise MismatchingValueType(message)

    def validate_letter(self, row_letter):
        if row_letter not in self.ALLOWED_TITLE_TYPES:
            message = (
                f"Title '{row_letter}' is not valid. Allowed types: '{self.ALLOWED_TITLE_TYPES}'"
            )
            raise MismatchingLetterType(message)

    def validate_header(self, headers):
        headers_not_found = [
            item for item in headers if item.lower() not in self.ALLOWED_HEADERS_TYPES
        ]
        if len(headers_not_found) > 0:
            message = (
                f"The following headers '{headers_not_found}' is not valid.\n"
                f"Allowed types: '{self.ALLOWED_HEADERS_TYPES}'"
            )
            raise MismatchingHeaders(message)
