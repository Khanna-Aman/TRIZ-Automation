# ADR 0001: Orchestration choice

## Context
We need external and internal orchestration for multi-step/agent workflows.

## Decision
- Internal cognition: LangGraph (stateful graph in Python)
- External automation: n8n (visual workflows, HTTP integrations)

## Status
Accepted (MVP). May revisit for strict-OSI licensing needs.

## Consequences
- Clear separation between internal thought processes and external I/O
- If strict OSI only is required, consider Node-RED/Huginn/Temporal/Argo as alternatives to n8n

