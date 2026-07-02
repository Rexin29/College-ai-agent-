import os
from typing import List, Dict, Any
from pathlib import Path
from langchain_core.documents import Document
from utils.logger import logger
from .base_processor import BaseProcessor


class TextProcessor(BaseProcessor):
    """Process plain text files"""

    def process(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Process text file
        
        Args:
            file_path: Path to text file
            metadata: Optional metadata dictionary
            
        Returns:
            List of Document objects
        """
        documents = []
        metadata = metadata or {}
        
        try:
            logger.info(f"Processing text file: {file_path}")
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if content.strip():
                doc_metadata = {
                    **metadata,
                    "source": Path(file_path).name,
                }
                
                document = Document(
                    page_content=content,
                    metadata=doc_metadata
                )
                documents.append(document)
            
            logger.info("Extracted text from file")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {str(e)}")
            raise
