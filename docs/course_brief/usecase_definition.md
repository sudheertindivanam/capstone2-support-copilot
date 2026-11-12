# Capstone 2 — Enterprise Customer & Knowledge Support Copilot
## Use Case Definition

## Purpose

This capstone combines **structured customer/support data** with **unstructured enterprise knowledge documents** to build a grounded Customer & Knowledge Support Copilot.

The solution should be able to answer two types of questions together:

1. **What does the company policy / knowledge base say?**
2. **What is true for this specific customer, account, product, entitlement, or ticket?**

A strong implementation should not treat the documents and the relational data as two unrelated sources. The application should combine them at runtime so that responses are both **policy-grounded** and **customer-specific**.

---

# 1. Structured Data Tables

The structured dataset contains operational customer-support information. These tables provide facts that should not be invented by the LLM.

## 1.1 `customers`

### What it contains
Customer-level master data such as customer identifiers, names, segment, geography, contact or classification attributes, and customer status.

### Function
This table represents **who the customer is**.

It is the starting point for customer-specific support context and can be used to answer questions such as:

- Who is this customer?
- What segment does the customer belong to?
- What region or market applies to the customer?
- Is the customer active?
- Should PII be masked for the current user?

### Typical AI use
The assistant can retrieve the customer record after a customer/account identifier is supplied, then use those attributes to filter or personalize the knowledge retrieved from documents.

---

## 1.2 `accounts`

### What it contains
Account-level information associated with customers. One customer may have one or more accounts.

Typical fields include account identifier, customer relationship, support tier, account status, region, service level, and other account-specific attributes.

### Function
This table represents **the commercial or service account under which support is delivered**.

It provides context that is often more specific than the customer master record.

### Typical AI use
The assistant can use account data to determine:

- support tier
- account status
- applicable SLA or escalation path
- which product/service relationship is being discussed
- whether a customer-specific entitlement exists

---

## 1.3 `products`

### What it contains
Product or service reference data such as product identifier, product name, family, category, service type, and product status.

### Function
This table defines **what product or service the support request relates to**.

### Typical AI use
The product record can be used to:

- classify the issue by product
- filter the knowledge base to the right product documentation
- distinguish policies that apply to one product but not another
- improve retrieval precision by adding product metadata to the RAG query

---

## 1.4 `entitlements`

### What it contains
Customer/account access or support entitlements for products and services.

Typical examples include active subscriptions, support eligibility, service level, start/end dates, feature access, or product-plan relationships.

### Function
This table answers **what the customer is entitled to receive or use**.

It is important because support decisions should not be based only on policy text; they may depend on whether the customer actually has the relevant product, plan, service level, or active entitlement.

### Typical AI use
The assistant can combine entitlement data with policy content to answer questions such as:

- Is the customer eligible for this support action?
- Is the requested product active for this account?
- Does the customer's plan allow this service?
- Should the request be escalated because the entitlement is missing or expired?

---

## 1.5 `support_agents`

### What it contains
Reference information about support personnel such as agent identifier, team, support queue, role, location, specialization, or skill group.

### Function
This table represents **who handles support work**.

### Typical AI use
It can be used to:

- route or recommend the correct support team
- identify the assigned agent or queue
- support escalation logic
- simulate role-based access or PII visibility

This is especially useful if the capstone includes a supervisor, routing, or escalation view.

---

## 1.6 `support_tickets`

### What it contains
The main support-case or ticket record.

Typical fields include ticket identifier, customer/account, product, issue category, priority, status, assigned agent, summary, timestamps, and resolution-related attributes.

### Function
This table represents **the current or historical support case**.

It is the primary operational table for understanding the support request in context.

### Typical AI use
The assistant can use ticket history to:

- summarize the current issue
- identify previous similar tickets
- understand customer history
- determine if the issue is recurring
- supply ticket context to the LLM before generating a response

Historical tickets can also be used as an additional retrieval source, although they should be treated differently from authoritative policy documents.

