"""
Chatbot de Hanseníase com Integração Langflow
Versão que usa Langflow quando disponível, senão usa sistema padrão
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import logging
from datetime import datetime

# Tentar importar a integração Langflow
try:
    from langflow_integration import HanseniaseLangflowBridge
    LANGFLOW_AVAILABLE = True
except ImportError:
    LANGFLOW_AVAILABLE = False
    print("⚠️ Langflow não disponível. Usando sistema padrão.")

# Importar sistema padrão como fallback
from transformers.pipelines import pipeline
import torch
from sentence_transformers import SentenceTransformer
import numpy as np

app = Flask(__name__)
CORS(app)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HanseniaseChatbotAdvanced:
    def __init__(self):
        self.use_langflow = False
        self.langflow_bridge = None
        
        # Sistema padrão (fallback)
        self.qa_pipeline = None
        self.embedding_model = None
        self.cache = {}
        self.pdf_text = ""
        self.chunks = []
        
        # Inicializar sistemas
        self._initialize_systems()
    
    def _initialize_systems(self):
        """Inicializa Langflow se disponível, senão usa sistema padrão"""
        if LANGFLOW_AVAILABLE:
            try:
                self.langflow_bridge = HanseniaseLangflowBridge()
                if self.langflow_bridge.use_langflow:
                    self.use_langflow = True
                    logger.info("✅ Langflow ativado! Usando processamento avançado.")
                    
                    # Configurar ambiente Langflow
                    setup_result = self.langflow_bridge.setup_langflow_environment()
                    if setup_result.get("success"):
                        logger.info("✅ Ambiente Langflow configurado!")
                    else:
                        logger.warning(f"⚠️ Configuração Langflow falhou: {setup_result.get('error')}")
                        self.use_langflow = False
                else:
                    logger.info("ℹ️ Langflow não disponível. Usando sistema padrão.")
            except Exception as e:
                logger.error(f"❌ Erro ao inicializar Langflow: {e}")
                self.use_langflow = False
        
        # Inicializar sistema padrão
        if not self.use_langflow:
            self._initialize_standard_system()
    
    def _initialize_standard_system(self):
        """Inicializa o sistema padrão de IA"""
        try:
            logger.info("Carregando sistema padrão...")
            
            # Carregar modelos
            self.qa_pipeline = pipeline(
                "question-answering",
                model="deepset/roberta-base-squad2",
                device=-1 if not torch.cuda.is_available() else 0
            )
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Carregar PDF
            self._load_pdf_content()
            
            logger.info("✅ Sistema padrão carregado!")
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar sistema padrão: {e}")
            raise
    
    def _load_pdf_content(self):
        """Carrega o conteúdo do PDF"""
        pdf_path = "PDFs/Roteiro de Dsispensação - Hanseníase.md"
        
        try:
            if os.path.exists(pdf_path):
                with open(pdf_path, 'r', encoding='utf-8') as file:
                    self.pdf_text = file.read()
                
                # Chunking inteligente
                self.chunks = self._chunk_text(self.pdf_text)
                logger.info(f"PDF carregado: {len(self.chunks)} chunks")
            else:
                logger.warning(f"PDF não encontrado: {pdf_path}")
                self.pdf_text = ""
                self.chunks = []
                
        except Exception as e:
            logger.error(f"Erro ao carregar PDF: {e}")
            self.pdf_text = ""
            self.chunks = []
    
    def _chunk_text(self, text, chunk_size=1500, overlap=300):
        """Divide o texto em chunks menores"""
        if not text:
            return []
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            if end > len(text):
                end = len(text)
            
            chunk = text[start:end]
            chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def answer_question(self, question: str, personality: str = "dr_gasnelio") -> dict:
        """
        Responde pergunta usando Langflow se disponível, senão usa sistema padrão
        
        Args:
            question: Pergunta do usuário
            personality: Personalidade (dr_gasnelio ou ga)
        
        Returns:
            Dict com resposta
        """
        # Verificar cache primeiro
        cache_key = f"{question}_{personality}"
        if cache_key in self.cache:
            cached_response = self.cache[cache_key]
            cached_response["source"] = "cache"
            return cached_response
        
        # Usar Langflow se disponível
        if self.use_langflow and self.langflow_bridge:
            try:
                result = self.langflow_bridge.answer_question(question, personality)
                
                if result.get("success"):
                    # Salvar no cache
                    self.cache[cache_key] = result
                    return result
                else:
                    logger.warning("Langflow falhou, usando sistema padrão")
                    
            except Exception as e:
                logger.error(f"Erro no Langflow: {e}")
        
        # Usar sistema padrão
        return self._standard_answer(question, personality)
    
    def _standard_answer(self, question: str, personality: str) -> dict:
        """Resposta usando sistema padrão"""
        try:
            # Busca semântica
            best_chunk = self._find_best_chunk(question)
            
            if best_chunk:
                # Usar modelo de question-answering
                result = self.qa_pipeline(
                    question=question,
                    context=best_chunk,
                    max_answer_len=512
                )
                
                answer = result['answer']
                confidence = result['score']
                
                # Formatar resposta baseada na personalidade
                formatted_answer = self._format_response(answer, personality, confidence)
                
                response = {
                    "success": True,
                    "answer": formatted_answer,
                    "confidence": confidence,
                    "personality": personality,
                    "timestamp": datetime.now().isoformat(),
                    "source": "standard_system",
                    "question": question
                }
                
                # Salvar no cache
                cache_key = f"{question}_{personality}"
                self.cache[cache_key] = response
                
                return response
            else:
                return self._fallback_response(question, personality)
                
        except Exception as e:
            logger.error(f"Erro no sistema padrão: {e}")
            return self._fallback_response(question, personality)
    
    def _find_best_chunk(self, question: str) -> str:
        """Encontra o chunk mais relevante para a pergunta"""
        if not self.chunks:
            return ""
        
        # Embeddings da pergunta
        question_embedding = self.embedding_model.encode([question])[0]
        
        best_chunk = ""
        best_score = 0
        
        for chunk in self.chunks:
            # Embedding do chunk
            chunk_embedding = self.embedding_model.encode([chunk])[0]
            
            # Similaridade cosseno
            similarity = np.dot(question_embedding, chunk_embedding) / (
                np.linalg.norm(question_embedding) * np.linalg.norm(chunk_embedding)
            )
            
            if similarity > best_score:
                best_score = similarity
                best_chunk = chunk
        
        # Threshold mínimo
        if best_score > 0.3:
            return best_chunk
        else:
            return ""
    
    def _format_response(self, answer: str, personality: str, confidence: float) -> str:
        """Formata a resposta baseada na personalidade"""
        if personality == "dr_gasnelio":
            return f"Dr. Gasnelio responde:\n\n{answer}\n\n*Confiança: {confidence:.2f}*"
        elif personality == "ga":
            # Simplificar linguagem para Gá
            simple_answer = self._simplify_text(answer)
            return f"Gá explica: {simple_answer} 😊"
        else:
            return answer
    
    def _simplify_text(self, text: str) -> str:
        """Simplifica o texto para o Gá"""
        replacements = {
            "dispensação": "entrega de remédios",
            "medicamentos": "remédios",
            "posologia": "como tomar",
            "administração": "como tomar",
            "reação adversa": "efeito colateral",
            "interação medicamentosa": "mistura de remédios",
            "protocolo": "guia",
            "orientação": "explicação",
            "adesão": "seguir o tratamento"
        }
        
        for complex_term, simple_term in replacements.items():
            text = text.replace(complex_term, simple_term)
        
        return text
    
    def _fallback_response(self, question: str, personality: str) -> dict:
        """Resposta de fallback quando não encontra informação"""
        if personality == "dr_gasnelio":
            answer = f"Dr. Gasnelio responde:\n\nInfelizmente não encontrei informações específicas sobre '{question}' na minha tese. Sugiro consultar um profissional de saúde para orientações mais precisas."
        else:
            answer = f"Gá explica: Opa, não encontrei isso na tese! 😅 Mas não se preocupe, um médico pode te ajudar melhor com essa pergunta."
        
        return {
            "success": True,
            "answer": answer,
            "confidence": 0.0,
            "personality": personality,
            "timestamp": datetime.now().isoformat(),
            "source": "fallback",
            "question": question
        }
    
    def get_system_info(self) -> dict:
        """Retorna informações sobre o sistema ativo"""
        return {
            "langflow_active": self.use_langflow,
            "standard_system_loaded": self.qa_pipeline is not None,
            "cache_size": len(self.cache),
            "chunks_loaded": len(self.chunks),
            "pdf_loaded": len(self.pdf_text) > 0
        }

# Instanciar chatbot
chatbot = HanseniaseChatbotAdvanced()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/tese')
def tese():
    """Página da tese"""
    return render_template('tese.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint do chat"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        question = data.get('question', '').strip()
        personality = data.get('personality', 'dr_gasnelio')
        
        if not question:
            return jsonify({"error": "Pergunta não fornecida"}), 400
        
        if personality not in ['dr_gasnelio', 'ga']:
            return jsonify({"error": "Personalidade inválida"}), 400
        
        # Processar pergunta
        response = chatbot.answer_question(question, personality)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Erro no endpoint /api/chat: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/health')
def health():
    """Health check"""
    system_info = chatbot.get_system_info()
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "system_info": system_info,
        "langflow_available": LANGFLOW_AVAILABLE
    })

@app.route('/api/info')
def info():
    """Informações da API"""
    return jsonify({
        "name": "Chatbot Hanseníase com Langflow",
        "version": "2.0.0",
        "description": "Chatbot inteligente para perguntas sobre hanseníase",
        "features": [
            "Integração com Langflow",
            "Sistema de fallback",
            "Duas personalidades",
            "Cache inteligente",
            "Busca semântica"
        ],
        "personalities": {
            "dr_gasnelio": "Tom sério e técnico",
            "ga": "Tom descontraído e acessível"
        },
        "langflow_integration": LANGFLOW_AVAILABLE
    })

@app.route('/api/system-status')
def system_status():
    """Status detalhado do sistema"""
    system_info = chatbot.get_system_info()
    
    return jsonify({
        "langflow": {
            "available": LANGFLOW_AVAILABLE,
            "active": system_info["langflow_active"]
        },
        "standard_system": {
            "loaded": system_info["standard_system_loaded"],
            "pdf_loaded": system_info["pdf_loaded"],
            "chunks": system_info["chunks_loaded"]
        },
        "cache": {
            "size": system_info["cache_size"]
        },
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Iniciando Chatbot de Hanseníase com Langflow...")
    print(f"📊 Status do sistema:")
    print(f"   - Langflow disponível: {LANGFLOW_AVAILABLE}")
    print(f"   - Sistema ativo: {'Langflow' if chatbot.use_langflow else 'Padrão'}")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 