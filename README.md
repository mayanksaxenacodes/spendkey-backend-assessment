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

## Copyright

Copyright © 2026 SpendKey. All Rights Reserved.

This software cannot be copied and/or redistributed via any medium without the
express written permission of SpendKey. See the accompanying [LICENSE] for
details.

**Proprietary and confidential.**

[license]: LICENSE
