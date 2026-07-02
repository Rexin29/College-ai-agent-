from langchain_ollama import OllamaEmbeddings
from utils.config import Config
from utils.logger import logger


class EmbeddingManager:
    """Manages embedding generation using Ollama"""

    def __init__(self, model: str = None, base_url: str = None):
        """
        Initialize Embedding Manager
        
        Args:
            model: Embedding model name (default from config)
            base_url: Ollama base URL (default from config)
        """
        self.model = model or Config.EMBEDDING_MODEL
        self.base_url = base_url or Config.OLLAMA_BASE_URL
        
        try:
            self.embeddings = OllamaEmbeddings(
                model=self.model,
                base_url=self.base_url,
            )
            logger.info(f"Embedding manager initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Error initializing embedding manager: {str(e)}")
            raise

    def embed_text(self, text: str) -> list:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.embeddings.embed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Error embedding text: {str(e)}")
            raise

    def embed_texts(self, texts: list) -> list:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.embeddings.embed_documents(texts)
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e:
            logger.error(f"Error embedding texts: {str(e)}")
            raise

    def get_embedding_function(self):
        """Get the underlying embedding function"""
        return self.embeddings
