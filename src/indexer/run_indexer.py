import os
import json
from dotenv import load_dotenv
from src.indexer.data_fetcher import get_data_sources
from src.indexer.data_embedder.preprocessor import Preprocessor
from src.indexer.data_embedder.chunker import Chunker
from src.indexer.data_embedder.metadata_extractor import MetadataExtractor
from src.indexer.data_embedder.embedder import DataEmbedder
from src.indexer.vector_db import VectorDBConnection

# Load credentials from .env in project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

"""
# .env should only contain credentials, e.g.:
# GITHUB_TOKEN=...
# PINECONE_API_KEY=...
"""

def run_indexing_pipeline(sources, pinecone_config):
    print("[Indexer] Starting pipeline...")
    # Initialize all components
    data_sources = get_data_sources({"sources": sources})
    preprocessor = Preprocessor()
    chunker = Chunker()
    extractor = MetadataExtractor()
    embedder = DataEmbedder()  # You can specify a model name here if needed
    db_conf = pinecone_config
    db = VectorDBConnection(db_conf["api_key"], db_conf["index_name"], db_conf["dimension"])
    db.connect()

    for source in data_sources:
        print(f"[Indexer] Fetching from source: {type(source).__name__}")
        docs = source.fetch()
        for doc in docs:
            text = doc["content"]
            file_name = doc.get("name")

            preprocessed = preprocessor.process(text)
            chunks = chunker.chunk(preprocessed)
            metadata = extractor.extract(text, file_name)
            
            # Generate embeddings for all chunks in a batch
            embeddings = embedder.embed(chunks)

            vectors = []
            for i, chunk in enumerate(chunks):
                vectors.append({
                    "id": f"{file_name}_{i}",
                    "values": embeddings[i],
                    "metadata": {**metadata, "chunk_index": i, "chunk_text": chunk}
                })

            if vectors:
                db.upsert(vectors)
                print(f"[Indexer] Upserted {len(vectors)} vectors for {file_name}")
    print("[Indexer] Pipeline complete.")

if __name__ == "__main__":
    # Example: get credentials from env, pass repo info as arguments
    github_token = os.environ.get("GITHUB_TOKEN")
    pinecone_api_key = os.environ["PINECONE_API_KEY"]
    gdrive_creds_path = os.environ.get("GOOGLE_DOCS_API_KEY")
    
    # Configure your sources here
    sources = [
        {
            "type": "github",
            "credentials": {"token": github_token},
            "repo": "atadagg/vim-teacher",
            "branch": "main",
            "path": ".",
            "extensions": ["*"]
        },
        {
            "type": "gdrive",
            "credentials_json": gdrive_creds_path,
            "folder_id": "YOUR_GOOGLE_DRIVE_FOLDER_ID" # <-- Replace this
        }
        # Add more sources as needed
    ]
    pinecone_config = {
        "api_key": pinecone_api_key,
        "index_name": "your-index",
        "dimension": 384  # Dimension for 'all-MiniLM-L6-v2' is 384
    }
    run_indexing_pipeline(sources, pinecone_config) 