#!/bin/bash
# Verify retention policy compliance

echo "Checking backup retention policies..."

# Count backups
BACKUP_COUNT=$(ls /backups/ 2>/dev/null | wc -l)
MIN_REQUIRED=7

if [ $BACKUP_COUNT -ge $MIN_REQUIRED ]; then
  echo "✓ Retention: PASS ($BACKUP_COUNT backups, minimum $MIN_REQUIRED)"
else
  echo "✗ Retention: FAIL ($BACKUP_COUNT backups, minimum $MIN_REQUIRED)"
  exit 1
fi
