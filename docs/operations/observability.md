# Observability

## Metrics
- Prometheus scraping endpoints exposed by services (via prometheus-fastapi-instrumentator)
- Dashboards in Grafana (HTTP latency, error rates, throughput)

## Tracing (planned)
- Add OpenTelemetry SDK to services and OTel Collector in Compose
- Export to Tempo/Jaeger

## Logging
- Standardize on JSON logs, include request_id and trace_id
- Centralize with Loki (planned)

