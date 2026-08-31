from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "processed"

DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASS = os.getenv("MYSQL_PASSWORD", "password")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_NAME = os.getenv("MYSQL_DATABASE", "superstore")


def main() -> None:
    clean_path = OUT_DIR / "clean.parquet"
    people_path = OUT_DIR / "people.parquet"

    clean = pd.read_parquet(clean_path)
    url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(url)

    clean.to_sql(
        "clean_orders",
        engine,
        if_exists="replace",
        index=False,
        chunksize=5000,
    )
    print("clean_orders:", len(clean), "rows")

    if people_path.exists():
        people = pd.read_parquet(people_path)
        people.to_sql(
            "people",
            engine,
            if_exists="replace",
            index=False,
        )
        print("people:", len(people), "rows")


if __name__ == "__main__":
    main()
