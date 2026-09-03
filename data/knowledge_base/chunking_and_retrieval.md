# Chunking and retrieval

Chunking means splitting documents into smaller passages. Chunks that are too short lose context, while chunks that are too long add noise and can reduce retrieval precision. Overlap helps preserve information located at the boundary between two chunks.

Retrieval can be lexical, for example TF-IDF or BM25, or semantic using embeddings. TF-IDF is simple, explainable and fast for a demo. Embeddings capture synonyms and different phrasing better, but require an embedding model and often a vector database.

In production, a vector database such as FAISS, Chroma or pgvector can store vectors and search for passages closest to the question.
