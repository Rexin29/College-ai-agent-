import os
from typing import List, Dict, Any
from pathlib import Path
from langchain_core.documents import Document
from utils.logger import logger
from .base_processor import BaseProcessor


class PDFProcessor(BaseProcessor):
    """Process PDF files and extract text"""

    def process(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Process PDF file
        
        Args:
            file_path: Path to PDF file
            metadata: Optional metadata dictionary
            
        Returns:
            List of Document objects
        """
        documents = []
        metadata = metadata or {}
        
        try:
            import pdfplumber
            
            logger.info(f"Processing PDF: {file_path}")
            
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    
                    if text.strip():
                        doc_metadata = {
                            **metadata,
                            "page_number": page_num,
                            "source": Path(file_path).name,
                        }
                        
                        doc = Document(
                            page_content=text,
                            metadata=doc_metadata
                        )
                        documents.append(doc)
            
            logger.info(f"Extracted {len(documents)} pages from PDF")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise
