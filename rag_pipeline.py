"""
Pipeline RAG (Retrieval-Augmented Generation) otimizado para deploy no Render
Usa OpenAI embeddings em vez de SentenceTransformers para evitar dependência do PyTorch
"""

import os
import logging
import openai
from typing import List, Dict, Any, Optional
from backend.rag_service_openai import RAGService

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Pipeline RAG principal para o chatbot"""
    
    def __init__(self):
        self.rag_service = None
        self.openai_client = None
        self.is_initialized = False
        
        # Configurações
        self.openai_api_key = os.getenv('OPENROUTER_API_KEY')
        self.openai_base_url = "https://openrouter.ai/api/v1"
        self.chat_model = "anthropic/claude-3.5-sonnet"
        
        self._initialize()
    
    def _initialize(self):
        """Inicializa o pipeline RAG"""
        try:
            logger.info("Inicializando RAG Pipeline...")
            
            # Inicializa RAG Service
            self.rag_service = RAGService()
            
            # Configura cliente OpenAI para chat
            self.openai_client = openai.OpenAI(
                api_key=self.openai_api_key,
                base_url=self.openai_base_url
            )
            
            if self.rag_service.is_initialized:
                self.is_initialized = True
                logger.info("RAG Pipeline inicializado com sucesso!")
            else:
                logger.error("Falha na inicialização do RAG Service")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar RAG Pipeline: {str(e)}")
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Adiciona documentos à base de conhecimento"""
        try:
            if not self.is_initialized:
                logger.error("Pipeline não inicializado")
                return False
            
            return self.rag_service.add_documents(documents)
            
        except Exception as e:
            logger.error(f"Erro ao adicionar documentos: {str(e)}")
            return False
    
    def search_context(self, query: str, max_context_length: int = 2000) -> str:
        """Busca contexto relevante para a query"""
        try:
            if not self.is_initialized:
                logger.error("Pipeline não inicializado")
                return "Pipeline não inicializado."
            
            return self.rag_service.get_context(query, max_context_length)
            
        except Exception as e:
            logger.error(f"Erro na busca de contexto: {str(e)}")
            return "Erro ao buscar contexto."
    
    def generate_response(self, query: str, persona: str = "professor") -> str:
        """Gera resposta usando RAG + LLM"""
        try:
            if not self.is_initialized:
                return "❌ Sistema não inicializado. Verifique as configurações."
            
            # Busca contexto relevante
            context = self.search_context(query)
            
            # Define persona
            if persona.lower() == "amigavel":
                system_prompt = """Você é Gá, um assistente amigável e acessível especializado em roteiro de dispensação farmacêutica. 
                
Características:
- Use linguagem simples e acessível
- Seja empático e acolhedor
- Use emojis quando apropriado
- Explique termos técnicos de forma clara
- Mantenha tom conversacional e amigável

Responda sempre em português brasileiro."""
            else:
                system_prompt = """Você é Dr. Gasnelio, um professor especialista em roteiro de dispensação farmacêutica.

Características:
- Use linguagem técnica e acadêmica
- Seja preciso e detalhado
- Cite evidências quando possível
- Mantenha tom professoral e educativo
- Forneça explicações aprofundadas

Responda sempre em português brasileiro."""
            
            # Monta prompt com contexto
            user_prompt = f"""Contexto relevante:
{context}

Pergunta do usuário: {query}

Por favor, responda baseando-se no contexto fornecido. Se a informação não estiver no contexto, indique isso claramente."""
            
            # Gera resposta
            response = self.openai_client.chat.completions.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            logger.info(f"Resposta gerada para query: {query[:50]}...")
            
            return answer
            
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}")
            return f"❌ Erro ao gerar resposta: {str(e)}"
    
    def reset_knowledge_base(self) -> bool:
        """Reseta a base de conhecimento"""
        try:
            if not self.is_initialized:
                return False
            
            return self.rag_service.reset_collection()
            
        except Exception as e:
            logger.error(f"Erro ao resetar base: {str(e)}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do pipeline"""
        return {
            "initialized": self.is_initialized,
            "rag_service_ready": self.rag_service.is_initialized if self.rag_service else False,
            "openai_configured": bool(self.openai_client),
            "model": self.chat_model
        }


# Função de conveniência para criar instância global
_pipeline_instance = None

def get_rag_pipeline() -> RAGPipeline:
    """Retorna instância singleton do pipeline RAG"""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = RAGPipeline()
    return _pipeline_instance


if __name__ == "__main__":
    # Teste básico
    logging.basicConfig(level=logging.INFO)
    
    pipeline = RAGPipeline()
    
    if pipeline.is_initialized:
        print("✅ RAG Pipeline inicializado com sucesso!")
        
        # Teste de busca
        context = pipeline.search_context("O que é roteiro de dispensação?")
        print(f"Contexto encontrado: {context[:100]}...")
        
        # Teste de geração
        response = pipeline.generate_response("O que é roteiro de dispensação?", "professor")
        print(f"Resposta gerada: {response[:100]}...")
        
    else:
        print("❌ Falha na inicialização do RAG Pipeline")

