from __future__ import annotations
from analytics.trends import daily_revenue
def detect_daily_revenue_anomalies():
    d=daily_revenue(); q1,q3=d.revenue.quantile(.25),d.revenue.quantile(.75); lo,hi=q1-1.5*(q3-q1),q3+1.5*(q3-q1); return d[(d.revenue<lo)|(d.revenue>hi)].assign(reason="IQR revenue anomaly")
