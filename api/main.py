from fastapi import FastAPI, HTTPException
from analytics.kpis import frame, summary, grouped, targets
from analytics.insights import generate_insights, alerts

app=FastAPI(title="NexaRetail Analytics API",version="1.0.0")
def ready():
    try:return frame()
    except Exception as e: raise HTTPException(503,"Run the pipeline first") from e
@app.get('/health')
def health(): ready(); return {"status":"ok"}
@app.get('/kpis')
def kpis(): return {"kpis":summary(),"targets":targets()}
@app.get('/sales')
def sales(): return ready().to_dict(orient='records')
@app.get('/products')
def products(): return grouped('product_name').head(25).to_dict(orient='records')
@app.get('/customers')
def customers(): return {"total":summary()["total_customers"]}
@app.get('/regions')
def regions(): return grouped('region').to_dict(orient='records')
@app.get('/alerts')
def get_alerts(): return alerts()
@app.get('/insights')
def get_insights(): return generate_insights()
