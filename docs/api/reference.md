# API Reference (Initial)

## Orchestrator
- POST /problems/start
  - Body: {"problem_statement": string, "context"?: string}
  - Headers: X-API-Key (optional, if configured)
  - Response: {status, input, triz, lateral, evaluation}

## TRIZ
- GET /triz/lookup?improving=&worsening= → [int]
- GET /triz/principles → [{id,name,description}]
- GET /triz/parameters → [{id,name,description}]
- POST /triz/resolve → {principles: [int], solutions: [string]}

## Lateral
- POST /lateral/generate → {ideas: [{technique, idea}]}

## Eval
- POST /evaluate → {ranked: [string], metrics: {...}}

Curl example:
```bash
curl -X POST http://localhost:8000/problems/start \
  -H 'Content-Type: application/json' \
  -d '{"problem_statement":"Reduce drone weight"}'
```

