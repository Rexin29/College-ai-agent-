from typing import List, Dict, Any, Tuple
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.config import Config
from utils.logger import logger


class RAGRetriever:
    """RAG Pipeline Retriever and Response Generator"""

    def __init__(self, vector_db, llm_manager, embeddings_manager):
        """
        Initialize RAG Retriever
        
        Args:
            vector_db: ChromaVectorDB instance
            llm_manager: LLMManager instance
            embeddings_manager: EmbeddingManager instance
        """
        self.vector_db = vector_db
        self.llm = llm_manager.get_llm()
        self.embeddings = embeddings_manager.get_embedding_function()
        self.retriever = vector_db.get_retriever(k=Config.TOP_K_RESULTS)
        logger.info("RAG Retriever initialized")

    def retrieve_documents(
        self, query: str, k: int = None, metadata_filter: Dict[str, Any] = None
    ) -> List[Tuple[str, Dict[str, Any], float]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User question
            k: Number of documents to retrieve
            metadata_filter: Optional metadata filter
            
        Returns:
            List of (content, metadata, score) tuples
        """
        if k is None:
            k = Config.TOP_K_RESULTS
        
        try:
            results = self.vector_db.search_with_scores(query=query, k=k)
            formatted_results = []
            
            for doc, score in results:
                formatted_results.append((
                    doc.page_content,
                    doc.metadata,
                    score
                ))
            
            logger.info(f"Retrieved {len(formatted_results)} documents")
            return formatted_results
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []

    def generate_answer(
        self, question: str, context_docs: List[str] = None
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Generate an answer based on retrieved documents
        
        Args:
            question: User question
            context_docs: Optional pre-retrieved documents
            
        Returns:
            Tuple of (answer, sources)
        """
        try:
            # Retrieve documents if not provided
            if context_docs is None:
                retrieved = self.retrieve_documents(question)
            else:
                retrieved = context_docs
            
            if not retrieved:
                return (
                    "I couldn't find enough information in the uploaded syllabus or notes.",
                    []
                )
            
            # Format context
            context_text = self._format_context(retrieved)
            sources = self._extract_sources(retrieved)
            
            # Create prompt
            prompt_template = ChatPromptTemplate.from_template(
                """
                You are an expert College Academic Assistant. Answer questions based ONLY on the provided syllabus and notes.
                
                If the answer is not found in the provided materials, respond with: "I couldn't find enough information in the uploaded syllabus or notes."
                
                Provide clear, detailed explanations with:
                - Step-by-step breakdowns for technical topics
                - Simple language explanations of concepts
                - Examples from the materials when available
                - Relevant section references
                
                Retrieved Context from Syllabus/Notes:
                {context}
                
                Question: {question}
                
                Answer:
                """
            )
            
            chain = prompt_template | self.llm | StrOutputParser()
            answer = chain.invoke({"context": context_text, "question": question})
            
            logger.info(f"Generated answer for question: {question}")
            return answer, sources
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return f"Error generating answer: {str(e)}", []

    def _format_context(self, retrieved_docs: List[Tuple]) -> str:
        """
        Format retrieved documents for the LLM prompt
        
        Args:
            retrieved_docs: Retrieved document tuples
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for i, (content, metadata, score) in enumerate(retrieved_docs, 1):
            source = metadata.get("file_name", "Unknown")
            page = metadata.get("page_number", "N/A")
            context_parts.append(
                f"[Source {i}: {source} (Page {page})\nConfidence: {score:.2f}]\n{content}\n"
            )
        
        return "\n---\n".join(context_parts)

    def _extract_sources(self, retrieved_docs: List[Tuple]) -> List[Dict[str, Any]]:
        """
        Extract source information from retrieved documents
        
        Args:
            retrieved_docs: Retrieved document tuples
            
        Returns:
            List of source metadata
        """
        sources = []
        for content, metadata, score in retrieved_docs:
            source_info = {
                "file_name": metadata.get("file_name"),
                "page_number": metadata.get("page_number"),
                "department": metadata.get("department"),
                "year": metadata.get("year"),
                "semester": metadata.get("semester"),
                "subject": metadata.get("subject"),
                "upload_date": metadata.get("upload_date"),
                "confidence_score": round(score, 2)
            }
            sources.append(source_info)
        
        return sources

    def rag_pipeline(
        self, question: str, metadata_filter: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Complete RAG pipeline: question -> retrieval -> generation
        
        Args:
            question: User question
            metadata_filter: Optional metadata filter
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            # Retrieve relevant documents
            retrieved_docs = self.retrieve_documents(
                question, metadata_filter=metadata_filter
            )
            
            if not retrieved_docs:
                return {
                    "answer": "I couldn't find enough information in the uploaded syllabus or notes.",
                    "sources": [],
                    "query": question,
                    "status": "no_results"
                }
            
            # Generate answer
            answer, sources = self.generate_answer(question, retrieved_docs)
            
            return {
                "answer": answer,
                "sources": sources,
                "query": question,
                "status": "success",
                "num_sources": len(sources)
            }
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {str(e)}")
            return {
                "answer": f"Error processing query: {str(e)}",
                "sources": [],
                "query": question,
                "status": "error"
            }
