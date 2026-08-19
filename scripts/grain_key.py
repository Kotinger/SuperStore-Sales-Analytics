import pandas as pd

df = pd.read_csv (r"data\SuperStoreOrders - SuperStoreOrders.csv")
"""
#step1
print(df.shape)
print (df ["order_id"].unique())
print(df.head(5))

#step2
print (df.isna().sum())

#step3
df["sales"]= df["sales"].astype(float)
df["sales"]=df["sales"].str.replace(",","",regex=False)
df["sales"]=pd.to_numeric(df["sales"])
print (df.dtypes)
print (df ["sales"].head(5))

#step4
dmy1= pd.to_datetime(df["order_date"], dayfirst=True, errors="coerce")
#mdy1= pd.to_datetime(df["order_date"], dayfirst=False, errors="coerce")
dmy2= pd.to_datetime(df["ship_date"], dayfirst=True, errors="coerce")
#mdy2= pd.to_datetime(df["ship_date"], dayfirst=False, errors="coerce")
print("Сколько не пустых dmy order_date", dmy1.notna().sum())
#print("Сколько не пустых mdy order_date", mdy1.notna().sum())
print("Сколько не пустых dmy order_date", dmy2.notna().sum())
#print("Сколько не пустых mdy order_date", mdy2.notna().sum())

#step5
delay = (df["ship_date"]- df["order_date"]).dt.days
print (delay.min(),delay.max(), delay.median())
"""
#step3
df["sales"]=df["sales"].str.replace(",","",regex=False)
df["sales"]=pd.to_numeric(df["sales"])

#step4
df["order_date"]=pd.to_datetime(df["order_date"], dayfirst=True)
df["ship_date"]=pd.to_datetime(df["ship_date"], dayfirst=True)

#step5
df["ship_days"] = (df["ship_date"]- df["order_date"]).dt.days


"""
#step6
#просто треню groupby изучаю че в датасете 
check = df.groupby("order_id")[["order_date", "customer_name"]].nunique()
print ((check>1).any(axis=1).sum())

check2 = df.groupby("year")["sales"].sum()
print (check2)

check3 = df.groupby("customer_name")["country"].nunique()
print ((check3>1).sum())

check4 = df.groupby("order_id")["customer_name"].nunique()
print ((check4>1).sum())

check5 = df.groupby("market")["sales"].sum()
print (check5)

check6 = df.groupby("market")[["sales", "profit"]].sum()
print (check6)

check7= df.groupby ("product_id")[["profit", "sales", "quantity"]].sum()
print (check7)

check8 = df.groupby ("ship_mode").agg(
    mean_ship_days = ("ship_days", "mean"),
    number_of_positions = ("order_id", "size")
    )
print (check8)

check9 = df.groupby ("year").agg(
gmv = ("sales", "sum"),
n_orders = ("order_id", "nunique"))
check9["aov"] = check9["gmv"]/check9["n_orders"]
print (check9)

check10 = df.groupby(["market","category"])["sales"].sum().sort_values(ascending=False)
print(check10)

check11 = df.groupby("country")["sales"].sum().sort_values(ascending=False)
print(check11.head(5))

check12 = df.groupby("segment")[["sales", "profit"]].sum()
check12["margin"]= check12["profit"]/check12["sales"]
print(check12)

check13 = df.groupby("product_id")["profit"].sum()
print((check13<0).sum())

check14 =  df.groupby("category").agg(
   a = ("order_id", "nunique"),
   b = ("order_id", "size")
)
check14["c"] = check14 ["b"]/check14["a"]
print (check14)

check15= df[df["year"]== 2014].groupby("region")["sales"].sum() 

print (check15)
"""
#step7
df["customer_key"]=df["customer_name"]+"|" + df["country"]
df["order_key"]=df["order_id"].astype(str)+ "|" + df["order_date"].astype(str) +"|" + df["customer_name"]+"|" + df["country"] 
print(df["customer_key"].nunique())
print(df["order_key"].nunique())

#ну и сохраняем
df.to_parquet(r"data\SuperStoreOrders.parquet", index=False )