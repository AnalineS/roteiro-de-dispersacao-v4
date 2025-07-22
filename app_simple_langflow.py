"""
Chatbot de Hanseníase - Versão Simplificada com Langflow
Evita problemas de compatibilidade com NumPy/PyTorch
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import re
import logging
from datetime import datetime
import requests

app = Flask(__name__)
CORS(app)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleHanseniaseChatbot:
    def __init__(self):
        self.use_langflow = False
        self.langflow_url = "http://localhost:7860"
        self.cache = {}
        self.pdf_text = ""
        
        # Carregar conteúdo do PDF
        self._load_pdf_content()
        
        # Verificar Langflow
        self._check_langflow()
    
    def _load_pdf_content(self):
        """Carrega o conteúdo do PDF"""
        pdf_path = "PDFs/Roteiro de Dsispensação - Hanseníase.md"
        
        try:
            if os.path.exists(pdf_path):
                with open(pdf_path, 'r', encoding='utf-8') as file:
                    self.pdf_text = file.read()
                logger.info(f"✅ PDF carregado: {len(self.pdf_text)} caracteres")
            else:
                logger.warning(f"⚠️ PDF não encontrado: {pdf_path}")
                self.pdf_text = ""
        except Exception as e:
            logger.error(f"❌ Erro ao carregar PDF: {e}")
            self.pdf_text = ""
    
    def _check_langflow(self):
        """Verifica se o Langflow está disponível"""
        # Carregar API key do arquivo .env
        self.api_key = os.environ.get("LANGFLOW_API_KEY", "sk-oZkcvhmKOMt0eRUizMCvOPLvgvNT1uEKrtm-Al4oXB4")
        
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.get(f"{self.langflow_url}/api/v1/health", 
                                  headers=headers, timeout=3)
            if response.status_code == 200:
                self.use_langflow = True
                logger.info("✅ Langflow detectado e ativo!")
                logger.info(f"   URL: {self.langflow_url}")
                logger.info(f"   API Key: {self.api_key[:10]}...")
            else:
                logger.info(f"ℹ️ Langflow não está rodando (status: {response.status_code})")
        except Exception as e:
            logger.info(f"ℹ️ Langflow não disponível - usando sistema simples ({e})")
    
    def answer_question(self, question: str, personality: str = "dr_gasnelio") -> dict:
        """
        Responde pergunta usando Langflow se disponível, senão usa busca simples
        
        Args:
            question: Pergunta do usuário
            personality: Personalidade (dr_gasnelio ou ga)
        
        Returns:
            Dict com resposta
        """
        # Verificar cache
        cache_key = f"{question}_{personality}"
        if cache_key in self.cache:
            cached_response = self.cache[cache_key]
            cached_response["source"] = "cache"
            return cached_response
        
        # Usar Langflow se disponível
        if self.use_langflow:
            try:
                result = self._langflow_answer(question, personality)
                if result.get("success"):
                    self.cache[cache_key] = result
                    return result
                else:
                    logger.warning("Langflow falhou, usando busca simples")
            except Exception as e:
                logger.error(f"Erro no Langflow: {e}")
        
        # Usar busca simples
        return self._simple_answer(question, personality)
    
    def _langflow_answer(self, question: str, personality: str) -> dict:
        """Resposta via Langflow"""
        try:
            payload = {
                "question": question,
                "personality": personality
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.post(
                f"{self.langflow_url}/api/v1/process",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "answer": result.get("output", ""),
                    "confidence": result.get("confidence", 0.8),
                    "personality": personality,
                    "timestamp": datetime.now().isoformat(),
                    "source": "langflow",
                    "question": question
                }
            else:
                return {
                    "success": False,
                    "error": f"Langflow retornou status {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _simple_answer(self, question: str, personality: str) -> dict:
        """Resposta usando busca simples no texto"""
        if not self.pdf_text:
            return self._fallback_response(question, personality)
        
        # Busca simples por palavras-chave
        question_lower = question.lower()
        paragraphs = self.pdf_text.split('\n\n')
        
        best_paragraph = ""
        best_score = 0
        
        # Palavras-chave importantes
        keywords = {
            "hanseníase": ["hanseníase", "lepra", "doença"],
            "tratamento": ["tratamento", "medicamento", "terapia", "cura"],
            "sintomas": ["sintoma", "sinal", "manifestação"],
            "diagnóstico": ["diagnóstico", "diagnosticar", "identificar"],
            "medicamento": ["medicamento", "remédio", "droga", "fármaco"]
        }
        
        # Encontrar parágrafo mais relevante
        for paragraph in paragraphs:
            if len(paragraph.strip()) < 50:
                continue
            
            paragraph_lower = paragraph.lower()
            score = 0
            
            # Calcular score baseado em palavras-chave
            for category, words in keywords.items():
                if any(word in question_lower for word in words):
                    if any(word in paragraph_lower for word in words):
                        score += 2
            
            # Score baseado em palavras comuns
            question_words = set(re.findall(r'\w+', question_lower))
            paragraph_words = set(re.findall(r'\w+', paragraph_lower))
            common_words = question_words.intersection(paragraph_words)
            score += len(common_words) / len(question_words) if question_words else 0
            
            if score > best_score:
                best_score = score
                best_paragraph = paragraph
        
        # Formatar resposta
        if best_paragraph and best_score > 0.5:
            answer = self._format_response(best_paragraph.strip(), personality, best_score)
            response = {
                "success": True,
                "answer": answer,
                "confidence": min(best_score / 5, 0.9),  # Normalizar confiança
                "personality": personality,
                "timestamp": datetime.now().isoformat(),
                "source": "simple_search",
                "question": question
            }
            
            # Salvar no cache
            cache_key = f"{question}_{personality}"
            self.cache[cache_key] = response
            
            return response
        else:
            return self._fallback_response(question, personality)
    
    def _format_response(self, text: str, personality: str, confidence: float) -> str:
        """Formata a resposta baseada na personalidade"""
        if personality == "dr_gasnelio":
            return f"Dr. Gasnelio responde:\n\nBaseado na minha tese sobre roteiro de dispensação para hanseníase, encontrei esta informação relevante:\n\n\"{text}\"\n\n*Confiança: {confidence:.2f}*"
        elif personality == "ga":
            # Simplificar texto para Gá
            simple_text = self._simplify_text(text)
            return f"Gá explica: {simple_text} 😊\n\n*Baseado na tese do Dr. Gasnelio*"
        else:
            return text
    
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
        """Resposta de fallback"""
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
        """Retorna informações sobre o sistema"""
        return {
            "langflow_active": self.use_langflow,
            "pdf_loaded": len(self.pdf_text) > 0,
            "cache_size": len(self.cache),
            "pdf_size": len(self.pdf_text)
        }

# Instanciar chatbot
chatbot = SimpleHanseniaseChatbot()

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
        "langflow_available": chatbot.use_langflow
    })

@app.route('/api/info')
def info():
    """Informações da API"""
    return jsonify({
        "name": "Chatbot Hanseníase - Versão Simplificada",
        "version": "2.1.0",
        "description": "Chatbot inteligente para perguntas sobre hanseníase",
        "features": [
            "Integração com Langflow (opcional)",
            "Busca simples no texto",
            "Duas personalidades",
            "Cache inteligente",
            "Sem dependências complexas"
        ],
        "personalities": {
            "dr_gasnelio": "Tom sério e técnico",
            "ga": "Tom descontraído e acessível"
        },
        "langflow_integration": chatbot.use_langflow
    })

@app.route('/api/system-status')
def system_status():
    """Status detalhado do sistema"""
    system_info = chatbot.get_system_info()
    
    return jsonify({
        "langflow": {
            "available": True,  # Sempre true, mas pode não estar rodando
            "active": system_info["langflow_active"]
        },
        "pdf": {
            "loaded": system_info["pdf_loaded"],
            "size": system_info["pdf_size"]
        },
        "cache": {
            "size": system_info["cache_size"]
        },
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Iniciando Chatbot de Hanseníase - Versão Simplificada...")
    print(f"📊 Status do sistema:")
    print(f"   - Langflow ativo: {chatbot.use_langflow}")
    print(f"   - PDF carregado: {len(chatbot.pdf_text) > 0}")
    print(f"   - Cache: {len(chatbot.cache)} itens")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 