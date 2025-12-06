#!/bin/bash
#
# Example Backup Script
#
# Usage:
#   ./backup.sh
#
# Environment Variables:
#   BACKUP_DIR - Backup destination directory (default: /var/backups)
#   RETENTION_DAYS - Days to keep backups (default: 30)
#
# Installation:
#   sudo cp backup.sh /usr/local/bin/
#   sudo chmod +x /usr/local/bin/backup.sh
#   sudo chown backup:backup /usr/local/bin/backup.sh

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/var/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_${TIMESTAMP}.tar.gz"
LOG_FILE="${BACKUP_DIR}/backup.log"

# Directories to backup
SOURCE_DIRS=(
    "/etc"
    "/var/www"
    "/home"
)

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "${LOG_FILE}"
}

# Error handler
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Check if running as backup user
if [ "$(whoami)" != "backup" ] && [ "$(whoami)" != "root" ]; then
    error_exit "This script must be run as backup user or root"
fi

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}" || error_exit "Failed to create backup directory"

log "Starting backup: ${BACKUP_NAME}"

# Create backup
tar -czf "${BACKUP_DIR}/${BACKUP_NAME}" \
    "${SOURCE_DIRS[@]}" \
    --exclude='*.log' \
    --exclude='*.tmp' \
    --exclude='/home/*/.cache' \
    2>&1 | tee -a "${LOG_FILE}" || error_exit "Backup creation failed"

# Verify backup
if [ -f "${BACKUP_DIR}/${BACKUP_NAME}" ]; then
    BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}" | cut -f1)
    log "Backup completed successfully: ${BACKUP_NAME} (${BACKUP_SIZE})"
else
    error_exit "Backup file not found: ${BACKUP_NAME}"
fi

# Remove old backups
log "Removing backups older than ${RETENTION_DAYS} days"
find "${BACKUP_DIR}" -name "backup_*.tar.gz" -type f -mtime +${RETENTION_DAYS} -delete 2>&1 | tee -a "${LOG_FILE}"

# List remaining backups
BACKUP_COUNT=$(find "${BACKUP_DIR}" -name "backup_*.tar.gz" -type f | wc -l)
log "Total backups: ${BACKUP_COUNT}"

# Check disk space
DISK_USAGE=$(df -h "${BACKUP_DIR}" | tail -1 | awk '{print $5}')
log "Disk usage for ${BACKUP_DIR}: ${DISK_USAGE}"

log "Backup process completed"

exit 0
