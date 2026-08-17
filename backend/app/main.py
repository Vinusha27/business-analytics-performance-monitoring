from datetime import datetime
from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import func
from sqlalchemy.orm import Session
from .db import Base, engine, get_db, SessionLocal
from .models import User, Organization, Agent, Workflow, Execution, Recommendation
from .security import bearer, create_token, hash_password, read_token, verify_password
from .ai import MockProvider

app = FastAPI(title="VentureFlow AI API", version="1.0.0", description="AI agents and workflow automation for business operations.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://localhost:8000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class RegisterIn(BaseModel): name: str; email: EmailStr; password: str = Field(min_length=8)
class LoginIn(BaseModel): email: EmailStr; password: str
class AgentIn(BaseModel): name: str; description: str = ""; system_prompt: str = ""; model: str = "mock-business-analyst"; status: str = "active"; configuration: dict = {}
class WorkflowIn(BaseModel): name: str; description: str = ""; status: str = "active"; trigger_type: str = "manual"; configuration: dict = {"nodes": ["START", "ANALYSIS", "RECOMMENDATION", "END"]}
class RunIn(BaseModel): input_data: dict = {}

def current_user(credentials=Depends(bearer), db: Session = Depends(get_db)):
    user = db.get(User, read_token(credentials))
    if not user: raise HTTPException(401, "User not found")
    return user
def payload(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}
def org_for(user): return user.organization_id

@app.on_event("startup")
def bootstrap():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        if db.query(User).count(): return
        org = Organization(name="VentureFlow Demo"); db.add(org); db.flush()
        user = User(name="Demo User", email="demo@ventureflow.ai", password_hash=hash_password("DemoPass123!"), organization_id=org.id); db.add(user); db.flush(); org.owner_id=user.id
        analyst=Agent(organization_id=org.id,name="Operations Analyst",description="Finds bottlenecks and growth opportunities.",system_prompt="Analyze business operations safely.")
        sales=Agent(organization_id=org.id,name="Revenue Intelligence",description="Turns sales signals into practical actions.",system_prompt="Summarize commercial performance.")
        db.add_all([analyst,sales]); db.flush()
        wf=Workflow(organization_id=org.id,name="Weekly Sales Performance Analysis",description="Analyzes sales performance and creates a prioritized action.",trigger_type="weekly",configuration={"nodes":["START","DATA ANALYSIS","AI AGENT","RECOMMENDATION","END"]}); db.add(wf); db.flush()
        for i in range(5): db.add(Execution(workflow_id=wf.id,status="success" if i!=3 else "failed",input_data={"week":i+1},output_data={"summary":"Performance reviewed"},duration=1.1+i*.2,completed_at=datetime.utcnow()))
        db.add_all([Recommendation(organization_id=org.id,category="Automation",title="Automate weekly sales reporting",description="The recurring reporting workflow can save approximately 18 hours per month by consolidating inputs and sending an AI summary.",impact_score=9,effort_score=4,priority="High",confidence=91), Recommendation(organization_id=org.id,category="Operations",title="Review the lowest-performing sales segment",description="Use a weekly exception review to isolate declining conversion before it impacts forecast attainment.",impact_score=7,effort_score=3,priority="Medium",confidence=82)])
        db.commit()
    finally: db.close()

@app.get("/health")
def health(): return {"status":"healthy", "provider":"mock", "time":datetime.utcnow()}
@app.post("/auth/register")
def register(data:RegisterIn, db:Session=Depends(get_db)):
    if db.query(User).filter_by(email=data.email).first(): raise HTTPException(409,"Email already registered")
    org=Organization(name=f"{data.name}'s workspace"); db.add(org); db.flush(); user=User(name=data.name,email=data.email,password_hash=hash_password(data.password),organization_id=org.id); db.add(user); db.flush(); org.owner_id=user.id; db.commit(); return {"access_token":create_token(user.id),"token_type":"bearer","user":payload(user)}
@app.post("/auth/login")
def login(data:LoginIn,db:Session=Depends(get_db)):
    user=db.query(User).filter_by(email=data.email).first()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Incorrect email or password")
    return {"access_token":create_token(user.id),"token_type":"bearer","user":payload(user)}
@app.get("/auth/me")
def me(user=Depends(current_user)): return payload(user)

@app.get("/agents")
def agents(user=Depends(current_user),db:Session=Depends(get_db)): return [payload(x) for x in db.query(Agent).filter_by(organization_id=org_for(user)).all()]
@app.post("/agents")
def create_agent(data:AgentIn,user=Depends(current_user),db:Session=Depends(get_db)):
    x=Agent(organization_id=org_for(user),**data.model_dump()); db.add(x); db.commit(); db.refresh(x); return payload(x)
@app.get("/agents/{agent_id}")
def get_agent(agent_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    x=db.get(Agent,agent_id)
    if not x or x.organization_id != org_for(user): raise HTTPException(404,"Agent not found")
    return payload(x)
@app.put("/agents/{agent_id}")
def update_agent(agent_id:int,data:AgentIn,user=Depends(current_user),db:Session=Depends(get_db)):
    x=get_agent(agent_id,user,db)
    obj=db.get(Agent,agent_id)
    for k,v in data.model_dump().items(): setattr(obj,k,v)
    db.commit(); return payload(obj)
@app.delete("/agents/{agent_id}")
def delete_agent(agent_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    obj=db.get(Agent,agent_id)
    if not obj or obj.organization_id!=org_for(user): raise HTTPException(404,"Agent not found")
    db.delete(obj);db.commit();return {"deleted":True}
@app.post("/agents/{agent_id}/execute")
def execute_agent(agent_id:int,data:RunIn,user=Depends(current_user),db:Session=Depends(get_db)):
    get_agent(agent_id,user,db); return MockProvider().execute(data.input_data.get("request","Analyze the business"),data.input_data)

@app.get("/workflows")
def workflows(user=Depends(current_user),db:Session=Depends(get_db)): return [payload(x) for x in db.query(Workflow).filter_by(organization_id=org_for(user)).all()]
@app.post("/workflows")
def create_workflow(data:WorkflowIn,user=Depends(current_user),db:Session=Depends(get_db)):
    x=Workflow(organization_id=org_for(user),**data.model_dump());db.add(x);db.commit();db.refresh(x);return payload(x)
@app.get("/workflows/{workflow_id}")
def get_workflow(workflow_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    x=db.get(Workflow,workflow_id)
    if not x or x.organization_id!=org_for(user): raise HTTPException(404,"Workflow not found")
    return payload(x)
@app.post("/workflows/{workflow_id}/run")
def run_workflow(workflow_id:int,data:RunIn,user=Depends(current_user),db:Session=Depends(get_db)):
    wf=db.get(Workflow,workflow_id); get_workflow(workflow_id,user,db); result=MockProvider().execute("workflow",data.input_data); e=Execution(workflow_id=wf.id,status="success",input_data=data.input_data,output_data={"nodes":[{"name":n,"status":"success"} for n in wf.configuration.get("nodes",[])],"result":result},duration=.8,completed_at=datetime.utcnow());db.add(e);db.commit();db.refresh(e);return payload(e)
@app.get("/workflows/{workflow_id}/executions")
def workflow_executions(workflow_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    get_workflow(workflow_id,user,db);return [payload(x) for x in db.query(Execution).filter_by(workflow_id=workflow_id).order_by(Execution.id.desc()).all()]
@app.get("/executions/{execution_id}")
def execution(execution_id:int,user=Depends(current_user),db:Session=Depends(get_db)):
    x=db.get(Execution,execution_id)
    if not x: raise HTTPException(404,"Execution not found")
    get_workflow(x.workflow_id,user,db);return payload(x)
@app.get("/analytics/overview")
def overview(user=Depends(current_user),db:Session=Depends(get_db)):
    oid=org_for(user); wids=[x[0] for x in db.query(Workflow.id).filter_by(organization_id=oid)]; executions=db.query(Execution).filter(Execution.workflow_id.in_(wids)).all(); total=len(executions); success=sum(x.status=="success" for x in executions)
    return {"total_workflows":len(wids),"active_agents":db.query(Agent).filter_by(organization_id=oid,status="active").count(),"executions_today":total,"success_rate":round(success/total*100) if total else 0,"average_execution_time":round(sum(x.duration for x in executions)/total,2) if total else 0,"recommendations_generated":db.query(Recommendation).filter_by(organization_id=oid).count(),"execution_trend":[{"label":f"Run {i+1}","success":1 if x.status=="success" else 0,"failed":1 if x.status=="failed" else 0} for i,x in enumerate(executions)]}
@app.get("/analytics/executions")
def analytics_executions(user=Depends(current_user),db:Session=Depends(get_db)): return overview(user,db)["execution_trend"]
@app.get("/recommendations")
def recommendations(user=Depends(current_user),db:Session=Depends(get_db)): return [payload(x) for x in db.query(Recommendation).filter_by(organization_id=org_for(user)).order_by(Recommendation.impact_score.desc()).all()]
@app.post("/recommendations/{recommendation_id}/{action}")
def update_recommendation(recommendation_id:int,action:str,user=Depends(current_user),db:Session=Depends(get_db)):
    if action not in {"accept","dismiss","implement"}: raise HTTPException(400,"Invalid action")
    x=db.get(Recommendation,recommendation_id)
    if not x or x.organization_id!=org_for(user): raise HTTPException(404,"Recommendation not found")
    x.status={"accept":"accepted","dismiss":"dismissed","implement":"implemented"}[action];db.commit();return payload(x)

web = Path(__file__).resolve().parents[2] / "frontend"
if web.exists(): app.mount("/", StaticFiles(directory=web, html=True), name="web")
