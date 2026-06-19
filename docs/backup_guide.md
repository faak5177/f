# Резервное копирование БД

Имя файла резервной копии: **`database_backup.backup`** (custom-формат `pg_dump`).

## Создание копии

### Windows

```bat
backup.bat
```

(скрипт лежит в корне проекта, выполняет `pg_dump -F c -b -v -f database_backup.backup Demoekzamen`)

### Linux / macOS

```bash
chmod +x backup.sh
./backup.sh
```

## Восстановление

```bat
restore.bat
```

или вручную:

```bash
createdb -U postgres Demoekzamen_restored
pg_restore -h localhost -p 5432 -U postgres -d Demoekzamen_restored -v database_backup.backup
```

## Проверка после восстановления

```sql
SELECT relname, n_live_tup
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```

## Альтернатива — plain SQL

Если нужен человекочитаемый дамп:

```bash
pg_dump -U postgres -F p -E UTF8 -f database_backup.sql Demoekzamen
```

Восстановление — `psql -U postgres -d Demoekzamen_restored -f database_backup.sql`.
