"""
Serviço RAG (Retrieval-Augmented Generation) para recuperação de contexto usando Astra DB
"""

import os
import logging
from typing import List
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class RAGService:
    """Serviço de recuperação de informações da base de conhecimento usando Astra DB"""
    
    def __init__(self):
        self.embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embedding_model = None
        self.astra_client = None
        self.collection = None
        self.is_initialized = False
        
        # Configurações Astra DB
        self.astra_db_token = os.getenv('ASTRA_DB_TOKEN')
        self.astra_db_endpoint = os.getenv('ASTRA_DB_ENDPOINT')
        self.astra_db_keyspace = os.getenv('ASTRA_DB_KEYSPACE', 'roteiro_dispersacao_bot')
        self.collection_name = "knowledge_base"
        
        # Inicializa o serviço
        self._initialize()
    
    def _initialize(self):
        """Inicializa o modelo de embeddings e conecta ao Astra DB"""
        try:
            logger.info("Inicializando RAG Service com Astra DB...")
            
            # Carrega modelo de embeddings
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            logger.info(f"Modelo de embeddings carregado: {self.embedding_model_name}")
            
            # Conecta ao Astra DB
            if self._connect_astra_db():
                logger.info("Conexão com Astra DB estabelecida")
                self.is_initialized = True
            else:
                logger.warning("Falha na conexão com Astra DB")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar RAG Service: {str(e)}")
    
    def _connect_astra_db(self) -> bool:
        """Conecta ao Astra DB"""
        try:
            if not all([self.astra_db_token, self.astra_db_endpoint]):
                logger.error("Credenciais do Astra DB não configuradas")
                return False
            
            # Importa bibliotecas do Astra DB
            try:
                from astrapy.db import AstraDB
                from astrapy.collection import AstraDBCollection
            except ImportError:
                logger.error("Bibliotecas do Astra DB não instaladas (astrapy)")
                return False
            
            # Inicializa cliente Astra DB
            self.astra_client = AstraDB(
                token=self.astra_db_token,
                api_endpoint=self.astra_db_endpoint,
                namespace=self.astra_db_keyspace
            )
            
            # Cria ou obtém a coleção
            try:
                # Tenta criar a coleção (se não existir)
                self.collection = self.astra_client.create_collection(
                    collection_name=self.collection_name,
                    dimension=384,  # Dimensão do modelo all-MiniLM-L6-v2
                    metric="cosine"
                )
                logger.info(f"Coleção '{self.collection_name}' criada")
            except Exception:
                # Se já existir, apenas obtém a referência
                self.collection = AstraDBCollection(
                    collection_name=self.collection_name,
                    astra_db=self.astra_client
                )
                logger.info(f"Coleção '{self.collection_name}' encontrada")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao conectar com Astra DB: {str(e)}")
            return False
    
    def build_index(self, documents: List[str]) -> bool:
        """
        Constrói o índice no Astra DB a partir de uma lista de documentos
        
        Args:
            documents: Lista de strings (chunks da tese)
        """
        try:
            logger.info(f"Construindo índice no Astra DB para {len(documents)} documentos...")
            
            if not self.is_ready():
                raise Exception("Serviço RAG não inicializado corretamente")
            
            # Gera embeddings para todos os documentos
            logger.info("Gerando embeddings...")
            embeddings = self.embedding_model.encode(documents, show_progress_bar=True)
            
            # Prepara documentos para inserção no Astra DB
            documents_to_insert = []
            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                doc_data = {
                    "_id": f"doc_{i}",
                    "content": doc,
                    "$vector": embedding.tolist(),
                    "metadata": {
                        "chunk_id": i,
                        "length": len(doc),
                        "source": "tese_doutorado"
                    }
                }
                documents_to_insert.append(doc_data)
            
            # Insere documentos no Astra DB em lotes
            batch_size = 20  # Astra DB recomenda lotes pequenos
            for i in range(0, len(documents_to_insert), batch_size):
                batch = documents_to_insert[i:i + batch_size]
                
                try:
                    self.collection.insert_many(batch)
                    logger.info(f"Lote {i//batch_size + 1} inserido: {len(batch)} documentos")
                except Exception as e:
                    logger.error(f"Erro ao inserir lote {i//batch_size + 1}: {str(e)}")
                    # Continua com próximo lote
            
            logger.info("Índice Astra DB construído com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao construir índice: {str(e)}")
            return False
    
    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """
        Recupera contexto relevante para uma consulta
        
        Args:
            query: Pergunta do usuário
            top_k: Número de documentos mais relevantes a retornar
            
        Returns:
            String com contexto concatenado
        """
        try:
            if not self.is_ready():
                return "Base de conhecimento não disponível no momento."
            
            # Gera embedding da consulta
            query_embedding = self.embedding_model.encode([query])[0]
            
            # Busca documentos similares no Astra DB
            results = self.collection.vector_find(
                vector=query_embedding.tolist(),
                limit=top_k,
                fields=["content", "metadata"]
            )
            
            # Extrai documentos relevantes
            relevant_docs = []
            for result in results:
                content = result.get("content", "")
                if content.strip():
                    relevant_docs.append(content)
            
            if not relevant_docs:
                return "Não encontrei informações específicas sobre sua pergunta na base de conhecimento."
            
            # Concatena contexto
            context = "\n\n".join(relevant_docs)
            
            logger.info(f"Recuperados {len(relevant_docs)} documentos relevantes do Astra DB")
            return context
            
        except Exception as e:
            logger.error(f"Erro ao recuperar contexto: {str(e)}")
            return "Erro ao acessar base de conhecimento."
    
    def is_ready(self) -> bool:
        """Verifica se o serviço está pronto para uso"""
        return (self.is_initialized and 
                self.embedding_model is not None and 
                self.astra_client is not None and
                self.collection is not None)
    
    def get_stats(self) -> dict:
        """Retorna estatísticas do índice"""
        if not self.is_ready():
            return {"status": "not_ready"}
        
        try:
            # Tenta obter estatísticas da coleção
            stats = self.collection.find_one({}, projection={"_id": 1})
            
            return {
                "status": "ready",
                "database": "Astra DB",
                "collection": self.collection_name,
                "keyspace": self.astra_db_keyspace,
                "embedding_model": self.embedding_model_name,
                "embedding_dimension": 384,
                "connected": True
            }
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {str(e)}")
            return {
                "status": "ready",
                "database": "Astra DB",
                "collection": self.collection_name,
                "keyspace": self.astra_db_keyspace,
                "embedding_model": self.embedding_model_name,
                "embedding_dimension": 384,
                "connected": False,
                "error": str(e)
            }
    
    def clear_collection(self) -> bool:
        """Limpa todos os documentos da coleção"""
        try:
            if not self.is_ready():
                return False
            
            # Remove todos os documentos
            self.collection.delete_many({})
            logger.info("Coleção limpa com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao limpar coleção: {str(e)}")
            return False

