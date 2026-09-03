# Evaluation RAG

Evaluating a RAG system requires measuring both retrieval and generation. For retrieval, useful metrics include precision@k, recall@k, mean reciprocal rank and expected-document coverage. For generation, we measure relevance, factuality, groundedness and the presence of correct citations.

Common errors include poor chunking, an incomplete index, outdated documents, an overly permissive prompt and missing source verification. A good evaluation contains test questions, expected answers and the passages that should be retrieved.

Production monitoring should track latency, cost, unanswered questions, sources used and user feedback.
