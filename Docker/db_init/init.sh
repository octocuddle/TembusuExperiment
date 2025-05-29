#!/bin/bash
echo "Setting password for user testuser..."
psql -U testuser -d MyLibrary2 -c "ALTER USER testuser WITH PASSWORD '000000';"

echo "Restoring database from dump..."
pg_restore --no-owner -U testuser -d MyLibrary2 /docker-entrypoint-initdb.d/mylibrary2_backup.dump
