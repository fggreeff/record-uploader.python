#!/bin/bash
set -e

export SQL_QUERIES="/app/*.sql"
export FROM_DATE="'2018-01-01'"
export TO_DATE="'2018-01-15'"

echo "Testing SQL Queries..."

for filename in $SQL_QUERIES; do
  echo "Testing query $filename ..."
  if psql -v ON_ERROR_STOP=1 -v from_date="$FROM_DATE" -v to_date="$TO_DATE" --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$filename"; then
    echo "Test Passed!"
  else
    echo "Test Failed for SQL Query in $filename - shutting down..."
    exit 1
  fi
done