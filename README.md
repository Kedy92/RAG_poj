# RAG interview project

This project demonstrates a simple, readable and locally executable RAG pipeline:

1. Markdown document ingestion.
2. Chunking with overlap.
3. TF-IDF indexing.
4. Cosine-similarity retrieval.
5. Answer generation with citations.

By default, the core RAG pipeline works without an external API. It can also call Ollama if a local model is available.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

For the optional Streamlit UI:

```bash
python -m pip install -e ".[ui]"
```

## Quick demo

```bash
python -m rag_project.cli "Explain the principle of RAG and its advantages"
```

Example with a custom document folder:

```bash
python -m rag_project.cli "How can a RAG system classify previous funding applications?" --docs data/red_cross_examples --top-k 4
```

## Streamlit demo

```bash
streamlit run src/rag_project/app.py
```

The UI shows two parts:

- A RAG question-answering panel with cited source chunks.
- A simple application-classification panel that extracts metadata such as program area, geography, donor type, target group, outcomes and indicators.

## Notebook demo

The primary interview walkthrough is `notebooks/red_cross_rag_demo.ipynb`. Open it in Jupyter or VS Code and run the cells from top to bottom:

```bash
jupyter notebook notebooks/red_cross_rag_demo.ipynb
```

It demonstrates ingestion, chunking, retrieval, cited answers, application classification and a small evaluation check using synthetic examples.

Optional Ollama mode:

```bash
ollama pull llama3.1
RAG_GENERATOR=ollama OLLAMA_MODEL=llama3.1 python -m rag_project.cli "What are the risks of poor chunking?"
```

## Tests

```bash
python -m unittest discover -s tests
```

Without editable installation:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m rag_project.cli "Explain the principle of RAG and its advantages"
```

## Architecture

- `rag_project.loaders`: document loading.
- `rag_project.chunking`: chunk creation.
- `rag_project.retriever`: TF-IDF model and vector search.
- `rag_project.generator`: extractive generation or Ollama generation.
- `rag_project.classifier`: simple metadata extraction for funding applications.
- `rag_project.pipeline`: complete RAG orchestration.
- `rag_project.cli`: terminal interface.
- `rag_project.app`: Streamlit demo app.

## Interview talking points

- RAG reduces hallucinations by forcing the model to use retrieved source material.
- Retrieval and generation are separate, so each part can be improved independently.
- Chunking strongly affects quality: chunks that are too small lose context; chunks that are too large add noise.
- Citations make answers auditable.
- In production, TF-IDF could be replaced with embeddings and a vector database, then extended with evaluation, monitoring and access control.

## Swedish Red Cross interview angle

For the internship interview, the strongest use case is:

Build a RAG-assisted classification system for previous applications, then use the structured database and retrieved source passages to support reporting and new application writing.

See `INTERVIEW_PRESENTATION.md` for a 15-minute presentation outline.

## Suggested interview demo flow

1. Open `notebooks/red_cross_rag_demo.ipynb` and explain the goal in one sentence.
2. Run the notebook cells through the cited answer and classification output.
3. Show the solution map in `INTERVIEW_PRESENTATION.md`.
4. Open the Streamlit app if there is time for an interactive second view.
5. Explain what would change in production: embeddings, vector database, access control, human review and Power BI integration.

## Possible extensions

- Replace TF-IDF with `sentence-transformers`.
- Add a vector database such as FAISS, Chroma or pgvector.
- Add a FastAPI API or Streamlit UI.
- Measure precision@k, recall@k, groundedness and faithfulness.
