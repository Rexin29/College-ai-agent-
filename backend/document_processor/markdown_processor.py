import os
from typing import List, Dict, Any
from pathlib import Path
from langchain_core.documents import Document
from utils.logger import logger
from .base_processor import BaseProcessor


class MarkdownProcessor(BaseProcessor):
    """Process Markdown files"""

    def process(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Process Markdown file
        
        Args:
            file_path: Path to Markdown file
            metadata: Optional metadata dictionary
            
        Returns:
            List of Document objects
        """
        documents = []
        metadata = metadata or {}
        
        try:
            logger.info(f"Processing Markdown: {file_path}")
            
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
            
            logger.info("Extracted content from Markdown file")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing Markdown {file_path}: {str(e)}")
            raise
