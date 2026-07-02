from langchain_ollama.llms import OllamaLLM
from utils.config import Config
from utils.logger import logger


class LLMManager:
    """Manages LLM interactions using Ollama"""

    def __init__(self, model: str = None, base_url: str = None):
        """
        Initialize LLM Manager
        
        Args:
            model: LLM model name (default from config)
            base_url: Ollama base URL (default from config)
        """
        self.model = model or Config.LLM_MODEL
        self.base_url = base_url or Config.OLLAMA_BASE_URL
        
        try:
            self.llm = OllamaLLM(
                model=self.model,
                base_url=self.base_url,
                temperature=0.7,
            )
            logger.info(f"LLM manager initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Error initializing LLM manager: {str(e)}")
            raise

    def generate(self, prompt: str) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: Prompt for the LLM
            
        Returns:
            Generated response
        """
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def get_llm(self):
        """Get the underlying LLM object for use in chains"""
        return self.llm
