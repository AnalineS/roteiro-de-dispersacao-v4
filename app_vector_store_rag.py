import os
import requests
import logging
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from datetime import datetime

try:
    pass
except ImportError:
    pass

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv('.env_vector_rag')

app = Flask(__name__)

class VectorStoreRAGIntegration:
    """Integração com Vector Store RAG do Langflow"""
    
    def __init__(self):
        self.langflow_url = os.getenv('LANGFLOW_URL', 'http://localhost:7860')
        self.api_key = os.getenv('LANGFLOW_API_KEY')
        self.flow_id = None
        self.is_available = False
        self.test_connection()
    
    def test_connection(self):
        """Testa a conexão com o Langflow"""
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'} if self.api_key else {}
            response = requests.get(f'{self.langflow_url}/api/v1/health', 
                                  headers=headers, timeout=5)
            self.is_available = response.status_code == 200
            logger.info(f"✅ Langflow Vector Store RAG disponível: {self.is_available}")
        except Exception as e:
            self.is_available = False
            logger.warning(f"ℹ️ Langflow Vector Store RAG não disponível: {e}")
    
    def create_vector_store_flow(self):
        """Cria um fluxo Vector Store RAG no Langflow"""
        if not self.is_available:
            return False
            
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Dados do fluxo Vector Store RAG
            flow_data = {
                "name": "Hanseníase Vector Store RAG",
                "description": "Fluxo para perguntas sobre hanseníase usando Vector Store e RAG",
                "data": {
                    "nodes": [
                        {
                            "id": "input_node",
                            "type": "InputNode",
                            "position": {"x": 100, "y": 100},
                            "data": {"input_type": "text", "name": "Pergunta"}
                        },
                        {
                            "id": "document_loader",
                            "type": "DocumentLoaderNode",
                            "position": {"x": 300, "y": 100},
                            "data": {
                                "file_path": "PDFs/Roteiro de Dsispensação - Hanseníase.md",
                                "loader_type": "markdown"
                            }
                        },
                        {
                            "id": "text_splitter",
                            "type": "TextSplitterNode",
                            "position": {"x": 500, "y": 100},
                            "data": {
                                "chunk_size": 1000,
                                "chunk_overlap": 200
                            }
                        },
                        {
                            "id": "vector_store",
                            "type": "VectorStoreNode",
                            "position": {"x": 700, "y": 100},
                            "data": {
                                "embedding_model": "text-embedding-ada-002",
                                "store_type": "chroma"
                            }
                        },
                        {
                            "id": "retriever",
                            "type": "RetrieverNode",
                            "position": {"x": 900, "y": 100},
                            "data": {
                                "top_k": 5,
                                "search_type": "similarity"
                            }
                        },
                        {
                            "id": "llm_node",
                            "type": "LLMNode",
                            "position": {"x": 1100, "y": 100},
                            "data": {
                                "model": "gpt-3.5-turbo",
                                "temperature": 0.7,
                                "max_tokens": 500
                            }
                        },
                        {
                            "id": "output_node",
                            "type": "OutputNode",
                            "position": {"x": 1300, "y": 100},
                            "data": {"output_type": "text"}
                        }
                    ],
                    "edges": [
                        {"source": "input_node", "target": "document_loader"},
                        {"source": "document_loader", "target": "text_splitter"},
                        {"source": "text_splitter", "target": "vector_store"},
                        {"source": "vector_store", "target": "retriever"},
                        {"source": "retriever", "target": "llm_node"},
                        {"source": "llm_node", "target": "output_node"}
                    ]
                }
            }
            
            response = requests.post(f'{self.langflow_url}/api/v1/flows',
                                   headers=headers,
                                   json=flow_data,
                                   timeout=30)
            
            if response.status_code in [200, 201]:
                result = response.json()
                self.flow_id = result.get('id')
                logger.info(f"✅ Fluxo Vector Store RAG criado: {self.flow_id}")
                return True
            else:
                logger.error(f"❌ Erro ao criar fluxo: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar fluxo Vector Store RAG: {e}")
            return False
    
    def process_question(self, question):
        """Processa uma pergunta usando Vector Store RAG"""
        if not self.is_available or not self.flow_id:
            return None
            
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Dados para execução do fluxo
            execution_data = {
                "flow_id": self.flow_id,
                "input_data": {
                    "input_node": {"text": question}
                }
            }
            
            response = requests.post(f'{self.langflow_url}/api/v1/flows/{self.flow_id}/run',
                                   headers=headers,
                                   json=execution_data,
                                   timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('output', {}).get('output_node', {}).get('text', '')
            else:
                logger.error(f"❌ Erro ao executar fluxo: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar pergunta: {e}")
            return None

class SimpleChatbot:
    """Sistema simples de fallback"""
    
    def __init__(self):
        self.pdf_content = self.load_pdf()
        self.cache = {}
        logger.info(f"✅ PDF carregado: {len(self.pdf_content)} caracteres")
    
    def load_pdf(self):
        """Carrega o conteúdo do PDF"""
        try:
            pdf_path = "PDFs/Roteiro de Dsispensação - Hanseníase.md"
            if os.path.exists(pdf_path):
                with open(pdf_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return ""
        except Exception as e:
            logger.error(f"❌ Erro ao carregar PDF: {e}")
            return ""
    
    def search_simple(self, question):
        """Busca simples no conteúdo do PDF"""
        if not self.pdf_content:
            return "Desculpe, não consegui carregar o conteúdo sobre hanseníase."
        
        # Busca por palavras-chave
        keywords = question.lower().split()
        relevant_sections = []
        
        lines = self.pdf_content.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in keywords):
                relevant_sections.append(line.strip())
        
        if relevant_sections:
            return "\n".join(relevant_sections[:3])  # Retorna até 3 seções relevantes
        else:
            return "Não encontrei informações específicas sobre isso no documento. Tente reformular sua pergunta."

# Inicializar sistemas
vector_rag = VectorStoreRAGIntegration()
simple_bot = SimpleChatbot()

# Criar fluxo Vector Store RAG se disponível
if vector_rag.is_available:
    vector_rag.create_vector_store_flow()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Pergunta não fornecida'}), 400
        
        # Tentar usar Vector Store RAG primeiro
        if vector_rag.is_available:
            answer = vector_rag.process_question(question)
            if answer:
                return jsonify({
                    'answer': answer,
                    'source': 'Vector Store RAG',
                    'timestamp': datetime.now().isoformat()
                })
        
        # Fallback para sistema simples
        answer = simple_bot.search_simple(question)
        return jsonify({
            'answer': answer,
            'source': 'Sistema Simples',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro no chat: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/system-status')
def system_status():
    return jsonify({
        'vector_store_rag_active': vector_rag.is_available,
        'simple_system_active': True,
        'pdf_loaded': len(simple_bot.pdf_content) > 0,
        'cache_size': len(simple_bot.cache),
        'langflow_url': vector_rag.langflow_url,
        'flow_id': vector_rag.flow_id
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("🚀 Iniciando Chatbot de Hanseníase - Vector Store RAG...")
    print("📊 Status do sistema:")
    print(f"   - Vector Store RAG ativo: {vector_rag.is_available}")
    print(f"   - Sistema simples ativo: True")
    print(f"   - PDF carregado: {len(simple_bot.pdf_content) > 0}")
    print(f"   - Cache: {len(simple_bot.cache)} itens")
    
    if vector_rag.is_available:
        print(f"   - Langflow URL: {vector_rag.langflow_url}")
        print(f"   - Flow ID: {vector_rag.flow_id}")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 