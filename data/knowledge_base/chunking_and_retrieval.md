# Chunking and retrieval

Le chunking consiste a couper les documents en passages plus petits. Des chunks trop courts perdent le contexte, tandis que des chunks trop longs ajoutent du bruit et peuvent reduire la precision du retrieval. Un overlap aide a conserver les informations qui se trouvent a la frontiere entre deux chunks.

Le retrieval peut etre lexical, par exemple TF-IDF ou BM25, ou semantique avec des embeddings. TF-IDF est simple, explicable et rapide pour une demo. Les embeddings capturent mieux les synonymes et les formulations differentes, mais demandent un modele d'embedding et souvent une base vectorielle.

En production, une base vectorielle comme FAISS, Chroma ou pgvector permet de stocker les vecteurs et de chercher les passages les plus proches de la question.
