"""
Módulo de conexão e operações com Astra DB
"""
import os
from typing import List, Dict, Any, Optional
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from astrapy import DataAPIClient
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class AstraDBConnection:
    """Classe para gerenciar conexão com Astra DB"""
    
    def __init__(self):
        self.client = None
        self.database = None
        self.collection = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Inicializa a conexão com Astra DB"""
        try:
            if not settings.ASTRA_DB_TOKEN:
                raise ValueError("ASTRA_DB_TOKEN não configurado")
            
            # Inicializar cliente da API
            self.client = DataAPIClient(settings.ASTRA_DB_TOKEN)
            
            # Conectar ao banco de dados
            self.database = self.client.get_database_by_api_endpoint(
                settings.ASTRA_DB_API_ENDPOINT
            )
            
            # Conectar à coleção (será criada se não existir)
            self.collection = self.database.get_collection("chat_history")
            
            logger.info("Conexão com Astra DB estabelecida com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao conectar com Astra DB: {e}")
            raise
    
    def save_chat_message(self, session_id: str, message: str, response: str, 
                         persona: str = "Dr. Gasnelio") -> bool:
        """Salva uma mensagem de chat no banco"""
        try:
            document = {
                "session_id": session_id,
                "message": message,
                "response": response,
                "persona": persona,
                "timestamp": {"$date": {"$numberLong": str(int(time.time() * 1000))}}
            }
            
            result = self.collection.insert_one(document)
            return result.acknowledged
            
        except Exception as e:
            logger.error(f"Erro ao salvar mensagem: {e}")
            return False
    
    def get_chat_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recupera histórico de chat de uma sessão"""
        try:
            cursor = self.collection.find(
                {"session_id": session_id},
                sort={"timestamp": -1},
                limit=limit
            )
            
            return list(cursor)
            
        except Exception as e:
            logger.error(f"Erro ao recuperar histórico: {e}")
            return []
    
    def save_document_chunk(self, chunk_id: str, content: str, 
                           embedding: List[float], metadata: Dict[str, Any]) -> bool:
        """Salva um chunk de documento com embedding"""
        try:
            document = {
                "chunk_id": chunk_id,
                "content": content,
                "embedding": embedding,
                "metadata": metadata,
                "created_at": {"$date": {"$numberLong": str(int(time.time() * 1000))}}
            }
            
            # Usar coleção específica para documentos
            docs_collection = self.database.get_collection("document_chunks")
            result = docs_collection.insert_one(document)
            
            return result.acknowledged
            
        except Exception as e:
            logger.error(f"Erro ao salvar chunk: {e}")
            return False
    
    def search_similar_chunks(self, query_embedding: List[float], 
                             limit: int = 5) -> List[Dict[str, Any]]:
        """Busca chunks similares usando embedding"""
        try:
            docs_collection = self.database.get_collection("document_chunks")
            
            # Busca por similaridade (implementação básica)
            # Em produção, usar busca vetorial otimizada
            cursor = docs_collection.find({}, limit=limit)
            
            return list(cursor)
            
        except Exception as e:
            logger.error(f"Erro na busca de chunks: {e}")
            return []


# Instância global da conexão
db_connection = None

def get_db_connection() -> AstraDBConnection:
    """Retorna instância da conexão com banco"""
    global db_connection
    if db_connection is None:
        db_connection = AstraDBConnection()
    return db_connection

