from __future__ import annotations
from pathlib import Path
import pandas as pd
from analytics.kpis import summary, grouped, targets
from analytics.insights import generate_insights, alerts
OUT=Path(__file__).parent/'output'
def generate():
    OUT.mkdir(exist_ok=True); k=summary(); pd.DataFrame([k]).to_csv(OUT/'kpi_summary.csv',index=False); html=f"<h1>NexaRetail Executive Report</h1><h2>KPI Summary</h2>{pd.DataFrame([k]).to_html(index=False)}<h2>Target Performance</h2>{pd.DataFrame(targets(k)).to_html(index=False)}<h2>Insights</h2><ul>"+''.join(f'<li>{x}</li>' for x in generate_insights())+"</ul><h2>Alerts</h2><ul>"+''.join(f'<li>{x}</li>' for x in alerts())+'</ul><h2>Top Products</h2>'+grouped('product_name').head(10).to_html(index=False); (OUT/'executive_report.html').write_text(html); return OUT
if __name__=='__main__': print(generate())
