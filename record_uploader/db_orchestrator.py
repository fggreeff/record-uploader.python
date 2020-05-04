import logging
from psycopg2 import sql, DatabaseError
import datetime
import uuid

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class DbOrchestrator:
    def __init__(self, connection="", cursor=""):
        self.cursor = cursor
        self.connection = connection

    def commit_query(self, result_collection):
        """
        This method commits the transaction if all records
        have been inserted successfully to the model.s3_files table
        """
        try:

            # If all records uploaded successfully, commit changes
            if result_collection:
                log.info("Commit DB transaction")
                self.connection.commit()
            else:
                log.info("Rolling back DB transaction")
                self.connection.rollback()
                self.connection.close()

        except DatabaseError as ex:
            log.error(f'Database error found - {ex}')
            raise ex

        finally:
            log.info('Closing connection...')
            self.cursor.close()

    def execute_query(self, row):
        """
        This method uploads a records file in the model.s3_files table
        """
        rows_uploaded_result = False

        self._execute_file_upload(row["title"], row["authorizer"], row["filename"],  self.cursor)
        rows_uploaded_result = True

        return rows_uploaded_result


    @staticmethod
    def _execute_file_upload(title, authorizer, filename, cursor):
        cursor.execute(
            sql.SQL(
                'INSERT INTO model.s3_files '
                '(ID,title,uploaded,row_updated_by,row_update_date,file_reference)'
                'VALUES (%s, %s, %s, %s, %s, %s);'
                  ),
            [str(uuid.uuid4()), title, 'Y', authorizer, DbOrchestrator._get_date(), filename]
        )

    @staticmethod
    def _get_date():
        return datetime.datetime.now()
