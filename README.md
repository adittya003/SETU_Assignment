# Payment Event Processing & Reconciliation API

A Flask-based REST API that processes payment lifecycle events from merchants while ensuring **idempotency**, **state validation**, **merchant validation**, and **transaction reconciliation**.

The application simulates a real-world payment processing system where asynchronous payment events are received, validated, persisted, and reconciled.

---

# Tech Stack

* **Python 3**
* **Flask**
* **SQLAlchemy**
* **PostgreSQL**
* **Flask Blueprints**
* **REST APIs**

---

# Features

* Process payment lifecycle events
* Merchant validation
* Payload validation
* Idempotent event processing
* Transaction state management
* Reconciliation tracking
* Duplicate event detection
* Layered service architecture
* Centralized exception handling
* Atomic database transactions

---

# Payment Lifecycle

The application supports the following payment lifecycle:

```text
payment_initiated
        │
        ▼
payment_processed
        │
        ▼
      settled
```

Valid transitions are tracked normally.

Any invalid or out-of-order transition is automatically marked as a **DISCREPANCY** for reconciliation instead of rejecting the request.

---

# Project Structure

```text
.
├── app.py
├── config.py
├── models/
│   ├── merchant.py
│   ├── transaction.py
│   └── payment_event.py
│
├── routes/
│   ├── event_routes.py
│   └── reconciliation_routes.py
│
├── services/
│   ├── event_processing_service.py
│   ├── merchant_service.py
│   ├── transaction_service.py
│   ├── payment_event_service.py
│   └── reconciliation_service.py
│
├── validators/
│   └── payload_validator.py
│
├── enums/
│   ├── event_type.py
│   ├── transaction_status.py
│   └── reconciliation_status.py
│
├── exceptions/
│   ├── duplicate_event_exception.py
│   ├── invalid_payload_exception.py
│   ├── merchant_not_found_exception.py
│   └── handlers.py
│
├── seed/
│   ├── merchant.json
│   ├── merchant_name_extraction.py
│   └── seed_merchant.py
│
└── README.md
```

---

# Architecture

```text
                Client
                   │
                   ▼
             Flask Routes
                   │
                   ▼
      EventProcessingService
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
MerchantService TransactionService PaymentEventService
                   │
                   ▼
       ReconciliationService
                   │
                   ▼
             PostgreSQL
```

### Responsibilities

**Routes**

* Handle HTTP requests and responses.
* Delegate business logic to services.

**EventProcessingService**

* Orchestrates the complete payment workflow.
* Validates merchants.
* Checks idempotency.
* Performs state transitions.
* Creates payment events.
* Commits database transactions.

**Other Services**

Responsible for database operations related to a single entity.

---

# Database Schema

## Merchant

| Column        | Description         |
| ------------- | ------------------- |
| id            | Primary Key         |
| merchant_id   | Merchant Identifier |
| merchant_name | Merchant Name       |

---

## Transaction

| Column                | Description           |
| --------------------- | --------------------- |
| id                    | Primary Key           |
| transaction_id        | Business UUID         |
| merchant_id           | Foreign Key           |
| amount                | Payment Amount        |
| currency              | Currency              |
| status                | Transaction Status    |
| reconciliation_status | Reconciliation Status |

---

## Payment Event

| Column          | Description        |
| --------------- | ------------------ |
| id              | Primary Key        |
| event_id        | Event UUID         |
| transaction_id  | Foreign Key        |
| event_type      | Payment Event Type |
| event_timestamp | Event Timestamp    |

---

# Transaction State Machine

Valid transitions:

```text
INITIATED
    │
    ▼
PROCESSED
    │
    ▼
SETTLED
```

Examples:

| Transition            | Result        |
| --------------------- | ------------- |
| INITIATED → PROCESSED | ✅ Valid       |
| PROCESSED → SETTLED   | ✅ Valid       |
| INITIATED → SETTLED   | ❌ DISCREPANCY |
| FAILED → SETTLED      | ❌ DISCREPANCY |
| First Event = SETTLED | ❌ DISCREPANCY |

---

# Merchant Seeding

The application requires merchants to exist before payment events can be processed.

Instead of manually inserting merchants into the database, merchant information is automatically extracted from the provided sample payloads.

## Step 1: Extract Merchants

The script:

```text
seed/merchant_name_extraction.py
```

