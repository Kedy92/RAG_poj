from __future__ import annotations

from dataclasses import dataclass
import re


WORD_RE = re.compile(r"\w+", re.UNICODE)
STOPWORDS = {
    "a",
    "and",
    "en",
    "for",
    "of",
    "on",
    "the",
    "to",
}


@dataclass(frozen=True)
class Chunk:
    id: str
    source: str
    text: str
    start_word: int
    end_word: int


def tokenize(text: str) -> list[str]:
    return [
        token
        for match in WORD_RE.finditer(text)
        if (token := _normalize_token(match.group(0))) not in STOPWORDS
    ]


def _normalize_token(token: str) -> str:
    token = token.lower()
    if len(token) > 5 and token.endswith(("es", "s")):
        token = token[:-1]
    return token


def chunk_text(source: str, text: str, chunk_size: int = 140, overlap: int = 35) -> list[Chunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    words = text.split()
    if not words:
        return []

    chunks: list[Chunk] = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunks.append(
            Chunk(
                id=f"{source}#{len(chunks) + 1}",
                source=source,
                text=" ".join(chunk_words),
                start_word=start,
                end_word=end,
            )
        )
        if end == len(words):
            break
    return chunks
