from datetime import datetime


class OrderRowParser:
    REQUIRED_FIELDS = [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
    ]
    DATETIME_FIELDS = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    def __init__(self, row: dict) -> None:
        self.row = row

    def parse(self) -> dict[str, str | datetime | None]:
        for key in self.row.keys():
            self.parse_required_fields(key, self.row[key])
            self.parse_date_fields(key, self.row[key])
        return self.row

    def parse_required_fields(self, key: str, value: str | None) -> None:
        if value == "" or value is None:
            if key in self.REQUIRED_FIELDS:
                raise ValueError(f"Required field {key} is missing")
            self.row[key] = None

    def parse_date_fields(self, key: str, value: str | None) -> None:
        if key in self.DATETIME_FIELDS and value is not None:
            try:
                parsed_date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                self.row[key] = parsed_date
            except ValueError as e:
                raise ValueError(f"Некорректная дата в поле {key}: {value!r}") from e
