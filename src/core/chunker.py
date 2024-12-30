# core/chunker.py

from typing import List, Dict
import os.path as osp
from ..config import load_config

_config = load_config()

class TextChunker:
    """Fixed size text chunking with overlap"""

    def __init__(self, chunk_size: int = None, overlap: int = None):
        self.chunk_size = chunk_size or _config["chunking"]["chunk_size"]
        self.overlap = overlap or _config["chunking"]["overlap"]

    def chunk_text(self, text: str) -> List[Dict]:
        """Split text into fixed-size chunks with overlap"""
        if not text:
            return []

        chunks = []
        start_pos = 0

        while start_pos < len(text):
            end_pos = min(start_pos + self.chunk_size, len(text))
            if end_pos < len(text):
                space_pos = text[start_pos:end_pos].rfind(' ')
                if space_pos != -1:
                    end_pos = start_pos + space_pos + 1

            chunk_text = text[start_pos:end_pos].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        "chunk_id": str(len(chunks)),
                        "start_pos": start_pos,
                        "end_pos": end_pos
                    }
                })

            if end_pos >= len(text):
                break

            start_pos = end_pos - self.overlap
            if start_pos <= end_pos - self.chunk_size:
                start_pos = end_pos

        return chunks
