import sys
import os
from pathlib import Path
os.environ.setdefault("JWT_SECRET", "test-only-secret-that-is-long-enough-for-hs256")
sys.path.insert(0, str(Path(__file__).parents[1] / "backend"))
from fastapi.testclient import TestClient
from app.main import app, bootstrap
bootstrap()
client = TestClient(app)
def auth():
    r=client.post('/auth/login',json={'email':'demo@ventureflow.ai','password':'DemoPass123!'})
    return {'Authorization':'Bearer '+r.json()['access_token']}
def test_health(): assert client.get('/health').status_code==200
def test_auth_and_agents():
    h=auth(); assert client.get('/auth/me',headers=h).status_code==200
    r=client.post('/agents',headers=h,json={'name':'Test agent'}); assert r.status_code==200
    assert client.post(f"/agents/{r.json()['id']}/execute",headers=h,json={'input_data':{'rows':[{'revenue':100}]}}).json()['tool_calls']
def test_workflow_analytics_recommendations():
    h=auth(); w=client.post('/workflows',headers=h,json={'name':'Test workflow'}).json()
    assert client.post(f"/workflows/{w['id']}/run",headers=h,json={'input_data':{}}).status_code==200
    assert client.get('/analytics/overview',headers=h).json()['total_workflows'] >= 1
    assert client.get('/recommendations',headers=h).status_code==200
