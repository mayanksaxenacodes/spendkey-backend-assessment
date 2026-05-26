# GEMINI.md

## Project Overview
SpendKey Backend Assessment is a FastAPI-based RESTful API for managing a bookstore inventory. It serves as a technical assessment project to evaluate capabilities in building APIs, ETL pipelines, and AI-integrated workflows.

### Main Technologies
- **Language:** Python 3.13+
- **Framework:** FastAPI
- **Database:** PostgreSQL (via `psycopg`)
- **Validation:** Pydantic
- **AI/LLM:** LangChain, LangGraph, OpenAI
- **Tooling:** Ruff (linting/formatting), Pyright (static type checking), Bandit (security scanning), Pre-commit hooks

## Building and Running
The project uses a `Makefile` to orchestrate common development tasks.

### Initialization
```bash
make init
source venv/bin/activate
```

### Running the Database
Requires Docker and Docker Compose.
```bash
make database
```

### Running the API Server
```bash
make start
```
The server runs on `http://localhost:3000` by default (port can be overridden via `PORT` env var). Interactive OpenAPI docs are available at `http://localhost:3000/docs` if enabled.

### Running Tests
```bash
make unit
```

### Linting and Formatting
```bash
make run-hooks
```

## Development Conventions

### Coding Style
- **PEP8 & Google Python Style Guide:** Follow these standards for all Python code.
- **Line Length:** 79 characters (enforced by Ruff and Black).
- **Typing:** Strict type checking with Pyright is enforced.
- **Formatting:** Handled by Ruff/Black.

### Git & Commits
- **Branching:** Use topic branches based on `develop`. Avoid working directly on `develop`.
- **Commit Messages:** Follow the format `[TICKET-ID] type: description`.
  - Example: `[GBI-001] feat: add book summary endpoint`
- **Atomic Commits:** Make small, logical units of work.

### Architecture
- `app/api/`: Contains route definitions and logic, organized by version and resource.
- `app/common/`: Shared utilities, database connection, and validators.
- `app/server/`: FastAPI application factory and middleware.
- `tests/`: Separated into `unit/` and `integration/`.

## Key Tasks & Endpoints
1. **GBI-001: AI Book Summary**
   - Endpoint: `POST /api/v1/books/{uid}/summarise`
   - Goal: Generate book summary using LangChain `ChatOpenAI` and persist to `ai_summary` column.
2. **GBI-002: ETL Pipeline**
   - Endpoint: `POST /api/v1/books/import`
   - Goal: Ingest CSV/JSON, validate, normalize prices (to integer cents), and resolve author/publisher.
3. **GBI-003: Agentic Recommendation**
   - Endpoint: `POST /api/v1/recommendations`
   - Goal: Use LangGraph `StateGraph` for natural language book recommendations.

## Environment Variables
- `DATABASE_URI`: PostgreSQL connection string.
- `OPENAI_API_KEY`: Required for AI-related tasks.
- `ENABLE_OPENAPI_DOCS`: Set to `true` to enable Swagger UI.
- `ENABLE_DEBUG`: Set to `true` for verbose logging.
