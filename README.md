# AI‑Powered FastAPI Project Generator

A CLI tool that turns a Software Requirements Specification (SRS) into a complete FastAPI service—code, tests, configs, and packaging included.

## Features

**SRS Ingestion**: Load .docx or .pdf files, split into text chunks, store embeddings in PostgreSQL (pgvector).  
**Requirement Extraction**: Use RAG + custom LLM to pull out API endpoints, business logic, schema, and auth rules.  
**Project Scaffolding**: Generate FastAPI folder layout, virtual environment, requirements, Dockerfile, and README.  
**Code & Tests**: Auto‑generate SQLAlchemy models, Pydantic schemas, routes, services, and pytest cases (TDD).  

## Prerequisites

Python 3.8+  
PostgreSQL with pgvector extension  
Groq API key (or HuggingFace token)  
alembic in your PATH or installed in your venv

## Installation
bash

cd fastapi‑srs‑generator
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt