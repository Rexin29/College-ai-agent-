from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain_core.documents import Document


class BaseProcessor(ABC):
    """Base class for document processors"""

    @abstractmethod
    def process(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Process a file and return Document objects
        
        Args:
            file_path: Path to the file
            metadata: Optional metadata dictionary
            
        Returns:
            List of Document objects
        """
        pass
