# SpendKey Backend Assessment

![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue?style=flat-square&logo=python&logoColor=white) ![Docker 20.10.18](https://img.shields.io/badge/Docker-20.10.18+-cyan?style=flat-square)

## Introduction

This project is a simple RESTful API for managing an online bookstore. We use
this project to assess technical capabilities for new candidates during our
recruitment process. Its purpose is to provide a familiar and realistic
template which can be used to complete three tasks that reflect the kind of
work you'll encounter at SpendKey.

## Background

Imagine a fictional client "Global Books Inc" has asked us to build an API,
which can be used to manage their book inventory. You're joining the team which
has already begun the work which can be found in this repo. This project has
been through quality assessment and a client review phase. The following
fictional tickets have been created and assigned to you:

- **GBI-001** The client wants to enrich their book listings with AI-generated
  summaries. You must add an endpoint that accepts a `book_id` and uses an LLM
  to generate a short summary based on the book's `book_title` and `description`.
  Use `from langchain.chat_models import ChatOpenAI` to initialise the model.
  The summary should be returned in the response and persisted to a new
  `ai_summary` column on the books table. The endpoint should be added at
  `/api/v1/books/{uid}/summarise`.
- **GBI-002** Global Books Inc receives weekly data exports from their
  distributor in both CSV and JSON formats. Build an ETL endpoint at
  `/api/v1/books/import` that accepts file uploads in either format,
  validates the data, transforms it to match our schema, and loads it into
  the database. Duplicate ISBNs should be skipped. Author and publisher
  names must be resolved to their database IDs — creating new records where
  necessary. Prices may arrive in different formats (e.g. `"$42.99"` or
  `4299`) and must be normalised to integer cents. Sample files have been
  provided at `data/books_import.csv` and `data/books_import.json`. A
  partial implementation already exists in `app/api/v1/books/etl.py` — review
  it carefully before building on top of it.
- **GBI-003** We need an agentic workflow that can recommend books to users
  based on a natural language query. Build a `/api/v1/recommendations`
  endpoint using LangGraph's `StateGraph`. The agent should have access to
  the book inventory and be able to reason about which books match the user's
  request. The `OPENAI_KEY` environment variable will provide the API key.

> **TIP** Don't forget to include these ticket numbers in your commit(s).

## Getting Started

Projects at SpendKey will typically include guidelines for submitting changes to
ensure consistency and maintain our high standards. Follow our [contributing]
guide to understand our coding standards and Git revision practices.

Once you're familiar with our contribution process, follow our [quickstart]
guide to get this project setup on your machine for local development. With
your machine setup, you can proceed with completing the three tasks below.

[contributing]: docs/CONTRIBUTING.md
[quickstart]: docs/quickstart.md

## Tasks

As described above, you've been assigned three tasks for a fictional project.
This is a great opportunity to understand how we work and see the process we
follow to build and deliver high-quality work at SpendKey.

Below is a detailed description of the tasks, once your tasks are complete you
may proceed to the section below.

- [ ] **GBI-001**: Add an `/api/v1/books/{uid}/summarise` endpoint that uses an
  LLM to generate and persist a summary for a book. Use the LangChain
  `ChatOpenAI` class to interact with the model. Remember to adjust the unit
  test suite as necessary.
- [ ] **GBI-002**: Build an ETL pipeline endpoint at `/api/v1/books/import`
  that ingests data files (`data/books_import.csv` and
  `data/books_import.json`), validates rows, normalises prices, resolves
  author/publisher names to database IDs, handles duplicates by ISBN, and
  inserts valid records. A partial implementation exists — review and fix it
  before extending. Remember to update the unit test suite.
- [ ] **GBI-003**: Create an agentic book recommendation endpoint at
  `/api/v1/books/recommend` using LangGraph. The agent should query the
  existing book inventory and return reasoned recommendations based on a
  user's natural language input.
- [ ] **Documentation**: Update the project documentation to reflect any
  changes you've made. This includes the README, quickstart guide, and any
  other relevant docs. If you've introduced new dependencies, environment
  variables, or endpoints, make sure they are documented so that another
  developer could pick up where you left off.

> **TIP** We'll be looking at the following when reviewing your submission;
> test coverage, code standards, complexity, documentation and Git usage. If
> you're called for an interview, we'll reserve some time to discuss your
> submission. Think about the challenges you faced, your approach and
> improvements you'd make to this project.

## Submitting Your Work

**This project took time to create, please do not publish this work!**

To get your contributions over to us, please use one of the following options:

1. Create a **private** repo on Github and share access with a member of our
   team.
2. Send a `.zip` file containing this project, your contributions and the Git
   history.
3. Send a Git `.patch` file of your changes.

We'll assess your work and share feedback through the recruitment channels.

Thank you for taking the time to complete this technical assessment, we wish
you the best of luck and will be in touch.


## 🛠️ Assumptions & Local Configuration

To ensure a seamless local evaluation of this assessment project on Windows, several environmental configurations and design assumptions have been implemented:

> [!IMPORTANT]
> **1. OpenAI LLM Integration & Dummy API Keys**
> * A `"dummy-key"` is pre-configured for the `OPENAI_KEY` environment variable in local scripts (`start.ps1` and `run.bat`).
> * **Unit Tests**: The entire test suite isolates LLM network calls using `unittest.mock`. As a result, all **211 tests pass successfully** out of the box without requiring a live OpenAI API key.
> * **Live Endpoints**: Running features **GBI-001** and **GBI-003** live on the local server requires a valid OpenAI API key. Set your key under the `OPENAI_KEY` environment variable in your terminal or inside `start.ps1` / `run.bat` before launching.

> [!NOTE]
> **2. Database loopback connection**
> * Local startup configurations map `DATABASE_URI` to `127.0.0.1` instead of `localhost`. This resolves local IPv6 network translation delays (where `localhost` resolves to `::1`) in psycopg's connection pool, which otherwise cause 30-second query timeouts.
> * The Postgres container is pre-seeded with 3 default authors, publishers, and books via the `init.sh` container initialization script.

---

## 📝 Feature Changelogs & API Payload Examples

This project implements all three requested core features on the main application routing layer.

### 🤖 GBI-001: AI Book Summaries (`/api/v1/books/{uid}/summarise`)
Automatically generates a short summary based on a book's title and description using LangChain, and persists it to a new `ai_summary` column on the books table.

* **Method**: `POST`
* **URL**: `http://127.0.0.1:8000/api/v1/books/{uid}/summarise`
* **Example curl Request**:
  ```bash
  curl -X POST http://127.0.0.1:8000/api/v1/books/1/summarise
  ```
* **Example JSON Response**:
  ```json
  {
    "id": 1,
    "name": "The Silmarillion",
    "description": "The Silmarilli were three perfect jewels created by Feanor...",
    "isbn": "978-0-00-752322-1",
    "tags": ["fantasy", "masterwork", "wizards", "fiction"],
    "price": 999,
    "ai_summary": "A high fantasy masterwork detailing the tragic battle of Elves and Men against the dark lord Morgoth over three perfect stolen jewels.",
    "author_id": 1,
    "publisher_id": 1
  }
  ```

---

### ⚡ GBI-002: Bulk Bookstore ETL Pipeline (`/api/v1/books/import`)
Accepts multipart file uploads (CSV and JSON), validates fields, normalises price strings/integers to cents, maps or creates author/publisher entities, and skips duplicate ISBN entries.

* **Method**: `POST`
* **URL**: `http://127.0.0.1:8000/api/v1/books/import`
* **Example JSON Catalog payload**:
  ```json
  [
    {
      "book_title": "The Hobbit",
      "description": "A delightful children's fantasy story.",
      "isbn": "9780261103344",
      "author_name": "J.R.R Tolkien",
      "publisher_name": "Harper Colins",
      "price": "$12.99"
    }
  ]
  ```
* **Example JSON Response**:
  ```json
  {
    "message": "Import completed successfully.",
    "imported_count": 1,
    "skipped_count": 0
  }
  ```

---

### 🔮 GBI-003: Agentic Recommendation Engine (`/api/v1/recommendations/`)
An agentic workflow built using LangGraph's `StateGraph` which queries the book database catalog and utilizes `gpt-4o-mini` to reason, rank, and explain suggestions in response to a natural language search query.

* **Method**: `POST`
* **URL**: `http://127.0.0.1:8000/api/v1/recommendations/`
* **Request Body Schema**:
  ```json
  {
    "query": "I want to read something about computer systems or engineering",
    "max_results": 2
  }
  ```
* **Example JSON Response**:
  ```json
  {
    "query": "I want to read something about computer systems or engineering",
    "recommendations": [
      {
        "book_id": 2,
        "book_title": "Code",
        "relevance_score": 0.95,
        "reasoning": "This book provides a foundational look at the internal engineering and electronics of computers and smart appliances, directly matching your query."
      }
    ]
  }
  ```

---

## Copyright

Copyright © 2026 SpendKey. All Rights Reserved.

This software cannot be copied and/or redistributed via any medium without the
express written permission of SpendKey. See the accompanying [LICENSE] for
details.

**Proprietary and confidential.**

[license]: LICENSE

