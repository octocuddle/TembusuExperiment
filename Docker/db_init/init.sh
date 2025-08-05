#!/bin/bash
echo "Setting password for user posgres..."
psql -U postgres -d MyLibrary2 -c "ALTER USER postgres WITH PASSWORD '123456';"

echo "Restoring database from dump..."
pg_restore --no-owner -U postgres -d MyLibrary2 /docker-entrypoint-initdb.d/mylibrary2_backup.dump
