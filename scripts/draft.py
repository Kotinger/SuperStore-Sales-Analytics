import pandas as pd

df = pd.read_csv (r"data\SuperStoreOrders - SuperStoreOrders.csv")

"""

#step1
print(df.shape)

#['order_id', 'order_date', 'ship_date', 'ship_mode', 'customer_name', 'segment', 'state', 'country', 'market', 
'region', 'product_id', 'category', 'sub_category', 'product_name', 'sales', 'quantity', 'discount', 'profit', 'shipping_cost', 
'order_priority', 'year']
print(df.columns.tolist())
print (df.isna().sum())

#step2 Зерно
order_col = "order_id"
#print(df["order_id"].nunique())
check = df.groupby(order_col).size().describe()
print(check)

#step3
df["sales"]= df["sales"].astype(float)
df["sales"]=df["sales"].str.replace(",","",regex=False)
df["sales"]=pd.to_numeric(df["sales"])
print (df.dtypes)
print (df ["sales"].head(5))

dmy1= pd.to_datetime(df["order_date"], dayfirst=True, errors="coerce")
#mdy1= pd.to_datetime(df["order_date"], dayfirst=False, errors="coerce")
dmy2= pd.to_datetime(df["ship_date"], dayfirst=True, errors="coerce")
#mdy2= pd.to_datetime(df["ship_date"], dayfirst=False, errors="coerce")
print("Сколько не пустых dmy order_date", dmy1.notna().sum())
#print("Сколько не пустых mdy order_date", mdy1.notna().sum())
print("Сколько не пустых dmy order_date", dmy2.notna().sum())
#print("Сколько не пустых mdy order_date", mdy2.notna().sum())

delay = (df["ship_date"]- df["order_date"]).dt.days
print (delay.min(),delay.max(), delay.median())
"""

#step3
df["sales"]=df["sales"].str.replace(",","",regex=False)
df["sales"]=pd.to_numeric(df["sales"])

df["order_date"]=pd.to_datetime(df["order_date"], dayfirst=True)
df["ship_date"]=pd.to_datetime(df["ship_date"], dayfirst=True)
df["ship_days"] = (df["ship_date"]- df["order_date"]).dt.days

#order_col = "order_id"
#money_col = "sales"
#print(df[money_col].sum())


#step4 Чистка
clean = df.copy()

clean = clean[clean["sales"]>0]
#print("sales<0", len(clean))

"""
#strp5 sanity
print("--- sanity ---")
print("rows", len(df), "->", len(clean))
print("orders", df["order_id"].nunique(), "->", clean["order_id"].nunique())
print("gmv", clean["sales"].sum())
print("dates", clean["order_date"].min(), "->", clean["order_date"].max())
print("sales min", clean["sales"].min(), "qty min", clean["quantity"].min())
"""

#step6 Ключи
order_col = "order_id"
money_col = "sales"

head_cols = ["order_date", "customer_name", "country"]
check = clean.groupby(order_col)[head_cols].nunique()
bad = (check[head_cols]>1).any(axis=1)
#print (bad.sum())

clean["order_key"]= (
    clean["order_id"].astype(str)
    +"|"
    +clean["order_date"].astype(str)
    +"|"
    +clean["customer_name"].astype(str)
    +"|"
    +clean["country"]
    )
#print(clean["order_id"].nunique())
#print(clean["order_key"].nunique())

client_col = "customer_key"
clean[client_col] = (
    clean["customer_name"].astype(str)
    + "|"
    + clean["country"]
)
#print(clean["customer_name"].nunique())
#print(clean[client_col].nunique())

order_col = "order_key"
check2=clean.groupby(order_col)[head_cols].nunique()
#print((check2>1).any(axis=1).sum())

people = (
    clean.groupby(client_col, as_index=False)
    .agg(
        orders=(order_col, "nunique"),
        gmv=(money_col, "sum"),
        lines=(client_col, "size"),
        first_order=("order_date", "min"),
    )
)
#print(len(clean), len(people))

#step7 Метрики

gmv = clean[money_col].sum()
orders = clean[order_col].nunique()
lines = len(clean)
aov = gmv / orders

#print(gmv)
#print(orders)
#print(lines)
#print(aov)
#print(lines/orders)


c = clean.groupby("country").agg(
    gmv = (money_col, "sum"),
    orders = (order_col, "nunique")
)
c["aov"]= c["gmv"] / c["orders"]
#print(c.sort_values("gmv", ascending=False).head(5))

y = clean.groupby("year").agg(
    gmv = (money_col, "sum"),
    orders = (order_col,"nunique")
)
y["aov"] = y["gmv"] / y["orders"]
#print(y.sort_values("aov", ascending=False).head(5))

clean["month"]= clean["order_date"].dt.month
y_m = clean.groupby(["year", "month"]).agg(
    gmv=(money_col, "sum"),
    orders=(order_col, "nunique")
)
y_m["aov"]=y_m["gmv"] / y_m["orders"]
#print(y_m)

y_mom=clean[clean["year"] == 2013].copy()
m = y_mom.groupby("month", as_index=False)["profit"].sum()
m=m.sort_values("month")
m["prev"]=m["profit"].shift(1)
m["mom"]=m["profit"].pct_change()
#print(m)

m1 = clean.groupby(["year", "month"], as_index=False).agg(
    profit=("profit", "sum")).sort_values(["year", "month"]
)
m1["prev"]=m1["profit"].shift(1)
m1["mom"]=m1["profit"].pct_change()
#print(m1)

profit_col= "profit"
dim_col = "category"
product_col="product_name"
x = clean.groupby(dim_col)[[money_col, profit_col]].sum()
x["margin"]=x[profit_col] / x[money_col]
#print(x.head(10))
qty = "quantity"
t = clean.groupby(product_col).agg(
    gmv=(money_col, "sum"),
    qty=(qty, "sum"),
    orders=(order_col, "nunique")
)
#print(t.sort_values("gmv", ascending=False).head(5))

repeat_rate = (people["orders"] >= 2).mean()

#print("repeat_rate", round(repeat_rate * 100, 1), "%")
#print("ltv median", people["gmv"].median())
#print(people.sort_values("gmv", ascending=False).head(5))

orders_tbl = (
    clean.groupby([client_col, order_col], as_index=False)
    .agg(order_date=("order_date", "min"))
)
orders_tbl["order_month"] = orders_tbl["order_date"].dt.to_period("M")
first_cohort = orders_tbl.groupby(client_col)["order_month"].min().rename("cohort")
orders_tbl = orders_tbl.join(first_cohort, on=client_col)
orders_tbl["period_n"] = (
    orders_tbl["order_month"].astype(int) - orders_tbl["cohort"].astype(int)
)

cohort_size = orders_tbl.groupby("cohort")[client_col].nunique()
active = orders_tbl.groupby(["cohort", "period_n"])[client_col].nunique()
retention = active.div(cohort_size, level=0).unstack(fill_value=0)
print(retention.iloc[:6, :8].round(3))

#ну и сохраняем для дашборда
#clean.to_parquet(r"data\SuperStoreOrders_clean.parquet", index=False)
#people.to_parquet(r"data\SuperStorePeople.parquet", index=False)