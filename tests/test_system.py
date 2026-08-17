from data.generate_data import generate
from pipeline.run_pipeline import run_pipeline
from analytics.kpis import summary, frame
from analytics.anomaly_detection import detect_daily_revenue_anomalies
def setup_module(): generate(n_orders=1000); run_pipeline()
def test_pipeline_repairs_bad_data(): assert run_pipeline()['records_rejected'] > 0
def test_kpis_are_real(): assert summary()['total_revenue'] > 0 and summary()['gross_profit'] > 0
def test_no_negative_loaded_quantities(): assert (frame().quantity>0).all()
def test_anomaly_returns_dataframe(): assert hasattr(detect_daily_revenue_anomalies(),'columns')
def test_api_health_and_kpis():
    from fastapi.testclient import TestClient
    from api.main import app
    client=TestClient(app)
    assert client.get('/health').status_code == 200
    assert client.get('/kpis').json()['kpis']['total_revenue'] > 0
