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

- `demoekz_project/` — настройки Django
- `store/` — приложение (модели, view, авторизация, команды)
- `templates/store/` — HTML-шаблоны
- `schema.sql` — SQL-скрипт создания БД
