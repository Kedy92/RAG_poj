from __future__ import annotations

from dataclasses import dataclass
import json
import os
import textwrap
import urllib.error
import urllib.request

from rag_project.chunking import tokenize
from rag_project.retriever import RetrievalResult


@dataclass(frozen=True)
class RagAnswer:
    answer: str
    citations: list[str]


class ExtractiveGenerator:
    def generate(self, question: str, contexts: list[RetrievalResult]) -> RagAnswer:
        if not contexts:
            return RagAnswer(
                answer="I could not find relevant context in the documents.",
                citations=[],
            )

        bullets = []
        citations = []
        for index, result in enumerate(contexts, start=1):
            excerpt = _relevant_excerpt(result.chunk.text, question, max_sentences=2)
            bullets.append(f"{index}. {excerpt}")
            citations.append(f"{index}: {result.chunk.id} (score={result.score:.3f})")

        answer = (
            f"Question: {question}\n\n"
            "Answer based on retrieved documents:\n"
            + "\n".join(bullets)
        )
        return RagAnswer(answer=answer, citations=citations)


class OllamaGenerator:
    def __init__(self, model: str = "llama3.1", endpoint: str = "http://localhost:11434/api/generate") -> None:
        self.model = model
        self.endpoint = endpoint

    def generate(self, question: str, contexts: list[RetrievalResult]) -> RagAnswer:
        if not contexts:
            return RagAnswer("I could not find relevant context in the documents.", [])

        context_text = "\n\n".join(
            f"[{index}] Source: {result.chunk.id}\n{result.chunk.text}"
            for index, result in enumerate(contexts, start=1)
        )
        prompt = textwrap.dedent(
            f"""
            You are a RAG assistant. Answer only from the provided context.
            If the context is not sufficient, say that clearly.
            Cite sources with [1], [2], etc.

            Question:
            {question}

            Context:
            {context_text}
            """
        ).strip()
        payload = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError) as exc:
            fallback = ExtractiveGenerator().generate(question, contexts)
            return RagAnswer(
                answer=f"Ollama is unavailable ({exc}).\n\n{fallback.answer}",
                citations=fallback.citations,
            )

        citations = [f"{index}: {result.chunk.id} (score={result.score:.3f})" for index, result in enumerate(contexts, start=1)]
        return RagAnswer(answer=body.get("response", "").strip(), citations=citations)


def build_generator() -> ExtractiveGenerator | OllamaGenerator:
    if os.getenv("RAG_GENERATOR", "").lower() == "ollama":
        return OllamaGenerator(model=os.getenv("OLLAMA_MODEL", "llama3.1"))
    return ExtractiveGenerator()


def _first_sentences(text: str, max_sentences: int) -> str:
    parts = [part.strip() for part in text.replace("\n", " ").split(".") if part.strip()]
    selected = parts[:max_sentences]
    suffix = "." if selected else ""
    return ". ".join(selected) + suffix


def _relevant_excerpt(text: str, question: str, max_sentences: int) -> str:
    """Select the most question-relevant sentences for the extractive fallback."""
    sentences = [part.strip() for part in text.replace("\n", " ").split(".") if part.strip()]
    if not sentences:
        return ""

    query_terms = set(tokenize(question))
    scored = []
    for position, sentence in enumerate(sentences):
        sentence_terms = set(tokenize(sentence))
        score = len(query_terms & sentence_terms)
        scored.append((score, position, sentence))

    selected = sorted(scored, key=lambda item: (-item[0], item[1]))[:max_sentences]
    selected.sort(key=lambda item: item[1])
    return ". ".join(item[2] for item in selected) + "."
