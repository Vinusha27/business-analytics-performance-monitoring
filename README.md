# VentureFlow AI

VentureFlow AI is a runnable SaaS-style MVP for connecting business processes, having AI analyze them, automating repeatable work, and monitoring the results.

## Included

- JWT signup/login and organization-scoped data
- AI agent creation and test execution using a deterministic, no-key mock provider
- Workflow creation, visual node sequences, execution logging, and weekly/manual trigger metadata
- Live KPI analytics calculated from persisted execution records
- Recommendation triage (accept/dismiss) and an interactive REST API at `/docs`
- Responsive browser dashboard, Docker support, seed data, and API tests

## Quick start

```powershell
py -m pip install -r backend/requirements.txt
py -m uvicorn backend.app.main:app --reload --port 8000
```

Open `http://localhost:8000`. The first start creates the local database and demo workspace.

Demo sign-in: `demo@ventureflow.ai` / `DemoPass123!`

Run verification with:

```powershell
py -m pytest tests/test_ventureflow.py
```

## Docker

```powershell
docker compose up --build
```

## Architecture and documentation

See [architecture](docs/architecture.md), [API](docs/api.md), [workflows](docs/workflows.md), and [AI agents](docs/ai-agents.md). The original NexaRetail analytics project remains in the repository; VentureFlow adds a separate operational automation surface that can later consume its analytics pipeline.

## Limitations

The demo is intentionally synchronous and uses SQLite plus a deterministic local AI provider. Production scheduling, Redis jobs, PostgreSQL migrations, and a real LLM adapter are clean extension points rather than silently simulated infrastructure.
