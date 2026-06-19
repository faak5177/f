#!/usr/bin/env bash
# ===============================================================
#  Резервная копия БД Demoekzamen (PostgreSQL, custom-формат)
#  Linux/macOS. Имя файла: database_backup.backup
# ===============================================================
set -e
export PGPASSWORD=123
OUT="database_backup.backup"

pg_dump -h localhost -p 5432 -U postgres -F c -b -v -f "$OUT" Demoekzamen

echo
echo "[OK] Backup saved to $OUT"
