@echo off
REM ===============================================================
REM  Резервная копия БД Demoekzamen (PostgreSQL, custom-формат)
REM  Windows. Имя файла: database_backup.backup
REM ===============================================================
set PGPASSWORD=123
set PGBIN="C:\Program Files\PostgreSQL\16\bin"
set OUT=database_backup.backup

%PGBIN%\pg_dump.exe -h localhost -p 5432 -U postgres -F c -b -v -f %OUT% Demoekzamen

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Backup saved to %OUT%
) else (
    echo.
    echo [ERR] pg_dump failed (code %ERRORLEVEL%)
)
pause
