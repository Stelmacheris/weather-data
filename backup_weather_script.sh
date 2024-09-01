#!/bin/sh

if [ -z "$DB_NAME" || -z "$DB_USER" || -z "$DB_PASSWORD" || -z "$DB_HOST" || -z "$DB_PORT" || -z "$BACKUP_DIR" ]; then
  echo "One or more environment variables are not set. Exiting."
  exit 1
fi

TIMESTAMP=$(date +"%Y_%m_%d_%H_%M_%S")
BACKUP_FILE="${BACKUP_DIR}/db_backup_${TIMESTAMP}.dump"

find "$BACKUP_DIR" -type f -name "*.dump" -mtime +1 -exec rm {} \;

PGPASSWORD="$DB_PASSWORD" pg_dump -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -F -c -b -v -f "$BACKUP_FILE" "$DB_NAME"
if [ $? -ne 0 ]; then
  echo "Backup failed. Check the error messages above."
  exit 1
fi

echo "Backup created at $BACKUP_FILE"
exit 0

