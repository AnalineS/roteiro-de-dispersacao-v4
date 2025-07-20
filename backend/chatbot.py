"""
Módulo principal do chatbot com integração RAG e OpenRouter
"""

import os
import logging
from typing import Optional, Dict, Any
from openai import OpenAI
from personas import PersonaManager
from rag_service import RAGService

logger = logging.getLogger(__name__)

class ChatbotService:
    """Serviço principal do chatbot que integra RAG, personas e LLM"""
    
    def __init__(self):
        self.persona_manager = PersonaManager()
        self.rag_service = RAGService()
        
        # Configuração do cliente OpenRouter
        self.openrouter_client = OpenAI(
            api_key=os.getenv('OPENROUTER_API_KEY'),
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Modelo Kimie K2
        self.model_name = "moonshot/moonshot-v1-8k"  # Kimie K2 Free
        
        logger.info("ChatbotService inicializado")
    
    def process_message(self, message: str, persona: str) -> str:
        """
        Processa uma mensagem do usuário através do pipeline completo:
        1. Recupera contexto relevante via RAG
        2. Formata prompt com persona
        3. Gera resposta via OpenRouter/Kimie K2
        """
        try:
            # 1. Recupera contexto relevante da base de conhecimento
            logger.info(f"Buscando contexto RAG para: {message[:50]}...")
            context = self.rag_service.retrieve_context(message)
            
            # 2. Formata prompt com persona e contexto
            messages = self.persona_manager.format_prompt_with_context(
                persona, message, context
            )
            
            # 3. Gera resposta via OpenRouter
            logger.info(f"Gerando resposta com persona: {persona}")
            response = self._generate_response(messages)
            
            return response
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            return self._get_error_response(persona)
    
    def _generate_response(self, messages: list) -> str:
        """Gera resposta usando OpenRouter/Kimie K2"""
        try:
            response = self.openrouter_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Erro ao chamar OpenRouter: {str(e)}")
            raise
    
    def _get_error_response(self, persona: str) -> str:
        """Retorna resposta de erro apropriada para cada persona"""
        if persona == 'dr_gasnelio':
            return ("Peço desculpas, mas encontrei dificuldades técnicas para processar "
                   "sua consulta no momento. Por favor, tente novamente em alguns instantes.")
        else:  # ga
            return ("Opa, parece que tive um probleminha técnico aqui! 😅 "
                   "Pode tentar perguntar de novo? Prometo que vou fazer o meu melhor!")
    
    def get_greeting(self, persona: str) -> str:
        """Retorna saudação da persona"""
        try:
            return self.persona_manager.get_persona_greeting(persona)
        except ValueError:
            return "Olá! Como posso ajudá-lo hoje?"
    
    def is_ready(self) -> bool:
        """Verifica se o serviço está pronto para uso"""
        try:
            # Verifica se as credenciais estão configuradas
            if not os.getenv('OPENROUTER_API_KEY'):
                logger.error("OPENROUTER_API_KEY não configurada")
                return False
            
            # Verifica se o RAG está pronto
            if not self.rag_service.is_ready():
                logger.error("RAG Service não está pronto")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao verificar status do serviço: {str(e)}")
            return False

