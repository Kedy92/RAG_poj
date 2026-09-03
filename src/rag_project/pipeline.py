from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rag_project.chunking import Chunk, chunk_text
from rag_project.generator import RagAnswer, build_generator
from rag_project.loaders import load_markdown_documents
from rag_project.retriever import TfidfRetriever


@dataclass(frozen=True)
class RagPipeline:
    retriever: TfidfRetriever
    chunks: list[Chunk]

    @classmethod
    def from_documents(
        cls,
        docs_path: str | Path,
        chunk_size: int = 140,
        overlap: int = 35,
    ) -> "RagPipeline":
        documents = load_markdown_documents(docs_path)
        chunks = [
            chunk
            for document in documents
            for chunk in chunk_text(document.source, document.text, chunk_size, overlap)
        ]
        retriever = TfidfRetriever().fit(chunks)
        return cls(retriever=retriever, chunks=chunks)

    def ask(self, question: str, top_k: int = 3) -> RagAnswer:
        contexts = self.retriever.retrieve(question, top_k=top_k)
        return build_generator().generate(question, contexts)
