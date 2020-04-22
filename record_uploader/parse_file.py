import logging
import csv


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class ParseFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv(self):
        data = []
        csvreader = None

        try:
            with open(self.file_path, encoding='utf-8-sig') as csvfile:
                csvreader = csv.DictReader(csvfile)

                data = [dict(row) for row in csvreader]

            log.info(f"Total no. of rows: {csvreader.line_num}")
            csvfile.close()

        except FileNotFoundError as e:
            log.error(f"FileNotFoundError {e} ", exc_info=True)
            raise e

        except IOError as e:
            log.error(f"IOError {e} ", exc_info=True)
            raise e

        if not csvreader:
            log.error("No data in file")
            raise EOFError("EOFError: No data in file")

        return data
