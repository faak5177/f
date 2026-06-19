@echo off
REM ===============================================================
REM  Восстановление БД Demoekzamen из database_backup.backup
REM ===============================================================
set PGPASSWORD=123
set PGBIN="C:\Program Files\PostgreSQL\16\bin"
set SRC=database_backup.backup
set DB=Demoekzamen_restored

%PGBIN%\createdb.exe -U postgres %DB%
%PGBIN%\pg_restore.exe -h localhost -p 5432 -U postgres -d %DB% -v %SRC%

echo.
echo [OK] Restored to %DB%
pause
