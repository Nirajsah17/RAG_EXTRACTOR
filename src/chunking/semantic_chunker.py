from typing import List


class SemanticChunker:
    def chunk(self, text: str, chunk_size: int = 1000) -> List[str]:
        if not text:
            return []

        cleaned = ' '.join(text.split())
        return [cleaned[i:i + chunk_size] for i in range(0, len(cleaned), chunk_size)]
