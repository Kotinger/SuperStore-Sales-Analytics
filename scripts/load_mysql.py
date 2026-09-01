from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "processed"

def read_password() -> str:
    env = os.environ.get("MYSQL_PASSWORD")
    if env:
        return env.strip()
    pass_file = ROOT / "pass.txt"
    if pass_file.exists():
        for line in pass_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                return line
    raise SystemExit("Нет пароля: MYSQL_PASSWORD или pass.txt")


DB_USER = os.getenv("MYSQL_USER", "root")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_NAME = os.getenv("MYSQL_DATABASE", "superstore")


def main() -> None:
    db_pass = read_password()
    clean_path = OUT_DIR / "clean.parquet"
    people_path = OUT_DIR / "people.parquet"

    clean = pd.read_parquet(clean_path)
    url = f"mysql+pymysql://{DB_USER}:{db_pass}@{DB_HOST}/{DB_NAME}"
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
