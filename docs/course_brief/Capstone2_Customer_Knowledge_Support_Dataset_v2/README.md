# Capstone 2 - Enterprise Customer & Knowledge Support Copilot Dataset (v2)

This package combines multi-page unstructured knowledge with structured customer/account/support data. It is designed to create meaningful work in chunking, hybrid retrieval, metadata filtering, structured-context fusion, evaluation, security and TokenOps.

## Knowledge documents
Seven documents are supplied in mixed formats. Current documents are 5 pages each; the archived policy is 4 pages.

- 01 Customer Support Operating Manual - DOCX
- 02 Refunds, Credits and Billing Adjustments Policy - PDF
- 03 Identity Verification and Account Access Standard - DOCX
- 04 Subscription, Entitlement and Product Support Guide - PDF
- 05 Service Incident and Performance SLA Runbook - DOCX
- 06 Customer Privacy and Data Request Procedure - PDF
- 99 ARCHIVED Refund and Service Credit Policy - DOCX

The current and archived billing policies deliberately conflict. Participants should use document metadata/status filtering and answer historical questions carefully.

## Structured data
The package includes the original Capstone 2 structured dataset:
- customers
- accounts
- products
- entitlements
- support_agents
- support_tickets
- ticket_events
- document_registry

Use `schema_ddl.sql` to create the relational database. Use `document_registry_ddl.sql` if you also want the document registry in the database; otherwise `document_registry.csv` can be consumed directly by the ingestion pipeline as metadata.

## Suggested chunking experiment
Participants should compare at least two chunking strategies, for example:
1. fixed/recursive chunks with overlap
2. structure-aware chunks based on headings/sections

Evaluate retrieval against the golden questions. Preserve metadata such as document_id, title, policy_id, version, status, section heading, product scope and region scope.

## Retrieval expectations
A good implementation should support:
- current-vs-archived filtering
- product/region metadata filters
- semantic retrieval
- keyword/hybrid retrieval for exact policy IDs and terms
- reranking
- separate structured customer/account lookup
- fusion of structured context with knowledge evidence

## Golden developer aid
`developer_aid/golden_questions_responses.csv` contains 20 question/response cases, expected decision states, evidence sources and developer notes. It is intended for evaluation and development support, not as the only test set.

## Security / PII
Customer names and email addresses in the synthetic CSV data should be treated as PII for the exercise. Do not put all customer PII into the vector store. Use structured lookup and demonstrate role-based masking or omission.

## Recommended decision states
- RESPOND
- CLARIFY
- ESCALATE
- HUMAN_APPROVAL
- NO_EVIDENCE
