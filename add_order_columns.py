"""
Доводит таблицу "Orders" до полной схемы:
добавляет недостающие колонки status, pickup_code, delivery_date.
Запуск:  python add_order_columns.py
"""
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'demoekz_project.settings'
django.setup()
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'Orders'
          AND column_name IN ('status', 'pickup_code', 'delivery_date')
    """)
    existing = {row[0] for row in cursor.fetchall()}
    print('Существующие колонки:', existing)

    if 'status' not in existing:
        cursor.execute('ALTER TABLE "Orders" ADD COLUMN "status" VARCHAR(30) NOT NULL DEFAULT \'Новый\'')
        print('Добавлена колонка status')

    if 'pickup_code' not in existing:
        cursor.execute('ALTER TABLE "Orders" ADD COLUMN "pickup_code" INTEGER')
        print('Добавлена колонка pickup_code')

    if 'delivery_date' not in existing:
        cursor.execute('ALTER TABLE "Orders" ADD COLUMN "delivery_date" DATE NULL')
        print('Добавлена колонка delivery_date')

print('Готово.')
