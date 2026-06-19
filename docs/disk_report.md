# Отчёт об использовании дискового пространства

Запрашиваются штатными функциями `pg_catalog`. Готовый набор запросов — в файле `disk_report.sql` в корне проекта.

## Запуск

```bash
psql -U postgres -d Demoekzamen -f disk_report.sql > disk_report.txt
```

## Что измеряется

| № | Метрика | Функция |
| --- | --- | --- |
| 1 | Размер всей БД | `pg_database_size('Demoekzamen')` |
| 2 | Размер таблицы (данные + индексы + TOAST) | `pg_total_relation_size(oid)` |
| 3 | Размер только данных | `pg_relation_size(oid)` |
| 4 | Размер индексов таблицы | `pg_indexes_size(oid)` |
| 5 | Количество строк | `pg_stat_user_tables.n_live_tup` |

## Сводный запрос по таблицам

```sql
SELECT
    c.relname                                     AS table_name,
    pg_size_pretty(pg_total_relation_size(c.oid)) AS total_size,
    pg_size_pretty(pg_relation_size(c.oid))       AS data_size,
    pg_size_pretty(pg_indexes_size(c.oid))        AS index_size,
    s.n_live_tup                                  AS rows
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN pg_stat_user_tables s ON s.relid = c.oid
WHERE n.nspname = 'public'
  AND c.relkind = 'r'
ORDER BY pg_total_relation_size(c.oid) DESC;
```

## Получение через pgAdmin 4

1. Открыть дерево объектов → БД `Demoekzamen`.
2. Правая панель → вкладка **Statistics** — общий размер БД.
3. По каждой таблице открыть **Statistics** — `Table size`, `Indexes size`, `Toast table size`, `Tuple count`.
4. Скриншоты вставить в отчёт `db_size_report.docx` / `tables_size_report.docx`.
