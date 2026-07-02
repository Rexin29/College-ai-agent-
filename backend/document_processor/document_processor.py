from typing import List, Dict, Any
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config import Config
from utils.logger import logger
from .base_processor import BaseProcessor
from .pdf_processor import PDFProcessor
from .docx_processor import DOCXProcessor
from .text_processor import TextProcessor
from .csv_processor import CSVProcessor
from .markdown_processor import MarkdownProcessor
from .pptx_processor import PPTXProcessor


class DocumentProcessor:
    """Main document processor that handles all file types"""

    def __init__(self):
        """Initialize document processor with available processors"""
        self.processors = {
            "pdf": PDFProcessor(),
            "docx": DOCXProcessor(),
            "doc": DOCXProcessor(),
            "txt": TextProcessor(),
            "md": MarkdownProcessor(),
            "csv": CSVProcessor(),
            "xlsx": CSVProcessor(),
            "pptx": PPTXProcessor(),
            "ppt": PPTXProcessor(),
        }
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        logger.info("Document processor initialized")

    def process_file(
        self, file_path: str, metadata: Dict[str, Any] = None
    ) -> List[Document]:
        """
        Process a file based on its extension
        
        Args:
            file_path: Path to file
            metadata: Optional metadata dictionary
            
        Returns:
            List of processed and chunked Document objects
        """
        file_ext = Path(file_path).suffix.lower().lstrip(".")
        metadata = metadata or {}
        
        # Add file metadata
        metadata["file_name"] = Path(file_path).name
        metadata["file_type"] = file_ext
        
        if file_ext not in self.processors:
            logger.error(f"Unsupported file type: {file_ext}")
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        try:
            # Get appropriate processor
            processor = self.processors[file_ext]
            logger.info(f"Using {processor.__class__.__name__} for {file_path}")
            
            # Process file
            documents = processor.process(file_path, metadata)
            
            # Split documents into chunks
            chunked_documents = self._chunk_documents(documents)
            
            logger.info(f"Processed {file_path}: {len(chunked_documents)} chunks")
            return chunked_documents
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            raise

    def _chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into semantic chunks
        
        Args:
            documents: List of documents
            
        Returns:
            List of chunked documents
        """
        chunked_docs = []
        
        for doc in documents:
            # Split text into chunks
            chunks = self.text_splitter.split_text(doc.page_content)
            
            for chunk in chunks:
                new_doc = Document(
                    page_content=chunk,
                    metadata=doc.metadata
                )
                chunked_docs.append(new_doc)
        
        logger.info(f"Created {len(chunked_docs)} chunks from {len(documents)} documents")
        return chunked_docs

    def process_directory(
        self, directory_path: str, metadata: Dict[str, Any] = None
    ) -> List[Document]:
        """
        Process all files in a directory
        
        Args:
            directory_path: Path to directory
            metadata: Optional metadata dictionary
            
        Returns:
            List of all processed documents
        """
        all_documents = []
        directory = Path(directory_path)
        
        if not directory.is_dir():
            logger.error(f"{directory_path} is not a directory")
            raise ValueError(f"{directory_path} is not a directory")
        
        logger.info(f"Processing directory: {directory_path}")
        
        for file_path in directory.rglob("*"):
            if file_path.is_file():
                file_ext = file_path.suffix.lower().lstrip(".")
                
                if file_ext in self.processors:
                    try:
                        docs = self.process_file(str(file_path), metadata)
                        all_documents.extend(docs)
                    except Exception as e:
                        logger.warning(f"Skipped {file_path}: {str(e)}")
        
        logger.info(f"Processed directory: {len(all_documents)} total chunks")
        return all_documents
