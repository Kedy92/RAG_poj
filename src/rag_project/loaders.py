from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    source: str
    text: str


def load_markdown_documents(path: str | Path) -> list[Document]:
    root = Path(path)
    if not root.exists():
        raise FileNotFoundError(f"Document path not found: {root}")

    files = [root] if root.is_file() else sorted(root.rglob("*.md"))
    documents: list[Document] = []
    for file_path in files:
        if file_path.name.startswith("."):
            continue
        text = file_path.read_text(encoding="utf-8").strip()
        if text:
            documents.append(Document(source=str(file_path), text=text))
    return documents
