from __future__ import annotations
import pandas as pd
from analytics.kpis import frame
def daily_revenue() -> pd.DataFrame:
    d=frame(); x=d[d.order_status=="completed"].groupby("order_date",as_index=False).net_revenue.sum().rename(columns={"net_revenue":"revenue"}); x["rolling_7d"]=x.revenue.rolling(7,min_periods=1).mean(); return x
def monthly_revenue() -> pd.DataFrame:
    x=daily_revenue(); x["month"]=x.order_date.dt.to_period("M").astype(str); x=x.groupby("month",as_index=False).revenue.sum(); x["mom_growth"]=x.revenue.pct_change(); return x
