from sentence_transformers import SentenceTransformer
from typing import List

class DataEmbedder:
    """A wrapper around a sentence-transformer model for embedding text."""
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        model_name: The name of the sentence-transformer model to use.
        """
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of texts and return the embeddings.
        """
        return self.model.encode(texts, convert_to_numpy=False)

    def embed_single(self, text: str) -> List[float]:
        """
        Embed a single text and return the embedding.
        """
        return self.model.encode(text, convert_to_numpy=False) 