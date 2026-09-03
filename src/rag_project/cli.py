from __future__ import annotations

import argparse
from pathlib import Path

from rag_project.pipeline import RagPipeline


DEFAULT_DOCS = Path(__file__).resolve().parents[2] / "data" / "knowledge_base"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local RAG demo for an ML interview")
    parser.add_argument("question", help="Question to ask the documents")
    parser.add_argument("--docs", default=str(DEFAULT_DOCS), help="Markdown file or directory")
    parser.add_argument("--top-k", type=int, default=3, help="Number of chunks to retrieve")
    parser.add_argument("--chunk-size", type=int, default=140, help="Chunk size in words")
    parser.add_argument("--overlap", type=int, default=35, help="Chunk overlap in words")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    pipeline = RagPipeline.from_documents(
        args.docs,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )
    answer = pipeline.ask(args.question, top_k=args.top_k)
    print(answer.answer)
    if answer.citations:
        print("\nSources:")
        for citation in answer.citations:
            print(f"- {citation}")


if __name__ == "__main__":
    main()
