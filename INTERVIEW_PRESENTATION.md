# 15-minute internship presentation

Audience: Swedish Red Cross, AI Strategist and Power BI / Data Platform Product Owner.

## Slide 1 - Introduction

Hi, my name is Osman Camara. I am studying Python development with a focus on AI and machine learning. I am especially interested in practical AI systems that help people work faster, make better decisions and keep knowledge reusable.

I have worked with Python, data processing, backend logic and AI assistant-style workflows. For this internship, I would like to combine technical delivery with learning how AI can be used responsibly in a humanitarian organization.

## Slide 2 - My goals for the internship

My goals are:

- Learn how AI and data platforms are used in a real organization.
- Build useful prototypes that solve concrete workflow problems.
- Improve my skills in RAG, document processing, evaluation and responsible AI.
- Understand how to connect AI solutions with reporting, data governance and Power BI workflows.

## Slide 3 - Expected outcomes after 6 months

By the end of the internship, I would aim to deliver:

- A working proof of concept for one selected AI/RAG use case.
- A documented data pipeline from documents to searchable structured information.
- A small evaluation framework to measure retrieval and answer quality.
- Clear documentation so the team can continue development after the internship.
- A final demo showing value, limitations and next steps.

## Slide 4 - Use case idea 1: Application classification database

Problem:
Previous applications contain valuable information, but they may be hard to search, compare and reuse when writing new applications and reports.

Idea:
Build a RAG-assisted classification pipeline that extracts metadata from previous applications and makes them searchable by topic, donor, country, program area, target group, outcomes, budget type and reporting requirements.

Potential value:

- Faster discovery of relevant past applications.
- More consistent classification.
- Better reuse of previous text and evidence.
- Stronger support for report writing and new funding applications.

## Slide 5 - Use case idea 2: Report drafting assistant

Problem:
Writing reports often requires finding previous commitments, activities, outcomes, indicators and narrative evidence across many documents.

Idea:
Build an assistant that retrieves relevant source passages, proposes a draft section and always shows citations. The assistant should not replace human review; it should reduce search and first-draft time.

Potential value:

- Faster report preparation.
- Better traceability from report text to source material.
- Less manual copy/paste work.
- Easier knowledge sharing across teams.

## Slide 6 - Selected use case

I would select use case 1: RAG-assisted classification of previous applications.

Reason:
It creates a foundation for several later use cases. Once previous applications are classified and searchable, the organization can use the same database for reporting, new applications, internal analysis and Power BI dashboards.

## Slide 7 - Solution map

High-level flow:

1. Collect previous applications and related documents.
2. Convert documents into text.
3. Split text into chunks with metadata.
4. Extract structured fields using rules and AI.
5. Store metadata in a database.
6. Store document chunks in a retrieval index.
7. Build a search/RAG interface for staff.
8. Connect structured outputs to Power BI for analysis.

## Slide 8 - Proposed architecture

Components:

- Document ingestion: PDF, Word and text files.
- Preprocessing: OCR if needed, cleaning, language detection and deduplication.
- Chunking: split long documents into meaningful sections.
- Classification: program area, location, donor, year, sector, SDG, target group and application status.
- Retrieval: embeddings or lexical search to find relevant source passages.
- Generation: answer questions or draft text using only retrieved sources.
- Human review: staff validate classifications and generated text.
- Analytics: Power BI dashboards over the structured database.

## Slide 9 - Evaluation and responsible AI

I would evaluate:

- Retrieval quality: does the system find the right documents and passages?
- Classification accuracy: are labels correct compared with human review?
- Groundedness: are generated answers supported by sources?
- Usability: does the workflow save time for staff?

Responsible AI controls:

- Citations for every generated answer.
- Human approval before using generated report text.
- Access control for sensitive documents.
- Clear handling of uncertain answers.
- Logging and monitoring for errors.

## Slide 10 - 6-month internship roadmap

Month 1:
Understand users, documents, data policies and success criteria.

Month 2:
Build ingestion and preprocessing prototype.

Month 3:
Build first retrieval and classification pipeline.

Month 4:
Add evaluation, human review flow and improve accuracy.

Month 5:
Prototype reporting/search assistant and Power BI-ready outputs.

Month 6:
Polish demo, document the system, present findings and recommend next steps.

## Slide 11 - Demo project

I prepared a small local RAG project to show how I think about the problem:

- Load documents.
- Split them into chunks.
- Retrieve relevant passages.
- Generate an answer with citations.
- Keep the system explainable and testable.

This is intentionally simple, but the same architecture can be upgraded with embeddings, a vector database, access control and a production data platform.

## Slide 12 - Questions for Swedish Red Cross

- What types of applications and reports are most important to start with?
- Are the documents mostly PDF, Word or stored in another system?
- What metadata is already available today?
- What would make a prototype genuinely useful for the team?
- What data governance or confidentiality rules should shape the design?

