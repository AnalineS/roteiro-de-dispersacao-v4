"""
Configurações do sistema de chatbot com RAG
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Configurações gerais
    APP_NAME: str = "Roteiro de Dispersação Bot v4"
    APP_VERSION: str = "4.0.0"
    DEBUG: bool = False
    
    # Configurações do Astra DB
    ASTRA_DB_ID: str = "5a956831-30af-4006-89c4-7b6eab21ea07"
    ASTRA_DB_REGION: str = "us-east1"
    ASTRA_DB_KEYSPACE: str = "roteiro-dispersacao_bot"
    ASTRA_DB_TOKEN: Optional[str] = None
    ASTRA_DB_API_ENDPOINT: str = "https://5a956831-30af-4006-89c4-7b6eab21ea07-us-east1.apps.astra.datastax.com"
    
    # Configurações do OpenRouter
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # Configurações do LangFlow
    LANGFLOW_API_KEY: Optional[str] = None
    LANGFLOW_BASE_URL: str = "https://api.langflow.astra.datastax.com"
    LANGFLOW_FLOW_ID: Optional[str] = None
    
    # Configurações do modelo
    DEFAULT_MODEL: str = "anthropic/claude-3-haiku"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Configurações do RAG
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.7
    
    # Configurações do Streamlit
    STREAMLIT_PORT: int = 8501
    STREAMLIT_HOST: str = "0.0.0.0"
    
    # Configurações do Flask (para API)
    FLASK_PORT: int = 5000
    FLASK_HOST: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instância global das configurações
settings = Settings()

