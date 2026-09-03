from __future__ import annotations

import unittest

from rag_project.chunking import chunk_text
from rag_project.classifier import classify_application
from rag_project.pipeline import RagPipeline
from rag_project.retriever import TfidfRetriever


class ChunkingTest(unittest.TestCase):
    def test_chunk_text_uses_overlap(self) -> None:
        text = " ".join(f"word{i}" for i in range(10))
        chunks = chunk_text("doc.md", text, chunk_size=5, overlap=2)

        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0].start_word, 0)
        self.assertEqual(chunks[1].start_word, 3)


class RetrieverTest(unittest.TestCase):
    def test_retriever_returns_relevant_chunk(self) -> None:
        chunks = [
            *chunk_text("rag.md", "RAG uses retrieval and generation with citations.", 20, 0),
            *chunk_text("other.md", "SQL databases store relational tables.", 20, 0),
        ]
        retriever = TfidfRetriever().fit(chunks)

        results = retriever.retrieve("retrieval generation", top_k=1)

        self.assertEqual(results[0].chunk.source, "rag.md")


class PipelineTest(unittest.TestCase):
    def test_pipeline_answers_from_sample_docs(self) -> None:
        pipeline = RagPipeline.from_documents("data/knowledge_base")

        answer = pipeline.ask("What are the advantages of RAG?", top_k=2)

        self.assertIn("Answer based", answer.answer)
        self.assertTrue(answer.citations)

    def test_answer_excerpt_changes_with_question(self) -> None:
        pipeline = RagPipeline.from_documents("data/red_cross_examples")

        classification_answer = pipeline.ask(
            "What fields should be extracted from previous funding applications?",
            top_k=2,
        )
        reporting_answer = pipeline.ask(
            "How can retrieved application data support report drafting?",
            top_k=2,
        )

        self.assertNotEqual(classification_answer.answer, reporting_answer.answer)
        self.assertIn("metadata", classification_answer.answer)
        self.assertIn("draft", reporting_answer.answer)


class ClassifierTest(unittest.TestCase):
    def test_classifies_synthetic_application(self) -> None:
        text = (
            "Program area: disaster preparedness.\n"
            "Country: Sweden.\n"
            "Target group: volunteers.\n"
            "Donor type: institutional donor.\n"
            "Expected outcomes: faster response, better reporting.\n"
            "The document mentions indicators related to trained volunteers and response time."
        )

        result = classify_application(text)

        self.assertEqual(result.program_area, "disaster preparedness")
        self.assertEqual(result.geography, "Sweden")
        self.assertIn("faster response", result.outcomes)
        self.assertIn("trained volunteers", result.indicators)


if __name__ == "__main__":
    unittest.main()
