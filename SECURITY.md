## Security Policy

### Supported Versions
- This is an MVP under active development. Security hardening is ongoing.

### Reporting a Vulnerability
- Please open a private issue or contact the maintainers directly.
- Provide reproduction steps and impact if possible.

### Secrets
- Do not commit secrets. Use environment variables or a secret manager in production (e.g., Vault).

### Hardening Roadmap (high-level)
- API Gateway + Keycloak for authN/Z
- TLS termination at gateway; mTLS for internal services (prod)
- Non-root containers, read-only FS, image digest pinning
- Rate limiting, CORS, request size limits
- OTel traces/metrics/logs + centralized alerting
- SCA and container scanning in CI (pip-audit, trivy)

