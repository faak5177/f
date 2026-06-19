-- ============================================================
--  Demoekzamen / вариант 3 / отчёт об использовании места
--  Запуск:  psql -U postgres -d Demoekzamen -f disk_report.sql
-- ============================================================

\echo === 1. РАЗМЕР ВСЕЙ БД ===
SELECT pg_size_pretty(pg_database_size('Demoekzamen')) AS database_size;

\echo
\echo === 2. РАЗМЕР КАЖДОЙ ТАБЛИЦЫ (данные + индексы + TOAST) ===
SELECT
    c.relname                                          AS table_name,
    pg_size_pretty(pg_total_relation_size(c.oid))      AS total_size,
    pg_size_pretty(pg_relation_size(c.oid))            AS data_size,
    pg_size_pretty(pg_indexes_size(c.oid))             AS index_size,
    COALESCE(s.n_live_tup, 0)                          AS rows
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN pg_stat_user_tables s ON s.relid = c.oid
WHERE n.nspname = 'public'
  AND c.relkind = 'r'
ORDER BY pg_total_relation_size(c.oid) DESC;

\echo
\echo === 3. 10 САМЫХ БОЛЬШИХ ОБЪЕКТОВ (таблицы + индексы + TOAST) ===
SELECT
    relname,
    pg_size_pretty(pg_total_relation_size(oid)) AS size
FROM pg_class
WHERE relkind IN ('r', 'i', 't')
ORDER BY pg_total_relation_size(oid) DESC
LIMIT 10;

\echo
\echo === 4. РАЗМЕР ОТДЕЛЬНЫХ ИНДЕКСОВ ===
SELECT
    schemaname,
    relname        AS table_name,
    indexrelname   AS index_name,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;

\echo
\echo === 5. СТАТИСТИКА СТРОК ПО ТАБЛИЦАМ ===
SELECT
    relname     AS table_name,
    n_live_tup  AS live_rows,
    n_dead_tup  AS dead_rows,
    last_vacuum,
    last_autovacuum,
    last_analyze
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
