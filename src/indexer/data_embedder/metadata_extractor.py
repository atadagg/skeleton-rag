from typing import Optional, Dict
import re

class MetadataExtractor:
    """Extracts metadata from data for embedding."""
    def __init__(self):
        pass

    def extract(self, text: str, file_name: Optional[str] = None) -> Dict[str, str]:
        """Extract metadata such as title, word count, character count, and file name."""
        metadata = {}
        # Title: first non-empty line or file name
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if lines:
            metadata['title'] = lines[0][:100]  # Truncate long titles
        elif file_name:
            metadata['title'] = file_name
        else:
            metadata['title'] = 'Untitled'
        # Word count
        metadata['word_count'] = str(len(re.findall(r'\w+', text)))
        # Character count
        metadata['char_count'] = str(len(text))
        # File name
        if file_name:
            metadata['file_name'] = file_name
        # Language detection (very basic, can be replaced with langdetect)
        if re.search(r'[\u0400-\u04FF]', text):
            metadata['language'] = 'Cyrillic-based'
        elif re.search(r'[\u4e00-\u9fff]', text):
            metadata['language'] = 'Chinese'
        else:
            metadata['language'] = 'English/Other'
        return metadata 