---

## 1.7 `ticket_events`

### What it contains
Time-ordered events associated with support tickets.

Examples may include ticket creation, assignment, status change, escalation, customer reply, internal note, resolution, reopening, or closure.

### Function
This table provides **the lifecycle and chronology of a support case**.

While `support_tickets` represents the current ticket state, `ticket_events` explains **how the ticket reached that state**.

### Typical AI use
The assistant can use event history to:

- create a case timeline
- summarize what has already happened
- detect repeated escalation or reopening
- avoid recommending an action already performed
- generate a better handoff summary for another agent

---

## 1.8 `document_registry`

### What it contains
Metadata describing the enterprise knowledge documents supplied with the capstone.

Typical fields may include:

- document identifier
- document name
- document type
- product applicability
- policy category
- current/archived status
- effective date
- version
- region or customer scope
- source file name

### Function
This table acts as the **structured control layer for the unstructured knowledge base**.

It is especially important for retrieval because documents should not be treated as equal. The system should know which document is current, archived, applicable to a product, or relevant to a policy category.

### Typical AI use
The registry can drive metadata filtering before vector search, for example:

- `status = CURRENT`
- `product = requested product`
- `region = customer region`
- `policy_type = REFUND`

This helps prevent the model from retrieving an outdated or inapplicable policy.

---

# 2. Unstructured Knowledge Documents

The document set contains multi-page enterprise support policies, standards, procedures, and operating guides.

The knowledge corpus includes topics such as:

- customer support operating procedures
- refunds, credits, and billing adjustments
- identity verification and account access
- subscription and entitlement support
- service incidents, performance, and SLA handling
- customer privacy and data requests
- archived or superseded policies

These documents are deliberately several pages long and contain multiple sections so that participants must make real decisions about:

- document parsing
- chunk size
- chunk overlap
- section-aware chunking
- metadata enrichment
- document versioning
- current versus archived content
- retrieval precision
- hybrid retrieval
- reranking

---

# 3. How Structured Data and Documents Work Together

The main learning objective is to combine **authoritative business facts** from structured data with **rules, procedures, and guidance** from the knowledge documents.

## Example 1 — Refund Request

### User question
> Can this customer receive a refund for the last charge?

### Structured data provides
- customer identity
- account status
- product/plan
- entitlement status
- ticket details
- potentially previous support history

### Documents provide
- refund policy
- eligibility rules
- limits and exclusions
- required approval path
- current policy version

### Combined response
The system should not simply quote the refund policy. It should evaluate the customer-specific context against the policy and produce a grounded response such as:

> The account is active and the customer has an eligible subscription. Under the current Refunds and Billing Adjustments Policy, the request appears eligible for review because the charge falls within the allowed period. Human approval is required before a refund is issued.

The response should cite the relevant policy section and distinguish policy facts from customer/account facts.

---

## Example 2 — Access / MFA Issue

### User question
> The customer is locked out and cannot complete MFA. What should support do?

### Structured data provides
- customer/account identity
- account status
- product/service relationship
- active entitlement
- current ticket history

### Documents provide
- identity verification standard
- account access procedure
- required verification steps
- escalation rules

### Combined response
The assistant should provide the correct support procedure while using the actual customer/account context to avoid giving generic guidance.

---

## Example 3 — Service Incident / SLA

### User question
> Is this customer eligible for priority escalation because of the outage?

### Structured data provides
- customer support tier
- account information
- product entitlement
- ticket priority/status

### Documents provide
- incident classification rules
- SLA definitions
- escalation policy
- priority handling procedure

### Combined response
The assistant should determine whether the customer's support tier and current issue meet the documented escalation criteria.

---

# 4. Recommended Runtime Pattern

A good runtime design is:

