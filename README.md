# Witness

> **An Event-Driven Workflow Engine demonstrating Event Sourcing, CQRS, Saga Pattern, Outbox Pattern, Kafka, and Projections.**

Witness is a production-inspired backend system that demonstrates how modern distributed applications maintain consistency, auditability, and scalability using event-driven architecture.

Although the demo domain is **loan processing**, the architecture is designed to be reusable for AI systems, fintech platforms, workflow engines, and enterprise applications.

---

## Architecture

```
                   Client
                      │
                FastAPI REST API
                      │
              Command Handlers
                      │
               Event Repository
                      │
      ┌───────────────┴───────────────┐
      │                               │
      ▼                               ▼
 Event Store                     Outbox Table
(PostgreSQL)                         │
      │                              │
      │                        Outbox Worker
      │                              │
      │                          Apache Kafka
      │                              │
      ▼                              ▼
Projection Worker              Future Consumers
      │
      ▼
CQRS Read Models
```

---

# Features

- Event Sourcing
- CQRS (Command Query Responsibility Segregation)
- Saga Pattern
- Transactional Outbox Pattern
- Kafka Event Publishing
- Projection Workers
- Projection Rebuilding
- Snapshot Support
- Event Replay
- Immutable Audit Log
- Dockerized Microservices
- REST API with FastAPI
- PostgreSQL Event Store

---

# Tech Stack

| Layer | Technology |
|--------|------------|
| Backend | Python |
| API | FastAPI |
| Database | PostgreSQL |
| Messaging | Apache Kafka |
| ORM | SQLAlchemy |
| Containers | Docker & Docker Compose |

---

# Event Flow

Every loan application is represented as a stream of immutable events.

```
LoanApplied
      │
      ▼
CreditScoreFetched
      │
      ▼
IncomeVerified
      │
      ▼
RiskCalculated
      │
      ▼
LoanApproved / LoanRejected
```

The current state is **never directly updated**.

Instead, it is rebuilt from the sequence of events.

---

# CQRS Read Model

The read model is maintained asynchronously by a Projection Worker.

```
Events
   │
   ▼
Projection Worker
   │
   ▼
loan_projection
```

This allows:

- Fast queries
- Event replay
- Read model rebuilding
- Historical auditing

---

# Saga Pattern

The system uses a Saga Worker to coordinate long-running workflows.

Example:

```
Loan Applied
      │
      ▼
Fetch Credit Score
      │
      ▼
Verify Income
      │
      ▼
Calculate Risk
      │
      ▼
Approve / Reject Loan
```

Each step is persisted as an event.

---

# Outbox Pattern

Events are written to both:

- Event Store
- Outbox Table

within the same database transaction.

The Outbox Worker then publishes events to Kafka, guaranteeing reliable event delivery.

```
Database Transaction
        │
        ├── Event Store
        └── Outbox

               │
               ▼

       Outbox Worker

               │
               ▼

            Kafka
```

---

# Project Structure

```
.
├── app.py
├── database.py
├── schema.sql
├── docker-compose.yml
│
├── repositories/
│   ├── event_repository.py
│   ├── outbox_repository.py
│   ├── projection_repository.py
│   └── snapshot_repository.py
│
├── services/
│   ├── loan_service.py
│   ├── decision_service.py
│   ├── projection_service.py
│   └── snapshot_service.py
│
├── workers/
│   ├── projection_worker.py
│   ├── outbox_worker.py
│   └── saga_worker.py
│
└── models/
```

---

# Running the Project

Clone the repository


Move into the project

```bash
cd witness
```

Start all services

```bash
docker compose up --build
```

API

```
http://localhost:8000/docs
```

---

# Why Event Sourcing?

Traditional systems overwrite state.

```
Status = Approved
```

Previous states disappear.

Witness stores every business event forever.

```
LoanApplied

↓

CreditScoreFetched

↓

IncomeVerified

↓

RiskCalculated

↓

LoanApproved
```

This enables:

- Complete audit history
- Event replay
- Time travel debugging
- Projection rebuilding
- Regulatory compliance

---

# Future Roadmap

- Kafka Consumers
- Dead Letter Queue (DLQ)
- Retry Policies
- OpenTelemetry Integration
- Event Versioning
- Multi-Tenant Support
- AI Workflow Execution Engine
- AI Agent Observability
- Policy Verification Layer (CAEV)
- Cognitive Anti-Fragility Firewall (CAFF)

---

# Inspiration

Witness is inspired by architectural patterns used in modern distributed systems including:

- Event Sourcing
- CQRS
- Domain-Driven Design
- Saga Pattern
- Transactional Outbox Pattern
- Event-Driven Microservices

---

# Author

**Himanshu Mishra**

Building distributed systems and AI infrastructure.

```
"Every decision tells a story.
Witness makes sure that story is never lost."
```