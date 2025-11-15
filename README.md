# 📘 **API Cataloger — Unified Internal API Discovery System**

API Cataloger is a system that automatically discovers APIs across your organization, parses both OpenAPI files *and* Java controller annotations, enriches them with metadata, and presents everything in a centralized, searchable catalog.

Its goal is simple:

### **Make every internal API findable, understandable, and trustworthy.**

This project bridges a major gap that Swagger/OpenAPI alone cannot solve.

---

## 🧩 Why This Project Exists

Modern engineering teams maintain dozens or hundreds of microservices.
APIs end up hidden across repositories, undocumented, duplicated, or forgotten.

**Swagger/OpenAPI only documents one service at a time.**
It cannot:

* Aggregate APIs from multiple repos
* Parse Java controllers without specs
* Track ownership, last updates, or status
* Provide cross-service search
* Give architectural visibility

**API Cataloger does all of this.**
It acts like a **central library for all internal APIs**.

---

## 🎯 What API Cataloger Gives You (In Plain English)

* A complete inventory of **all APIs across your organization**
* Unified documentation extracted from:

  * OpenAPI/Swagger files
  * Java Spring controllers
  * Annotations and decorators
* Metadata enrichment:

  * Owning team
  * Status (active/deprecated/experimental)
  * Last updated time
* A searchable web UI (React)
* A backend service (Java/Spring Boot) that processes, normalizes, and exposes the catalog
* Automatic scanning and periodic updates

In short:

### **Engineers stop asking “do we already have an API for this?”

They simply search and find it.**

---

## 🚀 What This Project Is *Not* (Important Clarification)

This is **not** a replacement for Swagger/OpenAPI.
It **uses** Swagger/OpenAPI wherever available, and compliments them by:

* Filling gaps when specs are missing
* Adding organizational metadata
* Aggregating across services
* Providing a centralized UI

Swagger = documentation for one service
API Cataloger = documentation + intelligence for the entire organization

---

## 🏗 How the System Works (High-Level)

API Cataloger has three major components:

### **1. Ingestion Layer**

* Scans repositories
* Finds OpenAPI files & Java controller files
* Collects metadata

### **2. Parsing + Enrichment Layer**

* Extracts endpoints from both specs and code
* Normalizes the data
* Adds team ownership, status, timestamps

### **3. Catalog + UI Layer**

* Stores all APIs in a database
* Indexes for fast search
* React UI for discoverability

Think of it as **Google for your internal APIs**.

---

## 📁 Project Structure (Simple Overview)

```
api-cataloger/
├── backend/        # Java Spring Boot service (API parser & catalog API)
├── frontend/       # React web UI for searching APIs
├── docs/           # Multi-page documentation
├── scripts/        # Helpers to run both services together
└── README.md       # This file
```

---

## 📚 Full Documentation (Multi-Page)

### 📘 **Architecture**

Architecture overview, diagrams, pipeline flow
👉 `docs/architecture.md`

### 📘 **Data Model**

APIService, Endpoint, Team, and metadata schema
👉 `docs/data-model.md`

### 📘 **Ingestion**

Repository scanning, file discovery, configuration
👉 `docs/ingestion.md`

### 📘 **Parsers**

OpenAPI extraction & Java annotation parsing
👉 `docs/parsers.md`

### 📘 **Metadata Enrichment**

Owner mapping, Git timestamps, status resolution
👉 `docs/enrichment.md`

### 📘 **Deployment Guide**

How to run in dev and production
👉 `docs/deployment.md`

---

## 💻 Running the Project (Local Demo)

### Backend (Java)

```
cd backend
mvn spring-boot:run
```

### Frontend (React)

```
cd frontend
npm install
npm run dev
```

### Or run both together:

```
./scripts/dev.sh
```

---

## 💼 Why This Project Is Valuable to Your Organization

* Faster onboarding
* Less duplicated API development
* Instant visibility of API surface area
* Better governance and compliance
* Stronger cross-team communication
* Improves developer experience (DX)

Just tell me the number.

