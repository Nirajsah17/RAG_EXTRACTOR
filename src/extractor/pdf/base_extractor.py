from abc import ABC, abstractmethod
from typing import TypedDict, Literal, Optional, Tuple, Any, List


class Element(TypedDict):
    type: Literal["text", "image", "table"]
    content: Any
    page: int
    bbox: Optional[Tuple[float, float, float, float]]
    metadata: dict
        
class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> List[Element]:
        pass
      
      
