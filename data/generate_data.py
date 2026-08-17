"""Generate a reproducible, deliberately imperfect NexaRetail source dataset."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import RAW

RNG = np.random.default_rng(20260817)
REGIONS = ["North", "South", "East", "West"]
CATEGORIES = {"Electronics": ["Audio", "Computing", "Mobile"], "Home": ["Kitchen", "Decor"], "Fashion": ["Apparel", "Accessories"], "Sports": ["Fitness", "Outdoor"]}

def generate(output: Path = RAW, n_orders: int = 60000) -> dict[str, int]:
    output.mkdir(parents=True, exist_ok=True)
    n_customers, n_products, n_reps = 5000, 180, 24
    customers = pd.DataFrame({"customer_id": range(1,n_customers+1), "customer_name": [f"Customer {i:05d}" for i in range(1,n_customers+1)], "email": [f"customer{i}@example.test" for i in range(1,n_customers+1)], "signup_date": pd.Timestamp("2023-01-01") + pd.to_timedelta(RNG.integers(0,900,n_customers),unit="D"), "region": RNG.choice(REGIONS,n_customers,p=[.28,.30,.20,.22]), "customer_segment": RNG.choice(["Consumer","Small Business","Enterprise"],n_customers,p=[.65,.28,.07])})
    cats = list(CATEGORIES); product_cat = RNG.choice(cats,n_products,p=[.30,.23,.27,.20])
    prices = np.round(RNG.lognormal(4.2,.55,n_products),2)
    products = pd.DataFrame({"product_id":range(1,n_products+1),"product_name":[f"{c} Product {i:03d}" for i,c in enumerate(product_cat,1)],"category":product_cat,"subcategory":[RNG.choice(CATEGORIES[c]) for c in product_cat],"unit_price":prices,"cost":np.round(prices*RNG.uniform(.42,.72,n_products),2),"launch_date":pd.Timestamp("2022-01-01")+pd.to_timedelta(RNG.integers(0,1000,n_products),unit="D")})
    reps=pd.DataFrame({"sales_rep_id":range(1,n_reps+1),"sales_rep_name":[f"Rep {i:02d}" for i in range(1,n_reps+1)],"region":np.resize(REGIONS,n_reps),"team":RNG.choice(["Growth","Strategic","Inside Sales"],n_reps)})
    dates=pd.date_range("2025-01-01","2026-06-30",freq="D"); weights=np.array([1.6 if d.month in (10,11,12) else 1.2 if d.month in (6,7) else .85 if d.weekday()>4 else 1 for d in dates]); dates=RNG.choice(dates,n_orders,p=weights/weights.sum())
    customer_ids=RNG.choice(customers.customer_id,n_orders); regions=customers.set_index("customer_id").loc[customer_ids,"region"].to_numpy(); statuses=RNG.choice(["completed","cancelled","returned"],n_orders,p=[.91,.045,.045])
    orders=pd.DataFrame({"order_id":range(1,n_orders+1),"customer_id":customer_ids,"order_date":pd.to_datetime(dates).strftime("%Y-%m-%d"),"region":regions,"sales_channel":RNG.choice(["Online","Marketplace","Store","B2B"],n_orders,p=[.48,.20,.22,.10]),"sales_rep_id":RNG.integers(1,n_reps+1,n_orders),"order_status":statuses})
    counts=RNG.choice([1,2,3,4],n_orders,p=[.42,.34,.18,.06]); order_ids=np.repeat(orders.order_id.to_numpy(),counts); product_ids=RNG.choice(products.product_id,len(order_ids),p=np.linspace(2,.3,n_products)/np.linspace(2,.3,n_products).sum()); pmap=products.set_index("product_id")
    items=pd.DataFrame({"order_item_id":range(1,len(order_ids)+1),"order_id":order_ids,"product_id":product_ids,"quantity":RNG.integers(1,5,len(order_ids)),"unit_price":np.round(pmap.loc[product_ids,"unit_price"].to_numpy()*RNG.uniform(.9,1.1,len(order_ids)),2),"discount":np.round(RNG.choice([0,.05,.1,.15,.2],len(order_ids),p=[.35,.25,.22,.12,.06]),2)})
    # intentional quality issues, repaired and reported by the pipeline
    items.loc[RNG.choice(items.index,25,False),"quantity"]=-1; customers.loc[RNG.choice(customers.index,12,False),"region"]=None; orders=pd.concat([orders,orders.iloc[:5]],ignore_index=True)
    for name,frame in {"customers":customers,"products":products,"sales_reps":reps,"orders":orders,"order_items":items}.items(): frame.to_csv(output/f"{name}.csv",index=False)
    return {name:len(frame) for name,frame in {"customers":customers,"products":products,"sales_reps":reps,"orders":orders,"order_items":items}.items()}

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('--orders',type=int,default=60000); args=p.parse_args(); print(generate(n_orders=args.orders))
