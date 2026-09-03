from __future__ import annotations

from dataclasses import dataclass
import math

from rag_project.chunking import Chunk, tokenize


@dataclass(frozen=True)
class RetrievalResult:
    chunk: Chunk
    score: float


class TfidfRetriever:
    def __init__(self) -> None:
        self._chunks: list[Chunk] = []
        self._idf: dict[str, float] = {}
        self._vectors: list[dict[str, float]] = []

    def fit(self, chunks: list[Chunk]) -> "TfidfRetriever":
        if not chunks:
            raise ValueError("Cannot fit retriever without chunks")

        self._chunks = chunks
        tokenized = [tokenize(chunk.text) for chunk in chunks]
        document_frequency: dict[str, int] = {}
        for tokens in tokenized:
            for term in set(tokens):
                document_frequency[term] = document_frequency.get(term, 0) + 1

        total_docs = len(chunks)
        self._idf = {
            term: math.log((1 + total_docs) / (1 + df)) + 1
            for term, df in document_frequency.items()
        }
        self._vectors = [self._to_vector(tokens) for tokens in tokenized]
        return self

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        if not self._chunks:
            raise ValueError("Retriever must be fitted before retrieve()")
        if top_k <= 0:
            raise ValueError("top_k must be positive")

        query_vector = self._to_vector(tokenize(query))
        scored = [
            RetrievalResult(chunk=chunk, score=_cosine(query_vector, vector))
            for chunk, vector in zip(self._chunks, self._vectors)
        ]
        scored.sort(key=lambda item: item.score, reverse=True)
        return [item for item in scored[:top_k] if item.score > 0]

    def _to_vector(self, tokens: list[str]) -> dict[str, float]:
        if not tokens:
            return {}

        counts: dict[str, int] = {}
        for token in tokens:
            if token in self._idf:
                counts[token] = counts.get(token, 0) + 1

        total = sum(counts.values())
        if total == 0:
            return {}
        return {term: (count / total) * self._idf[term] for term, count in counts.items()}


def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0

    dot = sum(weight * right.get(term, 0.0) for term, weight in left.items())
    left_norm = math.sqrt(sum(weight * weight for weight in left.values()))
    right_norm = math.sqrt(sum(weight * weight for weight in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)
