# VentureFlow AI architecture

VentureFlow is a FastAPI application with a static responsive dashboard. The REST layer authenticates users with signed JWTs, scopes queries to their organization, and uses SQLAlchemy models for users, organizations, agents, workflows, executions, and recommendations.

The provider boundary (`app/ai.py`) exposes a deterministic mock business analyst. It returns a safe execution plan, tool activity summary, metrics, and a final recommendation; no hidden reasoning is stored or shown. Workflow runs record node outcomes and feed the analytics queries. SQLite makes the demo zero-configuration, while `DATABASE_URL` supports PostgreSQL-compatible SQLAlchemy deployments.
