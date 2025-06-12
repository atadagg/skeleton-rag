from typing import List

class Chunker:
    """Chunks data into smaller pieces for embedding."""
    def __init__(self, chunk_size: int = 512, stride: int = 256):
        self.chunk_size = chunk_size
        self.stride = stride

    def chunk(self, text: str) -> List[str]:
        """Split the input text into overlapping chunks."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.stride):
            chunk = words[i:i + self.chunk_size]
            if chunk:
                chunks.append(' '.join(chunk))
            if i + self.chunk_size >= len(words):
                break
        return chunks 