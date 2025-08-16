# Deployment Modes

## Local (Docker Compose)
- Use 11-02-docker-compose.yml
- Configure environment via .env or service-level env vars

## Production (Kubernetes)
- Ingress with Traefik or Kong
- StatefulSets for Postgres/Qdrant/Neo4j/MinIO
- Secrets via Vault or sealed-secrets
- OTel Collector + Prometheus/Grafana/Loki stack
- HPA for workers/serving

## Config per Environment
- Use env vars parsed by Pydantic Settings per service (planned)
- Separate values files / K8s manifests per environment

