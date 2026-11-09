import csv
from collections.abc import Iterator
from pathlib import Path

ORDERS_COLUMNS = {
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
}


def read_orders(file_path: Path) -> Iterator[dict[str, str]]:
    with open(file_path, newline="", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        actual_columns = reader.fieldnames or []

        missing = ORDERS_COLUMNS - set(actual_columns)
        extra = set(actual_columns) - ORDERS_COLUMNS

        if len(actual_columns) != len(set(actual_columns)):
            raise ValueError(
                "В файле повторяющиеся заголовки"
            )

        if missing or extra:
            raise ValueError(
                f"Некорректные заголовки в {file_path.name}: "
                f"отсутствуют {sorted(missing)}, лишние {sorted(extra)}"
            )

        yield from reader
