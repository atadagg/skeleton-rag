# RAG Skeleton for Companies

## Architectural Overview

This project is a Retrieval-Augmented Generation (RAG) skeleton designed for companies to index, search, and query their internal data using LLMs. The architecture is modular, but currently many modules are unimplemented or incomplete. This README reflects the current state and outlines the necessary improvements.

## Project Structure

- **/indexer**: Handles data ingestion and indexing. Consists of a data fetcher, data embedder (preprocessor, chunker, metadata extractor), and a vector DB connection. Currently, the pipeline is monolithic and tightly coupled to Pinecone. Refactoring is needed for abstraction and flexibility.
- **/query**: Intended to be the LLM core of the application. Receives input, embeds it, retrieves top N similar results, builds prompts, and interacts with the LLM. **Currently, this module is a placeholder and must be fully implemented.**
- **/websocket**: Handles websocket connections and routes. Contains a router, connection manager, and handler. **Currently unimplemented.**
- **/app**: FastAPI application entry point. Lacks centralized configuration and dependency management. Routers for websocket and authentication are commented out.
- **/auth**: Intended for two-step authentication (token generation and validation for websocket). **Currently unimplemented.**

## Key Architectural Issues & TODOs

- No dedicated ingestion layer. Ingestion is currently a batch process, not a robust, scalable service.
- No open ingestion API for dynamic data submission (e.g., /ingest/file, /ingest/url, /ingest/repo).
- No persistent asynchronous job queue for ingestion/indexing (should use Celery, RQ, etc.).
- No extensible document parsers for various file formats (PDF, DOCX, HTML, etc.).
- Hardcoded configuration and credentials scattered throughout the codebase.
- Tight coupling to Pinecone; no abstraction for vector DB providers.
- Poor error handling and logging.
- Core modules (query, websocket, auth) are skeletons and must be implemented.

## Improvements & Recommendations

- **Implement a robust ingestion layer** with an open API and asynchronous job queue.
- **Centralize configuration management** for all services (database, embedding model, API keys, etc.).
- **Abstract the vector database layer** to support multiple providers.
- **Implement extensible document parsers** for various file formats.
- **Add robust error handling and logging** throughout the pipeline.
- **Fully implement the query, websocket, and authentication modules** with proper security and session management.
- Add unit and integration tests for each module.
- Use environment variables for sensitive config (e.g., API keys) and document them.
- Use dependency injection for easier testing and flexibility.
- Document API endpoints and authentication flow for users and developers.

## Example Ingestion API (to be implemented)

```
POST /ingest/file
POST /ingest/url
POST /ingest/repo
```
Each endpoint should accept relevant parameters and submit an ingestion job to a persistent queue. Workers will process jobs asynchronously, parse documents, and update the vector database.

## Configuration

All configuration (API keys, model names, DB settings, etc.) should be managed via a centralized config file or environment variables. Avoid hardcoding values in the codebase.

## Current Status

This project is a work in progress. Many modules are placeholders and require significant development to reach production readiness. See the TODO list for prioritized next steps.