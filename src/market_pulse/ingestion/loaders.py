from collections.abc import Iterable, Mapping
from datetime import datetime

import psycopg

ORDER_COLUMNS = (
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
)

OrderRow = Mapping[str, str | datetime | None]


def load_orders(
        conn: psycopg.Connection,
        rows: Iterable[Mapping[str, str | datetime | None]]
) -> int:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TEMP TABLE staging_orders
            (LIKE raw.orders)
            ON COMMIT DROP 
        """)

        with cur.copy("COPY staging_orders FROM STDIN") as copy:
            for row in rows:
                values = tuple(row[column] for column in ORDER_COLUMNS)
                copy.write_row(values)

        cur.execute("""
            INSERT INTO raw.orders
            SELECT * FROM staging_orders
            ON CONFLICT (order_id) DO NOTHING
        """)

        return cur.rowcount