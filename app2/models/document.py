from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class DocumentNode:
    doc_id: str
    page: int
    block_id: int
    type: str
    text: str
    bbox: Optional[list]
    metadata: Dict[str, Any]

    def to_dict(self):
        return {
            "doc_id": self.doc_id,
            "page": self.page,
            "block_id": self.block_id,
            "type": self.type,
            "text": self.text,
            "bbox": self.bbox,
            "metadata": self.metadata
        }