# Workflows

Workflows use a small, explicit node sequence stored in `configuration.nodes`: `START`, `ANALYSIS`, `AI AGENT`, `RECOMMENDATION`, `END`. A run executes that sequence, persists its input, result, status, duration, and per-node summaries. Scheduled trigger values are captured (`manual`, `daily`, `weekly`) for an external scheduler/worker deployment.
