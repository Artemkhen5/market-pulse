from pathlib import Path

from market_pulse.db import connect_db
from market_pulse.ingestion.loaders import load_orders
from market_pulse.ingestion.readers import read_orders
from market_pulse.ingestion.validators import OrderRowParser


def start(dataset: str, dataset_dir: Path):
    if dataset == 'orders':
        name = "olist_orders_dataset-1.csv"
        path = dataset_dir / name
        with connect_db() as conn:
            loaded_count = load_orders(conn, iter_valid_orders(path))

        print(f"Загружено строк в raw.orders: {loaded_count}")


def iter_valid_orders(path: Path):
    rows_read = 0
    rows_failed = 0
    rows_valid = 0
    for row in read_orders(path):
        rows_read += 1
        try:
            parsed_row = OrderRowParser(row).parse()
            rows_valid += 1
            yield parsed_row
        except ValueError as e:
            print(f"Ошибка на строке {rows_read} {e}")
            rows_failed += 1

    print(f"Прочитано строк: {rows_read},"
          f" принято строк: {rows_valid},"
          f" отклонено строк: {rows_failed}")
