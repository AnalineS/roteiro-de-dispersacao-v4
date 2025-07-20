"""
Serviço RAG (Retrieval-Augmented Generation) para recuperação de contexto
"""

import os
import logging
import pickle
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

logger = logging.getLogger(__name__)

class RAGService:
    """Serviço de recuperação de informações da base de conhecimento"""
    
    def __init__(self):
        self.embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embedding_model = None
        self.faiss_index = None
        self.documents = []
        self.is_initialized = False
        
        # Caminhos dos arquivos
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.index_path = os.path.join(self.data_dir, 'faiss_index.bin')
        self.docs_path = os.path.join(self.data_dir, 'documents.pkl')
        
        # Inicializa o serviço
        self._initialize()
    
    def _initialize(self):
        """Inicializa o modelo de embeddings e carrega índice se existir"""
        try:
            logger.info("Inicializando RAG Service...")
            
            # Carrega modelo de embeddings
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            logger.info(f"Modelo de embeddings carregado: {self.embedding_model_name}")
            
            # Tenta carregar índice existente
            if self._load_existing_index():
                logger.info("Índice FAISS carregado com sucesso")
                self.is_initialized = True
            else:
                logger.warning("Nenhum índice encontrado. Execute build_index() primeiro.")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar RAG Service: {str(e)}")
    
    def _load_existing_index(self) -> bool:
        """Carrega índice FAISS e documentos existentes"""
        try:
            if os.path.exists(self.index_path) and os.path.exists(self.docs_path):
                # Carrega índice FAISS
                self.faiss_index = faiss.read_index(self.index_path)
                
                # Carrega documentos
                with open(self.docs_path, 'rb') as f:
                    self.documents = pickle.load(f)
                
                logger.info(f"Carregados {len(self.documents)} documentos")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro ao carregar índice existente: {str(e)}")
            return False
    
    def build_index(self, documents: List[str]) -> bool:
        """
        Constrói o índice FAISS a partir de uma lista de documentos
        
        Args:
            documents: Lista de strings (chunks da tese)
        """
        try:
            logger.info(f"Construindo índice para {len(documents)} documentos...")
            
            if not self.embedding_model:
                raise Exception("Modelo de embeddings não inicializado")
            
            # Gera embeddings para todos os documentos
            embeddings = self.embedding_model.encode(documents, show_progress_bar=True)
            
            # Cria índice FAISS
            dimension = embeddings.shape[1]
            self.faiss_index = faiss.IndexFlatIP(dimension)  # Inner Product (cosine similarity)
            
            # Normaliza embeddings para usar cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Adiciona embeddings ao índice
            self.faiss_index.add(embeddings.astype('float32'))
            
            # Salva documentos
            self.documents = documents
            
            # Persiste índice e documentos
            self._save_index()
            
            self.is_initialized = True
            logger.info("Índice FAISS construído e salvo com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao construir índice: {str(e)}")
            return False
    
    def _save_index(self):
        """Salva índice FAISS e documentos no disco"""
        try:
            # Cria diretório se não existir
            os.makedirs(self.data_dir, exist_ok=True)
            
            # Salva índice FAISS
            faiss.write_index(self.faiss_index, self.index_path)
            
            # Salva documentos
            with open(self.docs_path, 'wb') as f:
                pickle.dump(self.documents, f)
                
        except Exception as e:
            logger.error(f"Erro ao salvar índice: {str(e)}")
            raise
    
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
            query_embedding = self.embedding_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Busca documentos similares
            scores, indices = self.faiss_index.search(
                query_embedding.astype('float32'), top_k
            )
            
            # Recupera documentos relevantes
            relevant_docs = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.documents) and score > 0.1:  # Threshold mínimo
                    relevant_docs.append(self.documents[idx])
            
            if not relevant_docs:
                return "Não encontrei informações específicas sobre sua pergunta na base de conhecimento."
            
            # Concatena contexto
            context = "\n\n".join(relevant_docs)
            
            logger.info(f"Recuperados {len(relevant_docs)} documentos relevantes")
            return context
            
        except Exception as e:
            logger.error(f"Erro ao recuperar contexto: {str(e)}")
            return "Erro ao acessar base de conhecimento."
    
    def is_ready(self) -> bool:
        """Verifica se o serviço está pronto para uso"""
        return (self.is_initialized and 
                self.embedding_model is not None and 
                self.faiss_index is not None and 
                len(self.documents) > 0)
    
    def get_stats(self) -> dict:
        """Retorna estatísticas do índice"""
        if not self.is_ready():
            return {"status": "not_ready"}
        
        return {
            "status": "ready",
            "total_documents": len(self.documents),
            "index_size": self.faiss_index.ntotal,
            "embedding_dimension": self.faiss_index.d,
            "model_name": self.embedding_model_name
        }