```text
User / Support Agent Question
        |
        v
Identify Customer / Account / Ticket / Product
        |
        +-------------------------+
        |                         |
        v                         v
Structured Data Lookup      Knowledge Retrieval
(Customer, account,         (Policies, guides,
entitlement, tickets)       standards, procedures)
        |                         |
        +------------+------------+
                     |
                     v
              Context Builder
                     |
                     v
             LLM Response Generation
                     |
                     v
       Grounded Answer + Evidence + Decision
```

The application should preserve the distinction between the two context types:

### Structured facts
Examples:
- customer is Enterprise tier
- account is active
- entitlement expires on a given date
- ticket is currently escalated

### Document-grounded rules
Examples:
- refund eligibility window
- identity verification requirements
- escalation criteria
- privacy handling requirements

The model should not invent either type.

---

# 5. Recommended Retrieval Strategy

The solution can use two retrieval paths.

## Structured retrieval
Use SQL or an application/API layer to retrieve exact customer, account, entitlement, product, ticket, and event data.

This is appropriate when the answer requires exact facts.

## Unstructured retrieval
Use embeddings/vector search, keyword search, or hybrid retrieval over document chunks.

The retrieval query should include useful metadata from the structured context where appropriate.

For example:

```text
Question: "Can this customer receive a refund?"
Customer Segment: Enterprise
Product: Premium Support
Region: North America
Policy Type: Refund
Document Status: Current
```

This context can improve metadata filtering and retrieval precision.

---

# 6. Important Design Principle

Do **not** place all relational data into the vector store and treat it as text.

Structured operational facts should normally remain in the relational database and be retrieved through SQL or APIs.

The vector store should primarily hold:

- policy chunks
- knowledge articles
- procedure sections
- approved document metadata
- optionally historical support-resolution summaries if the team explicitly distinguishes them from authoritative policy content

This separation helps preserve:

- accuracy
- freshness
- governance
- explainability
- access control

---

# 7. Example Context Assembly

For a single support request, the context sent to the LLM might look like:

```text
CUSTOMER CONTEXT
Customer: Example Customer
Segment: Enterprise
Account Status: Active
Support Tier: Premium
Product: Support Cloud Pro
Entitlement: Active

TICKET CONTEXT
Ticket: TKT-10492
Issue: Billing adjustment request
Priority: Medium
Status: Open

RETRIEVED POLICY CONTEXT
Document: Refunds, Credits and Billing Adjustments Policy
Version: Current
Section: Refund Eligibility
Relevant rule: ...

DECISION INSTRUCTION
Use the customer/account facts together with the retrieved policy.
Do not infer eligibility if evidence is missing.
Return one of:
RESPOND / CLARIFY / ESCALATE / HUMAN_APPROVAL / NO_EVIDENCE
```

This is a stronger enterprise pattern than simply sending document chunks to the model.

---

# 8. What Participants Should Learn

By using both data types together, participants should demonstrate that they understand:

- RAG is primarily for retrieving unstructured knowledge
- SQL/APIs are appropriate for exact operational facts
- customer-specific answers often require both sources
- metadata filtering improves document retrieval
- document status/version matters
- archived policies must not override current policy
- structured facts and policy evidence should remain traceable
- PII and role-based access must be considered before context is sent to the LLM
- evaluation should test both retrieval quality and customer-specific answer correctness

---

# 9. Golden Questions / Responses

The package includes a developer aid with golden questions and expected responses.

These can be used to:

- verify structured-data lookup
- verify correct policy retrieval
- test current-vs-archived filtering
- validate decision states
- compare chunking/retrieval strategies
- perform regression testing after model, embedding, or prompt changes

Participants should treat the golden set as an **evaluation asset**, not as few-shot content to blindly inject into every request.

---

# 10. Target Outcome

The final application should behave like an enterprise support copilot that can answer:

> **What is true for this customer?**

using structured data, and:

> **What should support do according to current company policy?**

using grounded enterprise knowledge.

The strongest implementation will combine both sources into a response that is **specific, grounded, explainable, governed, and safe**.
