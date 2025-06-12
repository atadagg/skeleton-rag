import re
from typing import List

class Preprocessor:
    """Preprocesses raw data before embedding."""
    def __init__(self):
        pass

    def to_lower(self, text: str) -> str:
        """Convert text to lowercase."""
        return text.lower()

    def remove_extra_whitespace(self, text: str) -> str:
        """Remove extra whitespace from text."""
        return re.sub(r'\s+', ' ', text).strip()

    def remove_punctuation(self, text: str) -> str:
        """Remove basic punctuation from text."""
        return re.sub(r'[\.,!?;:()\[\]{}\-]', '', text)

    def process(self, text: str) -> str:
        """Apply all preprocessing steps to the input text."""
        text = self.to_lower(text)
        text = self.remove_extra_whitespace(text)
        text = self.remove_punctuation(text)
        return text 