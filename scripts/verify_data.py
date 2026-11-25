"""Check that the course data loaded correctly into PostgreSQL."""
import csv
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "docs/course_brief/Capstone2_Customer_Knowledge_Support_Dataset_v2/data"
TABLES = ["products", "customers", "accounts", "entitlements",
          "support_agents", "support_tickets", "ticket_events", "document_registry"]


def count_csv_rows(path):
    """Count the data rows in a CSV file, not counting the header."""
    with open(path, newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.DictReader(f))


def main():
    load_dotenv(PROJECT_ROOT / ".env")
    failures = 0

    with psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
    ) as conn:
        print("Connected to the database.")

        # Check 1: each table has the same number of rows as its CSV file
        for table in TABLES:
            expected = count_csv_rows(DATA_DIR / f"{table}.csv")
            actual = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            ok = actual == expected
            print(f"{'PASS' if ok else 'FAIL'}  {table}: {actual} rows in database, {expected} in CSV")
            if not ok:
                failures += 1

        # Check 2: every account has an entitlement
        missing = conn.execute(
            "SELECT COUNT(*) FROM accounts a "
            "LEFT JOIN entitlements e ON e.account_id = a.account_id "
            "WHERE e.account_id IS NULL"
        ).fetchone()[0]
        ok = missing == 0
        print(f"{'PASS' if ok else 'FAIL'}  accounts without an entitlement: {missing}")
        if not ok:
            failures += 1

    if failures == 0:
        print("ALL CHECKS PASSED")
    else:
        print(f"{failures} CHECK(S) FAILED")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
