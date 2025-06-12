import os
from typing import List, Dict, Any
from pinecone import Pinecone
from pinecone import ServerlessSpec, CloudProvider, AwsRegion

# Placeholder for pinecone import
# import pinecone

class VectorDBConnection:
    """Handles connection to the Pinecone Vector DB."""
    def __init__(self, api_key: str, index_name: str, dimension: int, region: str = "us-east-1", cloud: str = "aws"):
        self.api_key = api_key
        self.index_name = index_name
        self.dimension = dimension
        self.region = region
        self.cloud = cloud
        self.pc = None
        self.index = None

    def connect(self):
        """Establish connection to the Pinecone vector DB and set the index. Creates index if it doesn't exist."""
        self.pc = Pinecone(api_key=self.api_key)
        # Check if index exists, create if not
        if self.index_name not in [idx.name for idx in self.pc.list_indexes()]:
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=CloudProvider.AWS,
                    region=AwsRegion.US_EAST_1
                )
            )
        # Get index host
        index_config = self.pc.describe_index(self.index_name)
        self.index = self.pc.Index(host=index_config.host)

    def upsert(self, vectors: List[Dict[str, Any]], namespace: str = "default"):
        """Upsert a list of vectors into the index. Each vector: {"id": str, "values": List[float], "metadata": dict (optional)}"""
        pinecone_vectors = []
        for v in vectors:
            pinecone_vectors.append((v["id"], v["values"], v.get("metadata", {})))
        self.index.upsert(vectors=pinecone_vectors, namespace=namespace)

    def query(self, vector: List[float], top_k: int = 5, namespace: str = "default", filter: dict = None) -> List[Dict[str, Any]]:
        """Query the index for the top_k most similar vectors to the given vector."""
        results = self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace,
            filter=filter
        )
        return results.matches 