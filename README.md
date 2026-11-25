# Capstone 2 - Customer & Knowledge Support Copilot

An AI assistant that helps support agents answer customer questions. It combines
the customer's account data (from a database) with the company's policy documents,
and gives a grounded answer with citations, or decides to clarify, escalate or
send for human review.

Built for the CGI Generative AI Partner Upskill Cohort 9 capstone. All data is synthetic.

## Technology

| Part | Tool |
|---|---|
| Language | Python 3.10 |
| Database | PostgreSQL 16 with pgvector, in Docker |
| Local LLMs and embeddings | Ollama |
| User interface | Streamlit (planned) |

## Setup

Requires: Docker with Docker Compose, Python 3.10+.

1. Copy the settings template and set a password:
```bash
   cp .env.example .env
```
2. Start the database:
```bash
   docker compose up -d
```
3. Create the tables and load the data:
```bash
   docker exec -i capstone2-db psql -U copilot -d support_copilot < docs/course_brief/Capstone2_Customer_Knowledge_Support_Dataset_v2/schema_ddl.sql
   docker exec -i capstone2-db psql -U copilot -d support_copilot < docs/course_brief/Capstone2_Customer_Knowledge_Support_Dataset_v2/document_registry_ddl.sql
   ./scripts/load_data.sh
```
4. Set up Python:
```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
```
5. Check the data loaded correctly:
```bash
   python scripts/verify_data.py
```
   Expected result: `ALL CHECKS PASSED`.

## Project structure

| Path | Contents |
|---|---|
| `docs/course_brief/` | Course brief, use case, dataset, policy documents and golden test set |
| `scripts/` | Data loading and checking scripts |
| `docker-compose.yml` | Database container |
| `requirements.txt` | Python packages (pinned versions) |

## Progress

- [x] Step 1: Database set up and structured data loaded
- [x] Step 2: Statement of Work and project plan
- [ ] Step 3: Document ingestion and chunking
- [ ] Step 4: Embeddings and hybrid search
- [ ] Step 5: Reranking and retrieval evaluation
- [ ] Step 6: Customer lookup and PII masking
- [ ] Step 7: Grounded answers with citations and decision states
- [ ] Step 8: Prompt-injection handling and TokenOps
- [ ] Step 9: Evaluation harness (2+ LLMs)
- [ ] Step 10: Streamlit app
