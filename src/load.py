from pathlib import Path
import json
from src.db import get_connection

TABLE_NAME = "ferry_ticket_counts"

# SQL statements live in the sql/ directory (sibling of src/), kept separate
# from the application logic so they can be versioned and run independently.
SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


def _read_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text(encoding="utf-8")


def _to_row(record: dict) -> tuple:
    """Map one source record to the tuple of column values for the upsert."""
    return (
        record["_id"],
        record["Timestamp"],
        record["Redemption Count"],
        record["Sales Count"],
    )


def load_records(records: list[dict]) -> int:
    """Create the table if needed and upsert the given ferry records.

    `records` are the raw dicts from the CKAN datastore, e.g.:
        {"_id": 1, "Timestamp": "2026-05-29T18:45:00",
         "Redemption Count": 115, "Sales Count": 111}

    Returns the number of rows written.
    """
    create_sql = _read_sql("create_ferry_ticket_counts.sql")
    upsert_sql = _read_sql("upsert_ferry_ticket_counts.sql")
    rows = [_to_row(r) for r in records]

    # The `with` blocks handle commit-on-success / rollback-on-error and close
    # the cursor and connection automatically.
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(create_sql)
            cur.executemany(upsert_sql, rows)

    return len(rows)


if __name__ == "__main__":
    # Smoke test with a couple of sample records: python -m src.load
    import json
    with open("data/transformed/ferry.json", "r", encoding="utf-8") as f:
        records = json.load(f)
    written = load_records(records)
    print(f"Loaded {written} rows into {TABLE_NAME}.")
