from __future__ import annotations

from pathlib import Path

from rag_project.classifier import classify_application
from rag_project.loaders import load_markdown_documents
from rag_project.pipeline import RagPipeline


DEFAULT_DOCS = Path(__file__).resolve().parents[2] / "data" / "red_cross_examples"


def main() -> None:
    import streamlit as st

    st.set_page_config(page_title="RAG Application Classifier", layout="wide")
    st.title("RAG Application Classifier")
    st.caption("Prototype for classifying previous applications and reusing knowledge with citations.")
    st.info("This demo uses synthetic data and is not connected to real Swedish Red Cross applications.")

    docs_path = st.sidebar.text_input("Document folder", value=str(DEFAULT_DOCS))
    top_k = st.sidebar.slider("Retrieved chunks", min_value=1, max_value=6, value=3)
    question = st.text_input(
        "Question",
        value="How can previous funding applications be classified for reporting and new proposals?",
    )

    left, right = st.columns([1, 1])

    try:
        pipeline = RagPipeline.from_documents(docs_path)
        documents = load_markdown_documents(docs_path)
    except Exception as exc:
        st.error(f"Could not load documents: {exc}")
        return

    with left:
        st.subheader("RAG answer")
        if st.button("Ask", type="primary"):
            answer = pipeline.ask(question, top_k=top_k)
            st.write(answer.answer)
            if answer.citations:
                st.subheader("Sources")
                for citation in answer.citations:
                    st.code(citation)

    with right:
        st.subheader("Application classification")
        selected_source = st.selectbox("Document", [document.source for document in documents])
        selected = next(document for document in documents if document.source == selected_source)
        classification = classify_application(selected.text)

        st.metric("Confidence", f"{classification.confidence:.0%}")
        st.write(
            {
                "program_area": classification.program_area,
                "geography": classification.geography,
                "donor_type": classification.donor_type,
                "target_group": classification.target_group,
                "outcomes": classification.outcomes,
                "indicators": classification.indicators,
            }
        )


if __name__ == "__main__":
    main()
