from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True); name: Mapped[str] = mapped_column(String(120)); email: Mapped[str] = mapped_column(String(255), unique=True, index=True); password_hash: Mapped[str] = mapped_column(String(255)); role: Mapped[str] = mapped_column(String(30), default="member"); organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"), nullable=True); created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(primary_key=True); name: Mapped[str] = mapped_column(String(160)); owner_id: Mapped[int | None] = mapped_column(nullable=True); created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
class Agent(Base):
    __tablename__ = "agents"
    id: Mapped[int] = mapped_column(primary_key=True); organization_id: Mapped[int] = mapped_column(index=True); name: Mapped[str] = mapped_column(String(120)); description: Mapped[str] = mapped_column(Text, default=""); system_prompt: Mapped[str] = mapped_column(Text, default=""); model: Mapped[str] = mapped_column(String(80), default="mock-business-analyst"); status: Mapped[str] = mapped_column(String(20), default="active"); configuration: Mapped[dict] = mapped_column(JSON, default=dict); created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
class Workflow(Base):
    __tablename__ = "workflows"
    id: Mapped[int] = mapped_column(primary_key=True); organization_id: Mapped[int] = mapped_column(index=True); name: Mapped[str] = mapped_column(String(140)); description: Mapped[str] = mapped_column(Text, default=""); status: Mapped[str] = mapped_column(String(20), default="active"); trigger_type: Mapped[str] = mapped_column(String(30), default="manual"); configuration: Mapped[dict] = mapped_column(JSON, default=dict); created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
class Execution(Base):
    __tablename__ = "workflow_executions"
    id: Mapped[int] = mapped_column(primary_key=True); workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"), index=True); status: Mapped[str] = mapped_column(String(20)); input_data: Mapped[dict] = mapped_column(JSON, default=dict); output_data: Mapped[dict] = mapped_column(JSON, default=dict); error: Mapped[str | None] = mapped_column(Text, nullable=True); started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow); completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True); duration: Mapped[float] = mapped_column(Float, default=0)
class Recommendation(Base):
    __tablename__ = "recommendations"
    id: Mapped[int] = mapped_column(primary_key=True); organization_id: Mapped[int] = mapped_column(index=True); category: Mapped[str] = mapped_column(String(50)); title: Mapped[str] = mapped_column(String(180)); description: Mapped[str] = mapped_column(Text); impact_score: Mapped[int] = mapped_column(Integer); effort_score: Mapped[int] = mapped_column(Integer); priority: Mapped[str] = mapped_column(String(20)); status: Mapped[str] = mapped_column(String(30), default="open"); confidence: Mapped[int] = mapped_column(Integer, default=80); created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
