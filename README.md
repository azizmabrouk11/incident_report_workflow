# 🚮 Incident Reporting & Vector Store Automation

**Intelligent n8n workflows** for automated waste management incident handling

* vector database migration for semantic search & future AI capabilities.

<p align="center">
  <img src="https://img.shields.io/badge/n8n-Workflow-EA4B71?style=flat-square" />
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/Pinecone-VectorDB-FF6F61?style=flat-square" />
  <img src="https://img.shields.io/badge/Google%20Gemini-Embeddings-4285F4?style=flat-square&logo=google" />
  <img src="https://img.shields.io/badge/Groq-AI-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Gmail-EA4335?style=flat-square&logo=gmail&logoColor=white" />
</p>

---

## 📖 Overview

This repository contains **two complementary n8n workflows** designed for modern municipal waste management:

### 1️⃣ Incident Report Automation

* Monitors **Gmail**
* Extracts structured data using **AI**
* Detects duplicates
* Classifies priority
* Routes notifications intelligently

### 2️⃣ Vector Store Migration & Embedding

* Reads existing incidents from **MongoDB**
* Chunks & embeds using **Google Gemini**
* Upserts into **Pinecone Vector Database**
* Preserves original MongoDB `_id` in metadata for traceability

📌 Both workflows share the same MongoDB **`incidents`** collection and form the foundation for:

* Semantic search
* Similarity analysis
* RAG applications
* Future AI enhancements

---

## ✨ Features

### 🚨 Incident Report Workflow

* Real-time Gmail inbox monitoring
* Groq-powered structured data extraction
* Semantic + location-based duplicate detection
* Automatic priority scoring (low / medium / high)
* Conditional routing (citizen reply vs admin alert)
* Contextual AI-generated email responses

### 🧠 Vector Migration Workflow

* Full or incremental migration from MongoDB
* Smart text chunking & cleaning
* High-quality embeddings using `gemini-embedding-001`
* MongoDB `_id` stored as `metadata.original_id`
* Efficient batch upsert to Pinecone
* Ready for semantic search & similarity-based analytics

---

## 📂 Repository Structure

```text
├── incident-report/
│   └── incident_report.json          # Main incident processing workflow
├── vector-migration/
│   └── vector_migration.json         # Vector database population workflow
├── README.md
└── docs/
```

---

## 🛠️ Prerequisites

* n8n (self-hosted or cloud, v1.0+ recommended)
* MongoDB (with `incidents` collection)
* Pinecone account & index

  * 3072 dimensions recommended for Gemini
* Google Gemini API key (embeddings)
* Groq API key (LLM extraction & generation)
* Gmail OAuth2 credentials
* Community nodes:

  * `@n8n/n8n-nodes-langchain`
  * `n8n-nodes-base.gmail`
  * `n8n-nodes-base.mongoDb`

---

## 🚀 Quick Setup

### 1️⃣ Import workflows

```bash
# Via n8n UI: Settings → Import from File
# or CLI (self-hosted)
n8n import:workflow --input=./incident-report/incident_report.json
n8n import:workflow --input=./vector-migration/vector_migration.json
```

### 2️⃣ Configure credentials

| Service       | Credential Type   | Used In                |
| ------------- | ----------------- | ---------------------- |
| Gmail         | OAuth2 API        | Trigger + Send nodes   |
| MongoDB       | MongoDB           | All MongoDB operations |
| Groq          | Groq API          | Chat Model nodes       |
| Google Gemini | Google Gemini API | Embeddings sub-node    |
| Pinecone      | Pinecone API      | Vector Store node      |

---

## 🔄 How the Workflows Connect

```text
MongoDB ───────────────┐
                       │
Incident Report        │   Vector Migration
   │                   │        │
   ▼                   ▼        ▼
Gmail → AI Extract → Duplicate Check
                       MongoDB → Chunk → Embed (Gemini) → Pinecone
   │                   │                   │
   ▼                   ▼                   ▼
Citizen/Admin Emails   New/Updated Record   Vector DB ready for search & RAG
```

---

## 🎯 Customization Suggestions

* Switch to other embedders (Cohere, Voyage, OpenAI…)
* Add metadata filtering in Pinecone queries
* Implement incremental sync (only new/updated documents)
* Build a semantic search API or chatbot

---

## ⚠️ Current Limitations & Workarounds

* **Pinecone Vector Store node auto-generates IDs**
  → Store MongoDB `_id` as `metadata.original_id` for traceability

* **Large collections may slow n8n**
  → Use **Split In Batches** node before processing

---

## 💬 Author & Contact

**Mohamed Aziz Mabrouk**
📅 January 2026

Built with ❤️ for smarter waste management systems.

Questions, improvements, or collaboration?
👉 **Open an issue!** 


---

## 🔗 Useful Resources

* n8n Documentation
* Pinecone Documentation
* Google Gemini Embeddings
* Groq API Reference

