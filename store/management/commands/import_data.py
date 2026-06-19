import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import connection

ROOT = Path(__file__).resolve().parents[3]

FILES = [
    ('Roles',        'Роли.csv',           ['role_name']),
    ('Categories',   'Категории.csv',      ['category_name']),
    ('Manufactures', 'Производители.csv',  ['manufacture_name']),
    ('Suplyers',     'Поставщики.csv',     ['suplyer_name', 'inn', 'address']),
    ('Users',        'Пользователи.csv',   ['surname', 'name', 'patronymic', 'login', 'password', 'role_id']),
    ('Products',     'Товары.csv',         ['article', 'name', 'unit', 'price', 'max_discount',
                                                  'manufacture_id', 'suplyer_id', 'category_id',
                                                  'discount', 'quantity', 'description', 'image_path']),
    ('PickPoints',   'Точки подбора.csv',  ['address']),
]


class Command(BaseCommand):
    help = 'Импорт CSV-файлов в PostgreSQL'

    def handle(self, *args, **opts):
        with connection.cursor() as cur:
            for table, fname, cols in FILES:
                path = ROOT / fname
                if not path.exists():
                    self.stdout.write(self.style.WARNING(f'Пропущен {fname}'))
                    continue
                with open(path, encoding='utf-8') as f:
                    reader = csv.reader(f, delimiter=';')
                    next(reader, None)
                    rows = [tuple(r[:len(cols)]) for r in reader if r]
                placeholders = ','.join(['%s'] * len(cols))
                column_list  = ','.join(f'"{c}"' for c in cols)
                sql = f'INSERT INTO "{table}" ({column_list}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'
                cur.executemany(sql, rows)
                self.stdout.write(self.style.SUCCESS(f'{table}: {len(rows)} строк'))
