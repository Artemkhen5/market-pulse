from collections.abc import Iterable, Mapping
from datetime import datetime

import psycopg

from market_pulse.ingestion.columns import ORDERS_COLUMNS

OrderRow = Mapping[str, str | datetime | None]


def load_orders(
        conn: psycopg.Connection,
        rows: Iterable[OrderRow]
) -> int:
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TEMP TABLE staging_orders
                    (
                        LIKE raw.orders
                    )
                        ON COMMIT DROP
                    """)

        with cur.copy("COPY staging_orders FROM STDIN") as copy:
            for row in rows:
                values = tuple(row[column] for column in ORDERS_COLUMNS)
                copy.write_row(values)

        cur.execute("""
                    INSERT INTO raw.orders
                    SELECT *
                    FROM staging_orders
                    ON CONFLICT (order_id) DO NOTHING
                    """)

        return cur.rowcount
