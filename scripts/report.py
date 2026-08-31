from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "processed"

ROUTE = "ABC"
ORDER_KEY = "order_key"
MONEY_COL = "sales"
DATE_COL = "order_date"
CLIENT_COL = "customer_key"
PROFIT_COL = "profit"


def load_tables() -> tuple[pd.DataFrame, pd.DataFrame | None]:
    clean = pd.read_parquet(OUT_DIR / "clean.parquet")
    people_path = OUT_DIR / "people.parquet"
    people = pd.read_parquet(people_path) if people_path.exists() else None
    return clean, people


def cohort_retention(clean: pd.DataFrame) -> pd.DataFrame:
    orders_tbl = (
        clean.groupby([CLIENT_COL, ORDER_KEY], as_index=False)
        .agg(order_date=(DATE_COL, "min"))
    )
    orders_tbl["order_month"] = orders_tbl["order_date"].dt.to_period("M")
    first_cohort = orders_tbl.groupby(CLIENT_COL)["order_month"].min().rename("cohort")
    orders_tbl = orders_tbl.join(first_cohort, on=CLIENT_COL)
    orders_tbl["period_n"] = (
        orders_tbl["order_month"].astype(int) - orders_tbl["cohort"].astype(int)
    )

    cohort_size = orders_tbl.groupby("cohort")[CLIENT_COL].nunique()
    active = orders_tbl.groupby(["cohort", "period_n"])[CLIENT_COL].nunique()
    return active.div(cohort_size, level=0).unstack(fill_value=0)


def main() -> None:
    clean, people = load_tables()
    order_col = ORDER_KEY

    gmv = clean[MONEY_COL].sum()
    orders = clean[order_col].nunique()
    print("--- итог ---")
    print("gmv", gmv, "orders", orders, "aov", gmv / orders, "lines", len(clean))

    if "A" in ROUTE or "C" in ROUTE:
        by_country = clean.groupby("country").agg(
            gmv=(MONEY_COL, "sum"),
            orders=(order_col, "nunique"),
        )
        by_country["aov"] = by_country["gmv"] / by_country["orders"]
        print("top country:\n", by_country.sort_values("gmv", ascending=False).head(3))

        clean = clean.copy()
        clean["month"] = clean[DATE_COL].dt.month
        by_ym = clean.groupby(["year", "month"]).agg(
            gmv=(MONEY_COL, "sum"),
            orders=(order_col, "nunique"),
        )
        print("year x month (last 3):\n", by_ym.tail(3))

    if "C" in ROUTE:
        margin = clean.groupby("category")[[MONEY_COL, PROFIT_COL]].sum()
        margin["margin_pct"] = margin[PROFIT_COL] / margin[MONEY_COL]
        print("margin by category:\n", margin.sort_values("margin_pct", ascending=False).head(3))

        top_products = (
            clean.groupby("product_name")
            .agg(gmv=(MONEY_COL, "sum"), orders=(order_col, "nunique"))
            .sort_values("gmv", ascending=False)
            .head(5)
        )
        print("top products:\n", top_products)

    if people is not None and "B" in ROUTE:
        repeat_rate = (people["orders"] >= 2).mean()
        print("customers", len(people), "repeat%", round(repeat_rate * 100, 1))
        print("ltv median", people["gmv"].median())

        retention = cohort_retention(clean)
        print("retention preview:\n", retention.iloc[:4, :6].round(3))


if __name__ == "__main__":
    main()
