# RAG-Graph Model (Initial)

## Nodes (examples)
- Document, Chunk, Entity, Concept, Principle, Parameter, Idea

## Relationships (examples)
- HAS_CHUNK, MENTIONS, RELATES_TO, SUGGESTS, DERIVES_FROM, SUPPORTS

## Notes
- Store entities and relations in Neo4j; vectors in Qdrant
- Hybrid retrieval: vector search → k-hop graph expansion → fusion/rerank
- Provide Cypher examples in future iterations

