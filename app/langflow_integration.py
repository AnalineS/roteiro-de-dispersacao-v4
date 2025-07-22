"""
Integração com LangFlow para processamento avançado de fluxos
"""

import logging
from typing import Any, Dict, List, Optional

import requests
from config.settings import settings

logger = logging.getLogger(__name__)


class LangFlowClient:
    """Cliente para integração com LangFlow"""

    # Decisão de design: encapsular toda a comunicação com a API do LangFlow nesta classe para facilitar manutenção e testes.
    # Permite trocar a implementação do cliente sem afetar o restante do sistema.

    def __init__(self):
        self.api_key = settings.LANGFLOW_API_KEY
        self.base_url = settings.LANGFLOW_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_flow(self, flow_data: Dict[str, Any]) -> Optional[str]:
        """Cria um novo fluxo no LangFlow"""
        # Lógica complexa: chamada à API externa do LangFlow para criar fluxos customizados.
        # Decisão: tratar erros de rede e resposta inesperada, retornando None em caso de falha.
        try:
            url = f"{self.base_url}/api/v1/flows"
            response = requests.post(url, headers=self.headers, json=flow_data)

            if response.status_code == 201:
                result = response.json()
                flow_id = result.get("id")
                logger.info(f"Fluxo criado com sucesso: {flow_id}")
                return flow_id
            else:
                logger.error(f"Erro ao criar fluxo: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Erro na criação do fluxo: {e}")
            return None

    def run_flow(self, flow_id: str, inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Executa um fluxo específico com inputs fornecidos"""
        try:
            url = f"{self.base_url}/api/v1/flows/{flow_id}/run"
            payload = {"inputs": inputs, "tweaks": {}}

            response = requests.post(url, headers=self.headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                logger.info(f"Fluxo executado com sucesso: {flow_id}")
                return result
            else:
                logger.error(f"Erro ao executar fluxo: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Erro na execução do fluxo: {e}")
            return None

    def get_flow_status(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Obtém o status de um fluxo"""
        try:
            url = f"{self.base_url}/api/v1/flows/{flow_id}"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Erro ao obter status: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Erro ao obter status do fluxo: {e}")
            return None

    def list_flows(self) -> List[Dict[str, Any]]:
        """Lista todos os fluxos disponíveis"""
        try:
            url = f"{self.base_url}/api/v1/flows"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                return response.json().get("flows", [])
            else:
                logger.error(f"Erro ao listar fluxos: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            logger.error(f"Erro ao listar fluxos: {e}")
            return []


class DispersionFlowManager:
    """Gerenciador de fluxos específicos para roteiro de dispersão"""

    def __init__(self):
        self.client = LangFlowClient()
        self.flow_templates = self._get_flow_templates()

    def _get_flow_templates(self) -> Dict[str, Dict]:
        """Define templates de fluxos para diferentes cenários"""
        # Decisão de design: manter templates de fluxo como dicionário para facilitar extensão e manutenção.
        # Permite adicionar novos tipos de fluxo sem alterar a lógica principal.
        return {
            "basic_dispersion": {
                "name": "Análise Básica de Dispersão",
                "description": "Fluxo para análise básica de dispersão atmosférica",
                "nodes": [
                    {
                        "id": "input_node",
                        "type": "TextInput",
                        "data": {
                            "template": {
                                "value": "",
                                "placeholder": "Digite os parâmetros de dispersão...",
                            }
                        },
                    },
                    {
                        "id": "rag_node",
                        "type": "RAGRetriever",
                        "data": {
                            "template": {
                                "search_kwargs": {"k": 5},
                                "input_key": "query",
                            }
                        },
                    },
                    {
                        "id": "llm_node",
                        "type": "OpenAI",
                        "data": {
                            "template": {
                                "model_name": "gpt-3.5-turbo",
                                "temperature": 0.7,
                                "max_tokens": 1000,
                            }
                        },
                    },
                    {
                        "id": "output_node",
                        "type": "TextOutput",
                        "data": {"template": {"text": "{llm_output}"}},
                    },
                ],
                "edges": [
                    {"source": "input_node", "target": "rag_node"},
                    {"source": "rag_node", "target": "llm_node"},
                    {"source": "llm_node", "target": "output_node"},
                ],
            },
            "advanced_calculation": {
                "name": "Cálculos Avançados de Dispersão",
                "description": "Fluxo para cálculos complexos com múltiplos parâmetros",
                "nodes": [
                    {
                        "id": "params_input",
                        "type": "JSONInput",
                        "data": {
                            "template": {
                                "value": "{}",
                                "placeholder": "Parâmetros em JSON...",
                            }
                        },
                    },
                    {
                        "id": "validation_node",
                        "type": "PythonFunction",
                        "data": {
                            "template": {
                                "code": """
def validate_params(params):
    required = ['wind_speed', 'temperature', 'emission_rate']
    for param in required:
                        if param not in params:
                            raise ValueError(f'Parâmetro {param} é obrigatório')
                    return params
                """
                            }
                        },
                    },
                    {
                        "id": "calculation_node",
                        "type": "PythonFunction",
                        "data": {
                            "template": {
                                "code": """
def calculate_dispersion(params):
                        # Implementar cálculos de dispersão
                        wind_speed = params['wind_speed']
                        temp = params['temperature']
                        emission = params['emission_rate']
                        
                        # Fórmula simplificada de Gaussian
                        concentration = emission / (wind_speed * temp)
                        return {'concentration': concentration, 'status': 'calculated'}
                """
                            }
                        },
                    },
                    {
                        "id": "result_formatter",
                        "type": "TextOutput",
                        "data": {"template": {"text": "Resultado: {calculation_result}"}},
                    },
                ],
            },
        }

    def create_dispersion_flow(self, flow_type: str = "basic_dispersion") -> Optional[str]:
        """Cria um fluxo específico para dispersão"""
        try:
            if flow_type not in self.flow_templates:
                logger.error(f"Tipo de fluxo não encontrado: {flow_type}")
                return None

            template = self.flow_templates[flow_type]
            flow_data = {
                "name": template["name"],
                "description": template["description"],
                "data": {
                    "nodes": template["nodes"],
                    "edges": template.get("edges", []),
                },
            }

            return self.client.create_flow(flow_data)

        except Exception as e:
            logger.error(f"Erro ao criar fluxo de dispersão: {e}")
            return None

    def process_dispersion_query(self, query: str, flow_id: str = None) -> Optional[str]:
        """Processa uma consulta usando fluxo de dispersão"""
        # Lógica: se não houver flow_id, cria um novo fluxo padrão.
        # Decisão: fallback automático para garantir que sempre exista um fluxo válido.
        try:
            if not flow_id:
                # Usar fluxo padrão ou criar um novo
                flow_id = self.create_dispersion_flow("basic_dispersion")
                if not flow_id:
                    return None

            inputs = {"query": query, "context": "roteiro de dispersão atmosférica"}

            result = self.client.run_flow(flow_id, inputs)

            if result and "outputs" in result:
                return result["outputs"].get("text", "Resultado não disponível")

            return None

        except Exception as e:
            logger.error(f"Erro ao processar consulta: {e}")
            return None

    def calculate_dispersion_parameters(self, params: Dict[str, float]) -> Optional[Dict[str, Any]]:
        """Calcula parâmetros de dispersão usando fluxo avançado"""
        try:
            flow_id = self.create_dispersion_flow("advanced_calculation")
            if not flow_id:
                return None

            result = self.client.run_flow(flow_id, {"parameters": params})

            if result and "outputs" in result:
                return result["outputs"]

            return None

        except Exception as e:
            logger.error(f"Erro no cálculo de parâmetros: {e}")
            return None


# Instância global do gerenciador
flow_manager = None


def get_flow_manager() -> DispersionFlowManager:
    """Retorna instância do gerenciador de fluxos"""
    global flow_manager
    if flow_manager is None:
        flow_manager = DispersionFlowManager()
    return flow_manager
