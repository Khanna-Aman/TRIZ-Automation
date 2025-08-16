# Backup & Restore

## Postgres
- Use pg_dump / pg_restore; store dumps in MinIO

## Neo4j
- Use neo4j-admin dump/load; stop DB before restore

## Qdrant
- Snapshot API: http://localhost:6333/dashboard#/snapshots
- Automate periodic snapshots and store in MinIO

## MinIO
- Use mc (MinIO client) for bucket syncs; versioning recommended

