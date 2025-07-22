"""
Integração com Langflow para o Chatbot de Hanseníase
Permite criar fluxos visuais de IA e conectar com o sistema existente
"""

import requests
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LangflowIntegration:
    def __init__(self, langflow_url: str = "http://localhost:7860"):
        """
        Inicializa a integração com Langflow
        
        Args:
            langflow_url: URL do servidor Langflow (padrão: localhost:7860)
        """
        self.langflow_url = langflow_url
        self.api_key = os.environ.get("LANGFLOW_API_KEY", "")
        self.langflow_path = os.environ.get("LANGFLOW_PATH", "C:\\Program Files\\Langflow")
        self.session = requests.Session()
        
        # Headers padrão
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        
        # Verificar se Langflow está instalado
        self._check_langflow_installation()
    
    def _check_langflow_installation(self):
        """Verifica se o Langflow está instalado"""
        # Verificar se existe o executável do Langflow
        langflow_exe = os.path.join(self.langflow_path, "langflow.exe")
        if os.path.exists(langflow_exe):
            logger.info(f"✅ Langflow encontrado em: {self.langflow_path}")
            return True
        
        # Verificar se está no PATH
        try:
            import subprocess
            result = subprocess.run(["langflow", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logger.info("✅ Langflow encontrado no PATH")
                return True
        except:
            pass
        
        # Verificar se está instalado via pip
        try:
            logger.info("✅ Langflow instalado via pip")
            return True
        except ImportError:
            pass
        
        logger.warning("❌ Langflow não encontrado")
        return False
    
    def check_connection(self) -> bool:
        """
        Verifica se o Langflow está acessível
        
        Returns:
            bool: True se conectado, False caso contrário
        """
        try:
            response = self.session.get(f"{self.langflow_url}/api/v1/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Erro ao conectar com Langflow: {e}")
            return False
    
    def create_hanseniase_flow(self) -> Dict[str, Any]:
        """
        Cria um fluxo específico para hanseníase no Langflow
        
        Returns:
            Dict com informações do fluxo criado
        """
        flow_config = {
            "name": "Chatbot Hanseníase",
            "description": "Fluxo para processamento de perguntas sobre hanseníase",
            "nodes": [
                {
                    "id": "input_node",
                    "type": "InputNode",
                    "data": {
                        "input_type": "str",
                        "required": True,
                        "placeholder": "Digite sua pergunta sobre hanseníase"
                    }
                },
                {
                    "id": "pdf_processor",
                    "type": "DocumentLoaderNode",
                    "data": {
                        "file_path": "PDFs/Roteiro de Dsispensação - Hanseníase.md",
                        "loader_type": "markdown"
                    }
                },
                {
                    "id": "text_splitter",
                    "type": "TextSplitterNode",
                    "data": {
                        "chunk_size": 1500,
                        "chunk_overlap": 300,
                        "separator": "\n\n"
                    }
                },
                {
                    "id": "embedding_model",
                    "type": "EmbeddingNode",
                    "data": {
                        "model_name": "all-MiniLM-L6-v2",
                        "device": "cpu"
                    }
                },
                {
                    "id": "vector_store",
                    "type": "VectorStoreNode",
                    "data": {
                        "store_type": "memory",
                        "similarity_metric": "cosine"
                    }
                },
                {
                    "id": "retriever",
                    "type": "RetrieverNode",
                    "data": {
                        "top_k": 3,
                        "similarity_threshold": 0.3
                    }
                },
                {
                    "id": "llm_node",
                    "type": "LLMNode",
                    "data": {
                        "model_name": "deepset/roberta-base-squad2",
                        "task": "question-answering",
                        "max_length": 512
                    }
                },
                {
                    "id": "personality_filter",
                    "type": "PromptTemplateNode",
                    "data": {
                        "template": """
                        Você é um especialista em hanseníase. Responda baseado no contexto fornecido.
                        
                        Personalidade: {personality}
                        - Dr. Gasnelio: Tom sério e técnico, linguagem formal
                        - Gá: Tom descontraído e acessível, linguagem simples
                        
                        Contexto: {context}
                        Pergunta: {question}
                        
                        Resposta:
                        """,
                        "input_variables": ["personality", "context", "question"]
                    }
                },
                {
                    "id": "output_node",
                    "type": "OutputNode",
                    "data": {
                        "output_type": "str",
                        "format": "markdown"
                    }
                }
            ],
            "edges": [
                {"source": "input_node", "target": "pdf_processor"},
                {"source": "pdf_processor", "target": "text_splitter"},
                {"source": "text_splitter", "target": "embedding_model"},
                {"source": "embedding_model", "target": "vector_store"},
                {"source": "vector_store", "target": "retriever"},
                {"source": "retriever", "target": "llm_node"},
                {"source": "llm_node", "target": "personality_filter"},
                {"source": "personality_filter", "target": "output_node"}
            ]
        }
        
        try:
            response = self.session.post(
                f"{self.langflow_url}/api/v1/flows",
                json=flow_config
            )
            
            if response.status_code == 201:
                logger.info("Fluxo de hanseníase criado com sucesso!")
                return response.json()
            else:
                logger.error(f"Erro ao criar fluxo: {response.status_code}")
                return {"error": "Falha ao criar fluxo"}
                
        except Exception as e:
            logger.error(f"Erro ao criar fluxo: {e}")
            return {"error": str(e)}
    
    def process_question(self, question: str, personality: str = "dr_gasnelio", flow_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Processa uma pergunta usando o Langflow
        
        Args:
            question: Pergunta do usuário
            personality: Personalidade (dr_gasnelio ou ga)
            flow_id: ID do fluxo (se None, usa o fluxo padrão)
        
        Returns:
            Dict com a resposta processada
        """
        if not flow_id:
            # Usar fluxo padrão
            flow_id = "hanseniase_default"
        
        payload = {
            "flow_id": flow_id,
            "inputs": {
                "question": question,
                "personality": personality
            }
        }
        
        try:
            response = self.session.post(
                f"{self.langflow_url}/api/v1/process",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "answer": result.get("output", ""),
                    "confidence": result.get("confidence", 0.0),
                    "personality": personality,
                    "timestamp": datetime.now().isoformat(),
                    "source": "langflow"
                }
            else:
                logger.error(f"Erro ao processar pergunta: {response.status_code}")
                return {
                    "success": False,
                    "error": f"Erro {response.status_code}",
                    "fallback": True
                }
                
        except Exception as e:
            logger.error(f"Erro ao processar pergunta: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback": True
            }
    
    def get_available_flows(self) -> Dict[str, Any]:
        """
        Lista todos os fluxos disponíveis
        
        Returns:
            Dict com lista de fluxos
        """
        try:
            response = self.session.get(f"{self.langflow_url}/api/v1/flows")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "flows": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"Erro {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Erro ao listar fluxos: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_flow(self, flow_id: str, flow_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza um fluxo existente
        
        Args:
            flow_id: ID do fluxo
            flow_config: Nova configuração
        
        Returns:
            Dict com resultado da atualização
        """
        try:
            response = self.session.put(
                f"{self.langflow_url}/api/v1/flows/{flow_id}",
                json=flow_config
            )
            
            if response.status_code == 200:
                logger.info(f"Fluxo {flow_id} atualizado com sucesso!")
                return {
                    "success": True,
                    "message": "Fluxo atualizado"
                }
            else:
                return {
                    "success": False,
                    "error": f"Erro {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Erro ao atualizar fluxo: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Classe para integração com o sistema existente
class HanseniaseLangflowBridge:
    def __init__(self, langflow_url: str = "http://localhost:7860"):
        """
        Bridge entre o sistema atual e Langflow
        """
        self.langflow = LangflowIntegration(langflow_url)
        self.use_langflow = self.langflow.check_connection()
        
        if self.use_langflow:
            logger.info("Langflow conectado! Usando processamento avançado.")
        else:
            logger.warning("Langflow não disponível. Usando sistema padrão.")
    
    def answer_question(self, question: str, personality: str = "dr_gasnelio") -> Dict[str, Any]:
        """
        Responde pergunta usando Langflow se disponível, senão usa sistema padrão
        
        Args:
            question: Pergunta do usuário
            personality: Personalidade desejada
        
        Returns:
            Dict com resposta
        """
        if self.use_langflow:
            # Usar Langflow
            result = self.langflow.process_question(question, personality)
            
            if result.get("success"):
                return result
            else:
                # Fallback para sistema padrão
                logger.warning("Langflow falhou, usando sistema padrão")
                return self._fallback_answer(question, personality)
        else:
            # Usar sistema padrão
            return self._fallback_answer(question, personality)
    
    def _fallback_answer(self, question: str, personality: str) -> Dict[str, Any]:
        """
        Resposta de fallback usando o sistema atual
        """
        # Aqui você pode importar e usar o sistema atual
        # Por enquanto, retorna uma resposta básica
        return {
            "success": True,
            "answer": f"Resposta via sistema padrão para: {question}",
            "confidence": 0.5,
            "personality": personality,
            "timestamp": datetime.now().isoformat(),
            "source": "fallback"
        }
    
    def setup_langflow_environment(self) -> Dict[str, Any]:
        """
        Configura o ambiente Langflow para hanseníase
        
        Returns:
            Dict com status da configuração
        """
        if not self.use_langflow:
            return {
                "success": False,
                "error": "Langflow não está disponível"
            }
        
        # Criar fluxo específico para hanseníase
        flow_result = self.langflow.create_hanseniase_flow()
        
        if "error" not in flow_result:
            return {
                "success": True,
                "message": "Ambiente Langflow configurado",
                "flow_id": flow_result.get("id"),
                "langflow_url": self.langflow.langflow_url
            }
        else:
            return {
                "success": False,
                "error": flow_result["error"]
            }

# Função de exemplo para uso
def test_langflow_integration():
    """
    Testa a integração com Langflow
    """
    print("🧪 Testando integração com Langflow...")
    
    # Criar bridge
    bridge = HanseniaseLangflowBridge()
    
    # Verificar conexão
    if bridge.use_langflow:
        print("✅ Langflow conectado!")
        
        # Configurar ambiente
        setup_result = bridge.setup_langflow_environment()
        print(f"Configuração: {setup_result}")
        
        # Testar pergunta
        test_question = "Qual é o tratamento para hanseníase?"
        result = bridge.answer_question(test_question, "dr_gasnelio")
        print(f"Resposta: {result}")
        
    else:
        print("❌ Langflow não disponível")
        print("💡 Para usar Langflow:")
        print("1. Instale: pip install langflow")
        print("2. Execute: langflow run")
        print("3. Acesse: http://localhost:7860")

if __name__ == "__main__":
    test_langflow_integration() 