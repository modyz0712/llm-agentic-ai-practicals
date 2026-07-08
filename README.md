# LLM and Agentic AI Practicals

Practical LangChain work for structured extraction, support-ticket routing, and retrieval-augmented question answering.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Runnable%20Chains-1C3C3C?style=flat-square)
![OpenAI](https://img.shields.io/badge/OpenAI-gpt--4o--mini-412991?style=flat-square&logo=openai&logoColor=white)
![Chroma](https://img.shields.io/badge/Vector%20Store-Chroma-5B4B8A?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## Overview

This repository is a curated public copy of hands-on LLM and agentic AI practical work. It focuses on small, explainable workflows that demonstrate how to build useful LLM applications with structured outputs, validation logic, retrieval, metadata filtering, and grounded response generation.

The repo intentionally avoids raw assignment packaging. Old drafts, generated vector databases, rubric files, teammate/reference notebooks, and private school-only materials are excluded so the public version stays clean and portfolio-ready.

## What This Shows

- Structured data extraction from messy customer-support messages.
- Runnable chain composition with LangChain Expression Language.
- Missing-field validation and conditional routing.
- PDF ingestion with hierarchical parsing and chunk metadata.
- Chroma-based retrieval with section and subsection filtering.
- Query transformation, scope guardrails, context compression, and grounded answer generation.
- Notebook-based RAG assistant workflow that can be rerun with an OpenAI API key.

## Repository Structure

```text
.
├── assignment1/
│   ├── structured_extraction_chain.py
│   └── support_ticket_router.py
├── documents/
│   └── attendance_policy_source.pdf
├── notebooks/
│   └── attendance_policy_rag_assistant.ipynb
├── requirements.txt
├── LICENSE
└── README.md
```

## Practical Work

### 1. Structured Extraction Chain

`assignment1/structured_extraction_chain.py` builds a LangChain runnable that extracts customer-support fields into a consistent JSON schema. It handles names, product details, serial numbers, issue labels, issue descriptions, and user inquiries from free-form text.

### 2. Support Ticket Router

`assignment1/support_ticket_router.py` extends the extraction chain with validation and routing. If one required field is missing, it returns a short clarification message. If multiple fields are missing, it uses the model to generate a polite follow-up. If the ticket is complete, it routes the case to a normal support-response chain.

### 3. Attendance Policy RAG Assistant

`notebooks/attendance_policy_rag_assistant.ipynb` demonstrates a RAG assistant over a PDF policy document. The workflow includes:

- loading and parsing a PDF source document,
- cleaning repeated headers and table-of-contents noise,
- preserving numbered-list content during chunking,
- enriching chunks with section and subsection metadata,
- indexing chunks with Chroma,
- compiling conversational queries into standalone retrieval queries,
- rejecting out-of-scope queries before retrieval,
- routing queries to relevant document sections and subsections,
- packing evidence with provenance labels, and
- generating grounded answers with source references.

## Setup

Install the dependencies in a Python environment:

```bash
pip install -r requirements.txt
```

Set your OpenAI API key before running the examples:

```bash
set OPENAI_API_KEY=your_api_key
```

For Google Colab, the notebook is prepared to read the key from Colab userdata. For local Jupyter use, adjust the setup cell to read from your environment.

## Running The Examples

The Python chain files expose reusable LangChain runnables:

```python
from assignment1.structured_extraction_chain import extraction_chain

result = extraction_chain.invoke(
    "Hi, I am Alex. My iPhone 13 serial number is SN12345. The screen flickers after charging."
)
print(result)
```

The RAG notebook can be opened in Jupyter or Colab. The source PDF is included under `documents/`, while generated Chroma index folders are intentionally not committed because they can be rebuilt from the notebook.

## Notes

- This is a portfolio-oriented public version of practical LLM work.
- API keys, generated vector stores, zipped submissions, grading documents, and unrelated reference notebooks are excluded.
- Some notebook outputs come from an interactive Colab workflow; rerun the notebook after setting an API key to reproduce fresh outputs.

## License

This project is released under the MIT License.
