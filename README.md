# 🚮 Incident Reporting & Vector Store Automation

**Automated incident processing and semantic search using n8n, MongoDB, and Pinecone vector databases**

This repository demonstrates how an email-based incident reporting system can evolve into a **scalable, AI-ready architecture** by combining workflow automation with vector embeddings and semantic search.

---

## 🧩 What This Project Does

The system is built around **three integrated components**:

### 1️⃣ Incident Processing Workflow

Handles incoming incident reports and turns unstructured emails into actionable data.

**Key responsibilities**

* Monitor incoming emails (Gmail)
* Extract structured information using LLMs (description, location, intent)
* Detect duplicates and classify priority
* Route responses automatically (citizen reply or admin alert)

---

### 2️⃣ Vector Migration & Embedding Workflow

Transforms historical incident data into a **vector-based representation** for intelligent retrieval.

**Key responsibilities**

* Read incidents from MongoDB
* Clean, chunk, and embed text fields
* Store vectors in Pinecone
* Preserve MongoDB `_id` in metadata for traceability

---

### 3️⃣ Similarity Service (FastAPI)

Provides a **REST API** for real-time semantic search across stored incidents.

**Key responsibilities**

* Accept text queries via HTTP
* Generate embeddings using Google Gemini
* Query Pinecone for similar incidents
* Return ranked matches with similarity scores

Together, these components enable:

* Semantic duplicate detection
* Similarity-based analysis
* RAG applications and intelligent search
* Integration with external systems

---

## ✨ Core Features

### 🚨 Incident Automation

* Gmail inbox monitoring
* AI-powered information extraction
* Semantic + location-aware duplicate detection
* Automatic priority scoring
* Context-aware email responses

### 🧠 Vector Store Pipeline

* Batch or incremental migration
* High-quality embeddings via Google Gemini
* Metadata preservation for auditability
* Optimized upserts to Pinecone
* Ready for semantic search and AI agents

### 🔍 Similarity API

* RESTful endpoint for semantic search
* Real-time embedding generation
* Configurable similarity threshold and result count
* Returns MongoDB IDs for cross-referencing
* FastAPI with automatic OpenAPI docs

---

## 🏗️ Architecture Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                     INCIDENT PROCESSING                      │
└─────────────────────────────────────────────────────────────┘

Gmail → n8n (AI extraction & routing) → MongoDB

┌─────────────────────────────────────────────────────────────┐
│                   VECTOR STORE PIPELINE                      │
└─────────────────────────────────────────────────────────────┘

MongoDB → Vector Migration Workflow → Embeddings (Gemini) → Pinecone

┌─────────────────────────────────────────────────────────────┐
│                    SIMILARITY SERVICE                        │
└─────────────────────────────────────────────────────────────┘

HTTP Request → FastAPI → Embed Query → Pinecone Search → JSON Response
                  ↓
            (returns MongoDB IDs)
```

---

## 📂 Repository Structure

```text
incident_report_workflow/
├── README.md
├── incident_report/
│   └── incident_report.json
├── similarity-service/
│   ├── .env.example
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── embedding.py
│       ├── main.py
│       ├── pinecone_client.py
│       └── schemas.py
└── vector-migration/
    ├── embeddingsGeneration.json
    └── semantic_similarity_search_pinecone.ipynb
```

---

## 🛠️ Requirements

**n8n Workflows**

* n8n (v1.0+ recommended)
* MongoDB (`incidents` collection)
* Gmail OAuth2 credentials
* Groq API key (LLM extraction & generation)
* Google Gemini API key (embeddings)
* Community nodes:
  * `@n8n/n8n-nodes-langchain`
  * `n8n-nodes-base.gmail`
  * `n8n-nodes-base.mongoDb`

**Similarity Service**

* Python 3.8+
* Pinecone index (3072 dimensions for Gemini)
* Google Gemini API key
* Pinecone API key

---

## 🚀 Getting Started

### 1️⃣ Import n8n workflows

```bash
n8n import:workflow --input=./incident-report/incident_report.json
n8n import:workflow --input=./vector-migration/vector_migration.json
```

### 2️⃣ Configure n8n credentials

Set up credentials inside n8n for:

* Gmail
* MongoDB
* Groq
* Google Gemini
* Pinecone

### 3️⃣ Set up Similarity Service

```bash
cd similarity-service

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys:
# PINECONE_API_KEY=your_key
# GEMINI_API_KEY=your_key
# PINECONE_INDEX=incidents

# Run the service
uvicorn app.main:app --reload --port 8000
```

### 4️⃣ Test the API

```bash
curl -X POST "http://localhost:8000/similar-incidents" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "broken streetlight on Main Street",
    "top_k": 5,
    "min_score": 0.7
  }'
```

**Response example:**

```json
{
  "matches": [
    {
      "mongodb_id": "507f1f77bcf86cd799439011",
      "score": 0.92,
      "text": "Streetlight malfunction at Main St intersection"
    },
    {
      "mongodb_id": "507f191e810c19729de860ea",
      "score": 0.85,
      "text": "Non-functioning light pole near Main Street"
    }
  ]
}
```

---

## 📡 API Reference

### POST `/similar-incidents`

Find semantically similar incidents from the vector database.

**Request Body:**

```json
{
  "text": "string",        // Query text to find similar incidents
  "top_k": 5,              // Number of results (default: 5)
  "min_score": 0.7         // Minimum similarity score 0-1 (default: 0.7)
}
```

**Response:**

```json
{
  "matches": [
    {
      "mongodb_id": "string",  // Original MongoDB document ID
      "score": 0.92,            // Similarity score (0-1)
      "text": "string"          // Matched incident text
    }
  ]
}
```

**Interactive docs:** `http://localhost:8000/docs` (when running)

---

## ⚠️ Notes & Design Decisions

* Pinecone auto-generates vector IDs
  → MongoDB `_id` is stored as metadata for traceability

* Large datasets
  → Use **Split In Batches** to avoid performance issues in n8n

---

## 🎯 Possible Extensions

* Incremental sync (only new or updated incidents)
* Metadata-based filtering in vector search
* Webhook integration from n8n to similarity service
* Chatbot layer using the similarity API
* Alternative embedding providers (OpenAI, Cohere, Voyage)
* Authentication & rate limiting for production
* Caching layer for frequent queries

---

## 👤 Author

**Mohamed Aziz Mabrouk**
January 2026

Built with a focus on **automation, clarity, and future AI extensibility**.

Feel free to open an issue for questions or improvements.

