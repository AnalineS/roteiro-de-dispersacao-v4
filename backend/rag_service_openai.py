"""
Serviço RAG (Retrieval-Augmented Generation) para recuperação de contexto usando Astra DB
Versão otimizada que usa OpenAI embeddings em vez de SentenceTransformers
"""

import os
import logging
from typing import List, Dict, Any
import openai

logger = logging.getLogger(__name__)

class RAGService:
    """Serviço de recuperação de informações da base de conhecimento usando Astra DB e OpenAI embeddings"""
    
    def __init__(self):
        self.embedding_model_name = "text-embedding-3-small"  # Modelo OpenAI mais eficiente
        self.openai_client = None
        self.astra_client = None
        self.collection = None
        self.is_initialized = False
        
        # Configurações OpenAI
        self.openai_api_key = os.getenv('OPENROUTER_API_KEY')  # Usando OpenRouter
        self.openai_base_url = "https://openrouter.ai/api/v1"
        
        # Configurações Astra DB
        self.astra_db_token = os.getenv('ASTRA_DB_TOKEN')
        self.astra_db_endpoint = os.getenv('ASTRA_DB_ENDPOINT')
        self.astra_db_keyspace = os.getenv('ASTRA_DB_KEYSPACE', 'roteiro_dispersacao_bot')
        self.collection_name = "knowledge_base"
        
        # Inicializa o serviço
        self._initialize()
    
    def _initialize(self):
        """Inicializa o cliente OpenAI e conecta ao Astra DB"""
        try:
            logger.info("Inicializando RAG Service com OpenAI embeddings...")
            
            # Configura cliente OpenAI
            self.openai_client = openai.OpenAI(
                api_key=self.openai_api_key,
                base_url=self.openai_base_url
            )
            logger.info(f"Cliente OpenAI configurado: {self.embedding_model_name}")
            
            # Conecta ao Astra DB
            if self._connect_astra_db():
                logger.info("Conexão com Astra DB estabelecida")
                self.is_initialized = True
            else:
                logger.warning("Falha na conexão com Astra DB")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar RAG Service: {str(e)}")
    
    def _connect_astra_db(self):
        """Conecta ao Astra DB"""
        try:
            if not self.astra_db_token or not self.astra_db_endpoint:
                logger.error("Credenciais do Astra DB não encontradas")
                return False
            
            from astrapy import DataAPIClient
            
            # Conecta ao Astra DB
            client = DataAPIClient(self.astra_db_token)
            database = client.get_database(self.astra_db_endpoint)
            
            # Obtém ou cria a collection
            try:
                self.collection = database.get_collection(self.collection_name)
                logger.info(f"Collection '{self.collection_name}' encontrada")
            except Exception:
                # Cria collection se não existir
                self.collection = database.create_collection(
                    self.collection_name,
                    dimension=1536,  # Dimensão do text-embedding-3-small
                    metric="cosine"
                )
                logger.info(f"Collection '{self.collection_name}' criada")
            
            self.astra_client = client
            return True
            
        except Exception as e:
            logger.error(f"Erro ao conectar com Astra DB: {str(e)}")
            return False
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Gera embeddings usando OpenAI API"""
        try:
            if not self.openai_client:
                raise Exception("Cliente OpenAI não inicializado")
            
            # Processa textos em lotes para eficiência
            embeddings = []
            batch_size = 100  # OpenAI permite até 2048 textos por request
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                
                response = self.openai_client.embeddings.create(
                    model=self.embedding_model_name,
                    input=batch
                )
                
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Erro ao gerar embeddings: {str(e)}")
            return []
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Adiciona documentos à base de conhecimento"""
        try:
            if not self.is_initialized:
                logger.error("RAG Service não inicializado")
                return False
            
            # Extrai textos dos documentos
            texts = [doc.get('content', '') for doc in documents]
            
            # Gera embeddings
            embeddings = self.get_embeddings(texts)
            
            if not embeddings:
                logger.error("Falha ao gerar embeddings")
                return False
            
            # Prepara documentos para inserção
            docs_to_insert = []
            for i, doc in enumerate(documents):
                doc_with_embedding = {
                    "_id": doc.get('id', f"doc_{i}"),
                    "content": doc.get('content', ''),
                    "metadata": doc.get('metadata', {}),
                    "$vector": embeddings[i]
                }
                docs_to_insert.append(doc_with_embedding)
            
            # Insere no Astra DB
            self.collection.insert_many(docs_to_insert)
            logger.info(f"Inseridos {len(docs_to_insert)} documentos")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao adicionar documentos: {str(e)}")
            return False
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Busca documentos relevantes para a query"""
        try:
            if not self.is_initialized:
                logger.error("RAG Service não inicializado")
                return []
            
            # Gera embedding da query
            query_embeddings = self.get_embeddings([query])
            
            if not query_embeddings:
                logger.error("Falha ao gerar embedding da query")
                return []
            
            query_vector = query_embeddings[0]
            
            # Busca no Astra DB
            results = self.collection.find(
                {},
                vector=query_vector,
                limit=top_k,
                include_similarity=True
            )
            
            # Formata resultados
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'content': result.get('content', ''),
                    'metadata': result.get('metadata', {}),
                    'similarity': result.get('$similarity', 0.0)
                })
            
            logger.info(f"Encontrados {len(formatted_results)} resultados para: {query[:50]}...")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Erro na busca: {str(e)}")
            return []
    
    def get_context(self, query: str, max_context_length: int = 2000) -> str:
        """Obtém contexto relevante para a query"""
        try:
            results = self.search(query, top_k=5)
            
            if not results:
                return "Nenhum contexto relevante encontrado."
            
            # Combina resultados em contexto
            context_parts = []
            current_length = 0
            
            for result in results:
                content = result['content']
                if current_length + len(content) <= max_context_length:
                    context_parts.append(content)
                    current_length += len(content)
                else:
                    # Adiciona parte do conteúdo se couber
                    remaining_space = max_context_length - current_length
                    if remaining_space > 100:  # Mínimo de 100 chars
                        context_parts.append(content[:remaining_space] + "...")
                    break
            
            context = "\n\n".join(context_parts)
            logger.info(f"Contexto gerado com {len(context)} caracteres")
            
            return context
            
        except Exception as e:
            logger.error(f"Erro ao obter contexto: {str(e)}")
            return "Erro ao recuperar contexto."
    
    def reset_collection(self) -> bool:
        """Reseta a collection (remove todos os documentos)"""
        try:
            if not self.collection:
                logger.error("Collection não inicializada")
                return False
            
            # Remove todos os documentos
            self.collection.delete_many({})
            logger.info("Collection resetada com sucesso")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao resetar collection: {str(e)}")
            return False


# Função de conveniência para criar instância
def create_rag_service() -> RAGService:
    """Cria e retorna uma instância do RAG Service"""
    return RAGService()


if __name__ == "__main__":
    # Teste básico
    logging.basicConfig(level=logging.INFO)
    
    rag = create_rag_service()
    
    if rag.is_initialized:
        print("✅ RAG Service inicializado com sucesso!")
        
        # Teste de embedding
        test_embeddings = rag.get_embeddings(["Teste de embedding"])
        if test_embeddings:
            print(f"✅ Embeddings funcionando! Dimensão: {len(test_embeddings[0])}")
        else:
            print("❌ Erro ao gerar embeddings")
    else:
        print("❌ Falha na inicialização do RAG Service")

