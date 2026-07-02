import os
from typing import List, Dict, Any
from pathlib import Path
from langchain_core.documents import Document
from utils.logger import logger
from .base_processor import BaseProcessor


class CSVProcessor(BaseProcessor):
    """Process CSV files and extract structured data"""

    def process(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Process CSV file
        
        Args:
            file_path: Path to CSV file
            metadata: Optional metadata dictionary
            
        Returns:
            List of Document objects
        """
        documents = []
        metadata = metadata or {}
        
        try:
            import pandas as pd
            
            logger.info(f"Processing CSV: {file_path}")
            
            df = pd.read_csv(file_path)
            
            for idx, row in df.iterrows():
                content = " | ".join([f"{col}: {val}" for col, val in row.items()])
                
                if content.strip():
                    doc_metadata = {
                        **metadata,
                        "row_number": idx + 1,
                        "source": Path(file_path).name,
                    }
                    
                    doc = Document(
                        page_content=content,
                        metadata=doc_metadata
                    )
                    documents.append(doc)
            
            logger.info(f"Extracted {len(documents)} rows from CSV")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing CSV {file_path}: {str(e)}")
            raise
