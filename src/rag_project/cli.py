from __future__ import annotations

import argparse
from pathlib import Path

from rag_project.pipeline import RagPipeline


DEFAULT_DOCS = Path(__file__).resolve().parents[2] / "data" / "knowledge_base"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Demo RAG locale pour entretien ML")
    parser.add_argument("question", help="Question a poser aux documents")
    parser.add_argument("--docs", default=str(DEFAULT_DOCS), help="Dossier ou fichier Markdown")
    parser.add_argument("--top-k", type=int, default=3, help="Nombre de chunks recuperes")
    parser.add_argument("--chunk-size", type=int, default=140, help="Taille des chunks en mots")
    parser.add_argument("--overlap", type=int, default=35, help="Overlap entre chunks en mots")
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
