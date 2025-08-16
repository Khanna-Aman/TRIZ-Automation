# ADR 0002: Graph and Vector Datastores

## Context
We need a graph DB and a vector DB for RAG-Graph.

## Decision
- Graph: Neo4j Community (GPLv3)
- Vector: Qdrant (Apache-2.0)

## Status
Accepted (MVP). Alternatives considered: ArangoDB (Apache-2.0), Weaviate/Milvus.

## Consequences
- Neo4j ecosystem and Cypher simplify graph work; consider ArangoDB if license constraints arise
- Qdrant is simple and performant for vectors; OSS-friendly

