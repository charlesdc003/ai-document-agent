# AI Document Intelligence Agent

An AI agent that processes PDF documents, extracts key information, generates summaries, flags risks and deadlines, and logs structured results to Airtable automatically.

---

## What It Does

1. **Ingests any PDF document** — contracts, invoices, reports, proposals
2. **Extracts text** using PyMuPDF
3. **Analyzes the document** using a local LLM (llama3.2 via Ollama) to produce:
   - Document type classification
   - 2-3 sentence summary
   - Key facts, dates, amounts, and named parties
   - Flags for risks, deadlines, missing information, or unusual clauses
4. **Logs structured results to Airtable** for review and record keeping

---

## Architecture
PDF document (input)
↓
PyMuPDF (text extraction)
↓
Ollama / llama3.2 (document analysis + structured output)
↓
JSON parser with retry logic (handles LLM output variability)
↓
Airtable API (log document name, type, summary, key info, flags, timestamp)

---

## Sample Output
Processing: test_contract.pdf
Extracting text...
Extracted 1443 characters
Analyzing document...
Document Type: contract
Summary:
Service Agreement for AI-powered customer support automation system
Key Information:
Project start date: April 1, 2026, Total contract value: $18,000 USD,
Payment schedule with 1.5% monthly interest charge if late
Flags:
Signed agreement is overdue (March 15, 2026)
Logging to Airtable...
Successfully logged to Airtable
Done.

---

## Airtable Output

Every processed document is logged with:

| Field | Description |
|---|---|
| Document Name | Original filename |
| Document Type | Contract, invoice, report, etc. |
| Summary | 2-3 sentence overview |
| Key Information | Dates, amounts, parties, terms |
| Flags | Risks, deadlines, missing items |
| Timestamp | Date processed |

---

## Tech Stack

| Component | Tool | Production Equivalent |
|---|---|---|
| LLM | Ollama / llama3.2 | OpenAI API / Azure OpenAI |
| PDF Parsing | PyMuPDF | Same / Apache Tika |
| Logging | Airtable API | PostgreSQL / Salesforce |
| Auth | Airtable Personal Access Token | OAuth2 / Service accounts |

---

## Setup

1. Clone the repo
2. Install dependencies:
```bash
pip install pymupdf pyairtable python-dotenv ollama requests
```
3. Create a `.env` file:
AIRTABLE_API_KEY=your_token_here
AIRTABLE_BASE_ID=your_base_id_here
4. Make sure Ollama is running with llama3.2 pulled:
```bash
ollama pull llama3.2
```
5. Run against any PDF:
```bash
python3 agent.py your_document.pdf
```

---

## What I'd Do Next In Production

- Add support for Word documents and plain text files
- Build a Flask API so documents can be uploaded via HTTP
- Add a Make.com trigger to auto-process documents emailed to an inbox
- Implement multi-document batch processing
- Add confidence scoring on extracted fields
- Connect to Google Drive or Dropbox for automatic document ingestion
- Build a review UI for flagged documents requiring human attention

---

## Author

Charles Cox | Charles Cox Consulting https://github.com/charlesdc003

Built as a portfolio project demonstrating PDF processing, unstructured data extraction, LLM-based document analysis, structured output generation, and Airtable integration.
