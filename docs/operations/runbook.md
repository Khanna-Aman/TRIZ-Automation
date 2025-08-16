# Runbook

## Common commands
- make build && make up
- make logs
- docker compose -f 11-02-docker-compose.yml ps

## Debugging tips
- Check /health endpoints for each service
- Inspect orchestrator logs for downstream errors (includes stage)
- Verify internal DNS: exec into orchestrator and curl triz:8000

## Common issues
- Postgres unavailable: ensure container is healthy before TRIZ DB calls
- n8n webhook URL mismatch: use the Test URL when executing via editor
- Ports already in use: stop conflicting processes or change mappings

