# Demoekzamen — вариант 3 (PostgreSQL)

Django-приложение «Интернет-магазин» для демонстрационного экзамена. БД — PostgreSQL.

## Запуск

```bash
python -m venv venv
venv\Scripts\activate                       # Windows
# source venv/bin/activate                  # Linux/macOS

pip install -r requirements.txt

createdb -U postgres Demoekzamen
psql -U postgres -d Demoekzamen -f schema.sql

python manage.py migrate --run-syncdb
python manage.py import_data
python manage.py create_orders_table
python manage.py runserver
```

## Структура

### Код приложения
- `demoekz_project/` — настройки Django (`settings.py`, `test_settings.py`)
- `store/` — приложение (модели, view, авторизация, команды)
- `templates/store/` — HTML-шаблоны
- `tests/` — pytest-сценарии по ролям (Гость / Клиент / Менеджер / Админ)

### База данных
- `schema.sql` / `database_script.sql` — DDL-скрипт создания БД
- `import.sql` — `\copy`-команды импорта CSV
- `add_order_columns.py` — миграция недостающих колонок в `Orders`

### Исходные данные (CSV в корне)
- `Роли.csv`, `Категории.csv`, `Производители.csv`, `Поставщики.csv`,
- `Пользователи.csv`, `Точки подбора.csv`, `Товары.csv`

### Вариативная часть
- `backup.bat` / `backup.sh` — создание `database_backup.backup` (pg_dump custom)
- `restore.bat` — восстановление из резервной копии
- `disk_report.sql` — отчёт о месте на диске (БД, таблицы, индексы)
- `docs/` — ER-диаграмма, UML Use Case, алгоритмы, план тестирования, инструкции

## Запуск тестов

```bash
pytest -q
```

Тесты работают с реальной БД `Demoekzamen` (`conftest.py` → `django_db_setup`), без создания `test_Demoekzamen`.