reads the provided `sample_payload.json`, extracts all unique merchant IDs and merchant names, and generates:

```text
seed/merchant.json
```

This ensures that the merchant data used during testing is always consistent with the sample payloads.

## Step 2: Seed Database

The script:

```text
seed/seed_merchant.py
```

reads the generated `merchant.json` file and inserts all merchants into the PostgreSQL database.

Run:

```bash
python seed/seed_merchant.py
```

before testing the APIs.

This only needs to be executed once (or whenever the merchant table is recreated).

---

# Validation

## Payload Validation

The application validates:

* Required fields
* UUID format
* Event type
* Positive payment amount
* Merchant ID
* Merchant name
* Currency
* Timestamp format

Invalid requests return **HTTP 400**.

---

## Merchant Validation

Every request validates both:

* Merchant ID
* Merchant Name

The merchant name must match the merchant ID stored in the database.

This prevents inconsistent merchant information from being processed.

---

# Idempotency

Every payment event contains a unique `event_id`.

Before processing an event, the application checks whether the event has already been processed.

If the event already exists, the request is ignored to ensure duplicate payment events are never processed twice.

---

# Reconciliation

Every transaction maintains a reconciliation status.

Possible values:

| Status      | Description                          |
| ----------- | ------------------------------------ |
| MATCHED     | Valid payment lifecycle              |
| PENDING     | Waiting for additional events        |
| DISCREPANCY | Invalid or unexpected event sequence |

---

# API Endpoints

## Process Payment Event

```http
POST /events
```

Processes an incoming payment event.

---

## Get All Transactions

```http
GET /transactions
```

Returns all processed transactions.

---

## Get Transaction

```http
GET /transactions/{transaction_id}
```

Returns details for a specific transaction.

---

## Reconciliation Summary

```http
GET /reconciliation/summary
```

Example response:

```json
{
    "matched": 10,
    "pending": 3,
    "discrepancy": 2
}
```

---

## Reconciliation Discrepancies

```http
GET /reconciliation/discrepancies
```

Returns all transactions currently marked as discrepancies.

---

# Sample Request

```json
{
    "event_id": "11111111-1111-1111-1111-111111111111",
    "event_type": "payment_initiated",
    "transaction_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    "merchant_id": "merchant_1",
    "merchant_name": "Amazon",
    "amount": 500,
    "currency": "INR",
    "timestamp": "2026-07-19T12:00:00"
}
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/adittya003/SETU_Assignment.git
cd SETU_ASSIGNMENT
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Database Configuration

Update your PostgreSQL connection inside `config.py`.

Example:

```python
SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost:5432/payment_db"
```

---

# Running the Application

Seed the merchants:

```bash
python seed/seed_merchant.py
```

Run the application:

```bash
python app.py
```

Server starts at:

```text
http://localhost:5000
```

---

# Error Handling

The application uses centralized exception handling.

| Status Code | Description           |
| ----------- | --------------------- |
| 200         | Success               |
| 400         | Invalid Payload       |
| 404         | Merchant Not Found    |
| 500         | Internal Server Error |

---

# Design Decisions

### Layered Architecture

Business logic is separated from route handlers. Routes are responsible only for request handling, while services encapsulate business logic and database operations.

### Service-Based Design

Each service has a single responsibility:

* MerchantService
* TransactionService
* PaymentEventService
* ReconciliationService

EventProcessingService orchestrates the complete workflow.

### Idempotent Processing

Duplicate events are detected using the unique `event_id`, ensuring each payment event is processed exactly once.

### State Machine-Based Processing

Transactions follow a controlled payment lifecycle:

```text
INITIATED → PROCESSED → SETTLED
```

Invalid transitions are preserved as reconciliation discrepancies rather than rejected, enabling downstream investigation.

### Merchant Validation

Both `merchant_id` and `merchant_name` are validated against the seeded merchant records before processing any event to ensure data consistency.

### Atomic Database Transactions

Database operations are executed within a single transaction. If any step fails, the transaction is rolled back to prevent partial writes.

### Centralized Exception Handling

Custom exception handlers provide consistent API responses and keep route handlers clean.

---

# Future Improvements

* Swagger / OpenAPI documentation
* Docker support
* Unit tests
* Integration tests
* Authentication & Authorization
* Flask-Migrate for database migrations
* Asynchronous event processing using Kafka or RabbitMQ

---

# Author

**Adittya Narayan**
