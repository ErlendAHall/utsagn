# Utsagn - AI Coding Instructions

## Project Overview
**Utsagn** is a Norwegian political statement database that stores and retrieves political quotes using vector embeddings. The system enables natural language queries against political statements using ChromaDB and FastAPI.

**Key Domain Concepts:**
- **Utsagn** (Norwegian): "Statement" or "quote" - the core entity representing a political statement
- **Speaker**: The politician who made the statement
- **Party**: Political affiliation
- **Source**: Original media source (NRK archives, fictional sources in test data)

## Architecture

### Three-Layer Structure
```
src/
├── main.py              # FastAPI REST API endpoints
├── db/
│   ├── chroma_client.py # ChromaDB wrapper and operations
│   └── seed.py          # Database seeding with fictional test data
└── models/
    └── utsagn.py        # TypedDict data models
```

### Data Flow
1. FastAPI endpoint receives natural language query → 2. `UtsagnDBClient.query_utsagn()` → 3. ChromaDB performs vector similarity search → 4. Returns matching statements with metadata

### Critical Design Decisions
- **ID Generation**: Uses MD5 hash of `statement + speaker + date_found` (see [chroma_client.py](../src/db/chroma_client.py#L52-L54) and [seed.py](../src/db/seed.py#L6-L10)). This prevents duplicate entries but allows same speaker to make identical statements on different dates.
- **Persistent Storage**: ChromaDB data stored in `./chromadb_data` (configurable via `CHROMA_PERSISTENT_LOCATION` env var)
- **Embeddings**: Uses ChromaDB's `DefaultEmbeddingFunction()` for automatic text vectorization

## Development Workflow

### Environment Setup
```bash
# Virtual environment is in .venv/
source .venv/bin/activate

# Run the FastAPI server (current branch: add-python-type-checking)
uvicorn src.main:app --reload
```

### Working with the Database
The `UtsagnDBClient` is a singleton initialized in [main.py](../src/main.py#L8):
```python
utsagn_db_client = UtsagnDBClient()  # Auto-creates/loads collection on init
```

**Seeding**: Database is currently seeded with 8 fictional political statements (see [seed.py](../src/db/seed.py#L33-L88)). These are intentionally fake to avoid real political attribution during development.

### API Endpoints
- `GET /heartbeat` - Health check
- `GET /utsagn/query?query_text=<text>` - Query statements using natural language

## Code Conventions

### Type Safety
- **Use TypedDict** for data structures (see [utsagn.py](../src/models/utsagn.py))
- Current branch `add-python-type-checking` suggests ongoing type annotation improvements
- Import pattern: `from __future__ import annotations` for forward references

### Import Organization
Relative imports from `src/`:
```python
from db.chroma_client import UtsagnDBClient
from models.utsagn import Utsagn, UtsagnRecord
```

### Data Model Structure
**Utsagn Model Fields** (defined in [utsagn.py](../src/models/utsagn.py#L5-L11)):
- `statement`: The actual quote text (stored as ChromaDB document)
- `speaker`: Politician name
- `party`: Political party
- `date_found`: ISO date string (YYYY-MM-DD format)
- `source`: Media source reference

**Note**: When writing to ChromaDB, `statement` goes into `documents`, all other fields go into `metadatas`.

## Known Issues & Gotchas

### Bug in query_utsagn()
[chroma_client.py#L42-L46](../src/db/chroma_client.py#L42-L46) has logic error:
```python
if isinstance(query_text, str):
    self.collection.peek([query_text])  # Should be .query()
else:
    self.collection.query(query_text)  # Missing return statement
```

### No Test Suite
Project currently has no tests (`def test_` searches return nothing). When adding tests, follow pytest conventions.

## 2026 MVP Roadmap
From [README.md](../README.md#L11-L15):
1. Deploy ChromaDB instance ✓ (local persistent DB exists)
2. LLM integration to scrape NRK archives (not yet implemented)
3. Quality assurance LLM for stored statements (not yet implemented)
4. User-facing natural language query interface (basic version via FastAPI)

When implementing LLM features, consider extracting statement parsing/validation into separate modules under `src/`.
