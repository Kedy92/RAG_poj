# RAG basics

Retrieval-Augmented Generation combines two steps: retrieving relevant information from a document collection, then asking a language model to produce an answer from that information. This approach is useful when knowledge changes frequently or when an organisation has internal documents that were not part of the model's training data.

A typical RAG pipeline contains document ingestion, cleaning, chunking, index creation, retrieval, prompt construction, generation and source citation. The model should not invent an answer when the retrieved context does not contain the requested information.

The main advantage is reducing hallucinations. Another advantage is separating knowledge from the model: documents can be updated without retraining the LLM.
