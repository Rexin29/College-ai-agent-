import os
import uuid
from typing import List, Dict, Any
from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.config import Config
from utils.logger import logger


class ChromaVectorDB:
    """ChromaDB Vector Database Manager"""

    def __init__(self, embeddings):
        """
        Initialize ChromaDB
        
        Args:
            embeddings: Embedding function from LangChain
        """
        self.embeddings = embeddings
        self.db_path = Config.VECTOR_DB_PATH
        self.collection_name = Config.COLLECTION_NAME
        
        # Initialize Chroma
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.db_path,
            embedding_function=embeddings,
        )
        logger.info(f"ChromaDB initialized at {self.db_path}")

    def add_documents(
        self, documents: List[Document], ids: List[str] = None
    ) -> List[str]:
        """
        Add documents to vector database
        
        Args:
            documents: List of Document objects
            ids: Optional list of document IDs
            
        Returns:
            List of added document IDs
        """
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        try:
            self.vector_store.add_documents(documents=documents, ids=ids)
            logger.info(f"Added {len(documents)} documents to vector DB")
            return ids
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise

    def search(
        self, query: str, k: int = None, filter_dict: Dict[str, Any] = None
    ) -> List[Document]:
        """
        Search for documents in vector database
        
        Args:
            query: Search query
            k: Number of results (default from config)
            filter_dict: Metadata filters
            
        Returns:
            List of relevant documents
        """
        if k is None:
            k = Config.TOP_K_RESULTS
        
        try:
            if filter_dict:
                results = self.vector_store.similarity_search(
                    query=query, k=k, filter=filter_dict
                )
            else:
                results = self.vector_store.similarity_search(query=query, k=k)
            
            logger.info(f"Found {len(results)} documents for query: {query}")
            return results
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise

    def search_with_scores(
        self, query: str, k: int = None
    ) -> List[tuple]:
        """
        Search with similarity scores
        
        Args:
            query: Search query
            k: Number of results
            
        Returns:
            List of (document, score) tuples
        """
        if k is None:
            k = Config.TOP_K_RESULTS
        
        try:
            results = self.vector_store.similarity_search_with_score(
                query=query, k=k
            )
            logger.info(f"Found {len(results)} documents with scores")
            return results
        except Exception as e:
            logger.error(f"Error searching with scores: {str(e)}")
            raise

    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from vector database
        
        Args:
            doc_id: Document ID to delete
            
        Returns:
            True if successful
        """
        try:
            self.vector_store.delete(ids=[doc_id])
            logger.info(f"Deleted document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise

    def delete_by_metadata(self, metadata_filter: Dict[str, Any]) -> bool:
        """
        Delete documents by metadata filter
        
        Args:
            metadata_filter: Metadata filter
            
        Returns:
            True if successful
        """
        try:
            # Get all documents matching the filter
            docs = self.vector_store.get(where=metadata_filter)
            if docs["ids"]:
                self.vector_store.delete(ids=docs["ids"])
                logger.info(f"Deleted {len(docs['ids'])} documents by metadata")
            return True
        except Exception as e:
            logger.error(f"Error deleting by metadata: {str(e)}")
            raise

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Get all documents from vector database
        
        Returns:
            List of documents with metadata
        """
        try:
            docs = self.vector_store.get()
            logger.info(f"Retrieved {len(docs['ids'])} documents")
            return docs
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise

    def get_retriever(self, k: int = None):
        """
        Get a retriever object for use in RAG chain
        
        Args:
            k: Number of results
            
        Returns:
            LangChain retriever
        """
        if k is None:
            k = Config.TOP_K_RESULTS
        
        return self.vector_store.as_retriever(search_kwargs={"k": k})

    def clear_database(self) -> bool:
        """
        Clear all documents from vector database
        
        Returns:
            True if successful
        """
        try:
            docs = self.vector_store.get()
            if docs["ids"]:
                self.vector_store.delete(ids=docs["ids"])
            logger.info("Cleared vector database")
            return True
        except Exception as e:
            logger.error(f"Error clearing database: {str(e)}")
            raise
