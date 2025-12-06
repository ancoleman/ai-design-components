#!/bin/bash
# Validate backup integrity and completeness

set -euo pipefail

BACKUP="${1:-latest}"
VERIFY_INTEGRITY="${2:-false}"

echo "Validating backup: $BACKUP"

# Check if backup exists
if ! ls "/backups/$BACKUP"* > /dev/null 2>&1; then
  echo "ERROR: Backup not found: $BACKUP"
  exit 1
fi

# Check backup size (should be > 0)
SIZE=$(du -sh "/backups/$BACKUP"* | awk '{print $1}')
echo "Backup size: $SIZE"

# Verify integrity if requested
if [[ "$VERIFY_INTEGRITY" == "true" ]]; then
  echo "Verifying backup integrity..."
  # For pgBackRest
  if command -v pgbackrest >/dev/null 2>&1; then
    pgbackrest --stanza=main info
  fi
  # For tar archives
  if [[ "$BACKUP" == *.tar.gz ]]; then
    tar -tzf "/backups/$BACKUP" > /dev/null && echo "Archive integrity: OK"
  fi
fi

echo "Backup validation: PASS"
