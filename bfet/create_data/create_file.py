from __future__ import annotations

import csv
from typing import Any, Dict

from .create_data import _get_data_by_type


def create(filename: str, columns: Dict[str, Any]) -> None:
    _create_csv(filename, columns)


def _create_csv(
    filename: str,
    columns: Dict[str, Dict[str, Any]],
    num_rows: int = 500000,
    batch_size: int = 5000,
) -> None:
    with open(filename, "w", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(columns)
        for _ in range(num_rows // batch_size):
            csv_writer.writerows(
                [_get_data_by_type(data_type=value["type"]) for value in columns.values()]
                for _ in range(batch_size)
            )
