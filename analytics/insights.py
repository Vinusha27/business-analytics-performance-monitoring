from __future__ import annotations
from analytics.kpis import grouped, summary
from analytics.trends import monthly_revenue
def generate_insights():
    k=summary(); cat=grouped("category").iloc[0]; reg=grouped("region").iloc[0]; m=monthly_revenue(); growth=float(m.mom_growth.iloc[-1]) if len(m)>1 else 0
    return [f"Latest monthly revenue changed {growth:+.1%} versus the prior month.",f"{cat.category} is the leading category at ${cat.revenue:,.0f} in completed revenue.",f"{reg.region} is the strongest region at ${reg.revenue:,.0f} in completed revenue.",f"Gross margin is {k['gross_margin']:.1%}, with ${k['gross_profit']:,.0f} gross profit."]
def alerts():
    k=summary(); a=[]
    if k["return_rate"]>.06:a.append("HIGH: Return rate is above the 6% operating threshold.")
    if k["cancellation_rate"]>.05:a.append("HIGH: Cancellation rate is above the 5% operating threshold.")
    if k["gross_margin"]<.35:a.append("MEDIUM: Gross margin is below the 35% target.")
    return a or ["No material KPI threshold breaches detected."]
