# RAG Skeleton for Companies

## Project Structure:

/indexer: Keeps data up-to-date by indexing the data sources of the company. It consists of a data fetcher, data embedder(preprocessor,chunker,metadata extractor) and a vector DB connection. Python Pinecone Vector DB, Langchain and Langgraph will be used. Data will be pulled from Github and Documentations in Google Drive but it must be adaptable to any source, not hardcoded. 

> **Indexing:** Indexing is triggered manually (via API/button) or on a schedule (e.g., hourly), not by continuous listeners. Data sources implement a standard interface (`DataSource`). To add a new source, simply create a new class inheriting from `DataSource` and update the config.

/query: LLM Core of the application. Receives input, embeds it into a query, get the top N most semantically similar results(chunks), combine the retrieved chunks and chat memory to a prompt and feed it into the LLM. This process consists of a query embedder, vector db retriever, a memory manager, prompt builder, an LLM client and a query orchestrator

/websocket: This handles all the concerns with our websocket connections and routes. It has a router, a connection manager and an handler.


/app: This is where the FastAPI lives. ıt's made up of main, dependencies, config

/auth: a two step authentication. One to generate a token through HTTP, one to use that token(validation) to establish a websocket connection. 

## Improvements & Recommendations

- Consider adding unit and integration tests for each module.
- Use environment variables for sensitive config (e.g., API keys) and document them.
- Add logging and error handling for production readiness.
- Use dependency injection for easier testing and flexibility.
- Document API endpoints and authentication flow for users and developers.