import csv
from collections.abc import Iterator
from pathlib import Path

from market_pulse.ingestion.columns import ORDERS_COLUMNS


def read_orders(file_path: Path) -> Iterator[dict[str, str]]:
    with open(file_path, newline="", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        actual_columns = reader.fieldnames or []
        expected_columns = set(ORDERS_COLUMNS)

        missing = expected_columns - set(actual_columns)
        extra = set(actual_columns) - expected_columns

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
