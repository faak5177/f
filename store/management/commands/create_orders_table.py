from django.core.management.base import BaseCommand
from django.db import connection

DDL = '''
CREATE TABLE IF NOT EXISTS "Orders" (
    order_id        SERIAL PRIMARY KEY,
    pickpoint_id    INTEGER REFERENCES "PickPoints"(pickpoint_id),
    order_date      DATE     NOT NULL DEFAULT CURRENT_DATE,
    delivery_date   DATE,
    status          VARCHAR(30) NOT NULL DEFAULT 'Новый',
    user_id         INTEGER REFERENCES "Users"(user_id),
    article         VARCHAR(20) REFERENCES "Products"(article),
    quantity        INTEGER NOT NULL DEFAULT 1,
    pickup_code     INTEGER
);
'''

EXPECTED_COLUMNS = {
    'pickup_code':   'INTEGER',
    'delivery_date': 'DATE',
    'pickpoint_id':  'INTEGER',
}


class Command(BaseCommand):
    help = 'Создать/дополнить таблицу Orders в PostgreSQL'

    def handle(self, *args, **opts):
        with connection.cursor() as cur:
            cur.execute(DDL)
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema='public' AND table_name='Orders'
            """)
            existing = {row[0] for row in cur.fetchall()}
            for col, typ in EXPECTED_COLUMNS.items():
                if col not in existing:
                    cur.execute(f'ALTER TABLE "Orders" ADD COLUMN "{col}" {typ}')
                    self.stdout.write(self.style.SUCCESS(f'+ столбец {col}'))
        self.stdout.write(self.style.SUCCESS('Orders готова'))
