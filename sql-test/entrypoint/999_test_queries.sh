#!/bin/bash
set -e

export SQL_QUERIES="/app/*.sql"

echo "Testing SQL Queries..."

for filename in $SQL_QUERIES; do
  echo "Testing query $filename ..."
  if psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$filename"; then
    echo "Test Passed!"
  else
    echo "Test Failed for SQL Query in $filename - shutting down..."
    exit 1
  fi
done