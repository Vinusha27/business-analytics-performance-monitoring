from __future__ import annotations
import sqlite3, pandas as pd
from config import DB_PATH, TARGETS

BASE="""SELECT o.order_id,o.order_date,o.region,o.sales_channel,o.order_status,p.category,p.product_name,oi.quantity,oi.unit_price,oi.discount,p.cost, o.customer_id FROM orders o JOIN order_items oi ON o.order_id=oi.order_id JOIN products p ON oi.product_id=p.product_id"""
def frame() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as c: d=pd.read_sql_query(BASE,c)
    d["net_revenue"]=d.quantity*d.unit_price*(1-d.discount); d["cost_total"]=d.quantity*d.cost; d["profit"]=d.net_revenue-d.cost_total; d["order_date"]=pd.to_datetime(d.order_date); return d
def summary(d: pd.DataFrame|None=None) -> dict[str,float]:
    d=frame() if d is None else d; all_orders=d.order_id.nunique(); complete=d[d.order_status=="completed"]; completed=complete.order_id.nunique(); net=complete.net_revenue.sum(); gross=(complete.quantity*complete.unit_price).sum(); profit=complete.profit.sum()
    return {"total_revenue":round(net,2),"gross_revenue":round(gross,2),"total_orders":all_orders,"completed_orders":completed,"cancelled_orders":d[d.order_status=='cancelled'].order_id.nunique(),"returned_orders":d[d.order_status=='returned'].order_id.nunique(),"average_order_value":round(net/max(completed,1),2),"units_sold":int(complete.quantity.sum()),"gross_profit":round(profit,2),"gross_margin":round(profit/max(net,1),4),"total_customers":int(d.customer_id.nunique()),"completion_rate":round(completed/max(all_orders,1),4),"return_rate":round(d[d.order_status=='returned'].order_id.nunique()/max(all_orders,1),4),"cancellation_rate":round(d[d.order_status=='cancelled'].order_id.nunique()/max(all_orders,1),4)}
def grouped(column:str,d:pd.DataFrame|None=None)->pd.DataFrame:
    d=frame() if d is None else d; return d[d.order_status=="completed"].groupby(column,as_index=False).agg(revenue=("net_revenue","sum"),profit=("profit","sum"),orders=("order_id","nunique"),units=("quantity","sum")).sort_values("revenue",ascending=False)
def targets(k:dict[str,float]|None=None)->list[dict[str,object]]:
    k=summary() if k is None else k; vals={"monthly_revenue":k["total_revenue"]/18,"completion_rate":k["completion_rate"],"gross_margin":k["gross_margin"],"return_rate":k["return_rate"],"cancellation_rate":k["cancellation_rate"],"aov":k["average_order_value"]}; out=[]
    for name,target in TARGETS.items():
        actual=vals[name]; lower_is_better=name.endswith("_rate") and name not in ("completion_rate",); achievement=(target/actual if lower_is_better and actual else actual/target); out.append({"metric":name,"actual":round(actual,4),"target":target,"achievement":round(achievement,3),"status":"On Track" if achievement>=1 else "Below Target"})
    return out
