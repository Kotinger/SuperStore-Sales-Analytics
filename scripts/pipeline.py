from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "processed"
RAW_PATH = DATA_DIR / "SuperStoreOrders - SuperStoreOrders.csv"

ORDER_COL = "order_id"
ORDER_KEY = "order_key"
MONEY_COL = "sales"
DATE_COL = "order_date"
SHIP_DATE_COL = "ship_date"
CLIENT_COL = "customer_key"
NEED_PEOPLE = True


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(df.shape)
    print(df.columns.tolist())
    print(df.isna().sum())
    return df


def check_grain(df: pd.DataFrame, order_col: str = ORDER_COL) -> str:
    rows, orders = len(df), df[order_col].nunique()
    grain = "line" if rows > orders else "order"
    print("rows", rows, "orders", orders, "->", grain)
    return grain


def prepare_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df[MONEY_COL] = pd.to_numeric(
        df[MONEY_COL].astype(str).str.replace(",", "", regex=False)
    )
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], dayfirst=True)
    df[SHIP_DATE_COL] = pd.to_datetime(df[SHIP_DATE_COL], dayfirst=True)
    df["ship_days"] = (df[SHIP_DATE_COL] - df[DATE_COL]).dt.days
    return df


def build_clean(df: pd.DataFrame) -> pd.DataFrame:
    return df[df[MONEY_COL] > 0].copy()


def sanity_check(
    raw: pd.DataFrame, clean: pd.DataFrame, order_col: str = ORDER_COL
) -> None:
    print("rows", len(raw), "->", len(clean))
    print("orders", raw[order_col].nunique(), "->", clean[order_col].nunique())
    print("gmv", clean[MONEY_COL].sum())
    print("dates", clean[DATE_COL].min(), "->", clean[DATE_COL].max())
    assert len(clean) > 0, "clean пустой"


def add_keys(clean: pd.DataFrame) -> pd.DataFrame:
    clean = clean.copy()
    head_cols = [DATE_COL, "customer_name", "country"]
    bad = (clean.groupby(ORDER_COL)[head_cols].nunique() > 1).any(axis=1)
    print("bad order_id:", bad.sum())

    clean[ORDER_KEY] = (
        clean[ORDER_COL].astype(str)
        + "|"
        + clean[DATE_COL].astype(str)
        + "|"
        + clean["customer_name"].astype(str)
        + "|"
        + clean["country"]
    )
    clean[CLIENT_COL] = (
        clean["customer_name"].astype(str) + "|" + clean["country"]
    )
    print("order_id", clean[ORDER_COL].nunique(), "order_key", clean[ORDER_KEY].nunique())
    print("customer_key", clean[CLIENT_COL].nunique())
    return clean


def build_people(clean: pd.DataFrame) -> pd.DataFrame:
    return (
        clean.groupby(CLIENT_COL, as_index=False)
        .agg(
            orders=(ORDER_KEY, "nunique"),
            gmv=(MONEY_COL, "sum"),
            lines=(CLIENT_COL, "size"),
            first_order=(DATE_COL, "min"),
        )
    )


def save_tables(clean: pd.DataFrame, people: pd.DataFrame | None = None) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    clean.to_parquet(OUT_DIR / "clean.parquet", index=False)
    if people is not None:
        people.to_parquet(OUT_DIR / "people.parquet", index=False)
    print("saved", OUT_DIR)


def main() -> None:
    raw = load_data(RAW_PATH)
    check_grain(raw)
    df = prepare_types(raw)
    clean = build_clean(df)
    sanity_check(raw, clean)

    clean = add_keys(clean)
    people = build_people(clean) if NEED_PEOPLE else None
    save_tables(clean, people)
    print("OK -> python scripts/report.py")


if __name__ == "__main__":
    main()
