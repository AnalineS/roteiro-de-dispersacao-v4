from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import json
import re
from transformers.pipelines import pipeline
import torch
from sentence_transformers import SentenceTransformer
import numpy as np
import hashlib
import pickle
from datetime import datetime
from chatbot_core import DispensacaoChatbot
import logging
from app.services.text_utils import chunk_text, expand_query_with_synonyms
from app.services.pdf_utils import extract_text_from_pdf

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class HanseniaseChatbot:
    def __init__(self):
        self.pdf_path = "PDFs/Roteiro de Dsispensação - Hanseníase F.docx.pdf"
        self.qa_pipeline = None
        self.embedding_model = None
        self.cache = {}
        self.load_models()
        self.load_pdf_content()
        
        # Dicionário de sinônimos e termos relacionados
        self.synonyms = {
            'hanseníase': ['lepra', 'doença de hansen', 'mycobacterium leprae'],
            'medicamento': ['fármaco', 'droga', 'remédio', 'medicação'],
            'dispensação': ['dispensar', 'entrega', 'fornecimento', 'distribuição'],
            'tratamento': ['terapia', 'cura', 'medicação', 'tratar'],
            'sintomas': ['sinais', 'manifestações', 'sintomatologia'],
            'diagnóstico': ['identificação', 'detecção', 'diagnosticar'],
            'prevenção': ['prevenir', 'evitar', 'profilaxia'],
            'contágio': ['transmissão', 'infecção', 'contaminação'],
            'cura': ['tratamento', 'recuperação', 'melhora'],
            'antibiótico': ['antimicrobiano', 'medicamento antibacteriano'],
            'dapsona': ['dds', 'diaminodifenilsulfona'],
            'rifampicina': ['rifampin'],
            'clofazimina': ['lamprene'],
            'poliquimioterapia': ['pqt', 'tratamento múltiplo'],
            'paucibacilar': ['pb', 'poucos bacilos'],
            'multibacilar': ['mb', 'muitos bacilos'],
            'bacilo': ['bactéria', 'mycobacterium', 'micobactéria'],
            'lesão': ['ferida', 'mancha', 'alteração cutânea'],
            'pele': ['cutâneo', 'dermatológico', 'epiderme'],
            'nervo': ['neural', 'nervoso', 'neurológico'],
            'deformidade': ['deformação', 'sequela', 'alteração física'],
            'isolamento': ['separação', 'quarentena', 'isolamento social'],
            'notificação': ['comunicação', 'registro', 'declaração'],
            'vigilância': ['monitoramento', 'acompanhamento', 'supervisão'],
            'reação': ['resposta imunológica', 'inflamação', 'alergia'],
            'recidiva': ['recaída', 'retorno da doença', 'reaparecimento'],
            'resistência': ['resistente', 'refratário', 'não responsivo'],
            'adverso': ['efeito colateral', 'reação adversa', 'complicação'],
            'compliance': ['aderência', 'cumprimento', 'seguimento do tratamento'],
            'monitoramento': ['acompanhamento', 'vigilância', 'supervisão']
        }
    
    def load_models(self):
        """Carrega os modelos de IA"""
        try:
            logger.info("Carregando modelos de IA...")
            self.qa_pipeline = pipeline(
                "question-answering",
                model="deepset/roberta-base-squad2",
                device=-1 if not torch.cuda.is_available() else 0
            )
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Modelos carregados com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao carregar modelos: {e}")
            raise
    
    def load_pdf_content(self):
        """Carrega e processa o conteúdo do PDF"""
        try:
            if os.path.exists(self.pdf_path):
                self.pdf_text = extract_text_from_pdf(self.pdf_path)
                self.chunks = chunk_text(self.pdf_text)
                logger.info(f"PDF carregado: {len(self.chunks)} chunks")
            else:
                logger.warning(f"PDF não encontrado: {self.pdf_path}")
                self.pdf_text = ""
                self.chunks = []
        except Exception as e:
            logger.error(f"Erro ao carregar PDF: {e}")
            self.pdf_text = ""
            self.chunks = []
    
    def get_relevant_chunks(self, question, top_k=3):
        """Encontra os chunks mais relevantes para a pergunta com busca otimizada"""
        if not self.chunks or self.embedding_model is None:
            return []
        
        try:
            # Busca por palavras-chave primeiro (mais rápida)
            keyword_scores = np.zeros(len(self.chunks))
            question_words = set(question.lower().split())
            
            for i, chunk in enumerate(self.chunks):
                chunk_words = set(chunk.lower().split())
                common_words = question_words.intersection(chunk_words)
                if common_words:
                    keyword_scores[i] = len(common_words) / len(question_words)
            
            # Se encontrou chunks com palavras-chave, usar apenas eles
            keyword_chunks = [i for i, score in enumerate(keyword_scores) if score > 0.1]
            
            if keyword_chunks:
                # Usar apenas chunks com palavras-chave para embedding
                selected_chunks = [self.chunks[i] for i in keyword_chunks]
                question_embedding = self.embedding_model.encode(question)
                chunk_embeddings = self.embedding_model.encode(selected_chunks)
                
                # Calcular similaridade
                similarities = np.dot(chunk_embeddings, question_embedding) / (
                    np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(question_embedding)
                )
                
                # Combinar scores
                final_scores = 0.6 * similarities + 0.4 * keyword_scores[keyword_chunks]
                
                # Pegar os melhores
                top_indices = np.argsort(final_scores)[-top_k:][::-1]
                relevant_chunks = [selected_chunks[i] for i in top_indices if final_scores[i] > 0.05]
                
            else:
                # Fallback: usar embedding em todos os chunks
                question_embedding = self.embedding_model.encode(question)
                chunk_embeddings = self.embedding_model.encode(self.chunks)
                
                similarities = np.dot(chunk_embeddings, question_embedding) / (
                    np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(question_embedding)
                )
                
                top_indices = np.argsort(similarities)[-top_k:][::-1]
                relevant_chunks = [self.chunks[i] for i in top_indices if similarities[i] > 0.1]
            
            return relevant_chunks
            
        except Exception as e:
            logger.error(f"Erro ao calcular similaridade: {e}")
            return []
    
    def answer_question(self, question, personality_id):
        """Responde uma pergunta sobre hanseníase com cobertura melhorada"""
        # Verificar cache
        cache_key = f"{personality_id}_{hashlib.md5(question.encode()).hexdigest()}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Obter chunks relevantes com busca expandida
        relevant_chunks = self.get_relevant_chunks(question, top_k=5)
        
        if not relevant_chunks:
            # Sem resposta encontrada no PDF
            if personality_id == "dr_gasnelio":
                response = {
                    "answer": "Não encontrei essa informação específica na tese. Por favor, reformule sua pergunta ou seja mais específico sobre o aspecto da hanseníase que gostaria de saber.",
                    "confidence": 0.0,
                    "source": "no_answer",
                    "personality": "Dr. Gasnelio",
                    "disease": "Hanseníase"
                }
            else:
                response = {
                    "answer": "Olha, sobre isso específico eu não tenho certeza no material que tenho aqui. Mas posso te ajudar com outras perguntas sobre hanseníase! Que tal perguntar sobre sintomas, tratamento ou como funciona a dispensação dos medicamentos? 😊",
                    "confidence": 0.0,
                    "source": "fallback",
                    "personality": "Gá",
                    "disease": "Hanseníase"
                }
            self.cache[cache_key] = response
            return response
        
        # Combinar chunks relevantes com contexto expandido
        context = " ".join(relevant_chunks)
        
        try:
            # Verificar se o pipeline está disponível
            if self.qa_pipeline is None:
                raise Exception("Pipeline de QA não disponível")
            
            # Tentar apenas 2 variações da pergunta para melhor performance
            question_variations = [
                question,
                question.replace("?", "").strip()
            ]
            
            best_result = None
            best_confidence = 0.0
            
            for q_var in question_variations:
                try:
                    result = self.qa_pipeline(
                        question=q_var,
                        context=context,
                        max_answer_len=200,  # Reduzido para melhor performance
                        handle_impossible_answer=True
                    )
                    
                    # Verificar se result é um dicionário
                    if isinstance(result, dict):
                        confidence = result.get('score', 0.0)
                        
                        if confidence > best_confidence:
                            best_confidence = confidence
                            best_result = result
                        
                except Exception as e:
                    logger.debug(f"Erro com variação da pergunta: {e}")
                    continue
            
            if best_result is None:
                raise Exception("Nenhuma resposta válida encontrada")
            
            # Verificar confiança
            confidence = best_confidence
            
            if confidence < 0.3:  # Threshold ajustado
                if personality_id == "dr_gasnelio":
                    # Tentar fornecer uma resposta baseada no contexto
                    if len(context) > 100:
                        # Extrair informações relevantes do contexto
                        sentences = context.split('.')
                        relevant_sentences = []
                        question_words = set(question.lower().split())
                        
                        for sentence in sentences:
                            sentence_words = set(sentence.lower().split())
                            if question_words.intersection(sentence_words):
                                relevant_sentences.append(sentence.strip())
                        
                        if relevant_sentences:
                            # Pegar a primeira frase relevante
                            answer = relevant_sentences[0] + "."
                            source = "context_extraction"
                        else:
                            answer = ""
                            source = "no_answer"
                    else:
                        answer = ""
                        source = "no_answer"
                else:
                    answer = "Olha, encontrei algumas informações relacionadas, mas não tenho certeza total. Vou te contar o que sei: " + best_result.get('answer', '')
                    source = "low_confidence"
            else:
                answer = best_result.get('answer', '')
                source = "pdf"
            
            personality_name = "Dr. Gasnelio" if personality_id == "dr_gasnelio" else "Gá"
            
            response = {
                "answer": answer,
                "confidence": confidence,
                "source": source,
                "personality": personality_name,
                "disease": "Hanseníase"
            }
            
            self.cache[cache_key] = response
            return response
            
        except Exception as e:
            logger.error(f"Erro ao processar pergunta: {e}")
            if personality_id == "dr_gasnelio":
                response = {
                    "answer": "",
                    "confidence": 0.0,
                    "source": "error_no_answer",
                    "personality": "Dr. Gasnelio",
                    "disease": "Hanseníase"
                }
            else:
                response = {
                    "answer": "Ops, tive um probleminha técnico aqui! 😅 Mas não se preocupe, você pode tentar reformular sua pergunta ou perguntar sobre outro aspecto da hanseníase que eu posso te ajudar!",
                    "confidence": 0.0,
                    "source": "error_fallback",
                    "personality": "Gá",
                    "disease": "Hanseníase"
                }
            self.cache[cache_key] = response
            return response

# Inicializar chatbot
chatbot = HanseniaseChatbot()

@app.route('/')
def index():
    """Página inicial com seleção de personalidade"""
    html_template = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chatbot Hanseníase - Roteiro de Dispensação</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
                max-width: 800px;
                width: 100%;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            
            .content {
                padding: 40px;
            }
            
            .disease-info {
                background: #f8f9fa;
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 30px;
                text-align: center;
            }
            
            .disease-info h2 {
                color: #495057;
                margin-bottom: 15px;
            }
            
            .disease-info p {
                color: #6c757d;
                line-height: 1.6;
            }
            
            .personality-section {
                margin-top: 30px;
                text-align: center;
            }
            
            .personality-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            
            .personality-card {
                background: #f8f9fa;
                border-radius: 15px;
                padding: 30px;
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                cursor: pointer;
                border: 2px solid transparent;
            }
            
            .personality-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                border-color: #667eea;
            }
            
            .personality-card.selected {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .personality-card h3 {
                font-size: 1.5em;
                margin-bottom: 15px;
            }
            
            .personality-card p {
                font-size: 1em;
                opacity: 0.8;
                margin-bottom: 20px;
            }
            
            .personality-card .style {
                font-size: 0.9em;
                font-style: italic;
                opacity: 0.7;
            }
            
            .start-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 40px;
                border-radius: 25px;
                font-size: 1.1em;
                cursor: pointer;
                transition: transform 0.3s ease;
                margin-top: 20px;
            }
            
            .start-btn:hover {
                transform: translateY(-2px);
            }
            
            .start-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }
            
            .instructions {
                background: #e9ecef;
                border-radius: 15px;
                padding: 20px;
                margin-top: 30px;
            }
            
            .instructions h3 {
                color: #495057;
                margin-bottom: 15px;
            }
            
            .instructions ul {
                list-style: none;
                padding: 0;
            }
            
            .instructions li {
                padding: 8px 0;
                border-bottom: 1px solid #dee2e6;
            }
            
            .instructions li:last-child {
                border-bottom: none;
            }
            
            .instructions li:before {
                content: "✓";
                color: #28a745;
                font-weight: bold;
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 Chatbot Hanseníase</h1>
                <p>Roteiro de Dispensação Farmacêutica</p>
            </div>
            
            <div class="content">
                <div class="disease-info">
                    <h2>Hanseniase</h2>
                    <p>Doença infecciosa crônica causada pela bactéria Mycobacterium leprae. 
                    Este chatbot responde perguntas baseadas exclusivamente no conteúdo da tese sobre roteiro de dispensação farmacêutica.</p>
                </div>
                
                <div class="personality-section">
                    <h2 style="color: #495057; margin-bottom: 20px;">Escolha uma Personalidade:</h2>
                    
                    <div class="personality-grid">
                        <div class="personality-card" onclick="selectPersonality('dr_gasnelio')">
                            <h3>Dr. Gasnelio</h3>
                            <p>Especialista em hanseníase com abordagem técnica e científica</p>
                            <div class="style">Sério e técnico</div>
                        </div>
                        
                        <div class="personality-card" onclick="selectPersonality('ga')">
                            <h3>Gá</h3>
                            <p>Companheiro descontraído que explica de forma simples e acessível</p>
                            <div class="style">Descontraído e simples</div>
                        </div>
                    </div>
                    
                    <button class="start-btn" id="startBtn" disabled>Iniciar Chat</button>
                </div>
                
                <div class="instructions">
                    <h3>📋 Como usar:</h3>
                    <ul>
                        <li>Escolha entre Dr. Gasnelio (técnico) ou Gá (descontraído)</li>
                        <li>Clique em "Iniciar Chat" para começar a conversa</li>
                        <li>Faça perguntas sobre hanseníase e dispensação farmacêutica</li>
                        <li>O chatbot responderá baseado exclusivamente no conteúdo da tese</li>
                        <li>Dr. Gasnelio só responde se encontrar a informação no PDF</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <script>
            let selectedPersonality = null;
            
            function selectPersonality(personalityId) {
                selectedPersonality = personalityId;
                
                // Atualizar seleção visual
                document.querySelectorAll('.personality-card').forEach(card => {
                    card.classList.remove('selected');
                });
                event.target.closest('.personality-card').classList.add('selected');
                
                // Habilitar botão de início
                document.getElementById('startBtn').disabled = false;
            }
            
            function startChat() {
                if (selectedPersonality) {
                    // Redirecionar para o chat com parâmetros
                    window.location.href = `/chat?personality=${selectedPersonality}`;
                }
            }
            
            // Event listeners
            document.getElementById('startBtn').addEventListener('click', startChat);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/chat')
def chat():
    """Página do chat com personalidade específica"""
    personality_id = request.args.get('personality')
    
    if not personality_id or personality_id not in ['dr_gasnelio', 'ga']:
        return "Personalidade inválida", 400
    
    personality_name = "Dr. Gasnelio" if personality_id == "dr_gasnelio" else "Gá"
    personality_style = "sério e técnico" if personality_id == "dr_gasnelio" else "descontraído e simples"
    
    if personality_id == "dr_gasnelio":
        greeting = "Olá! Sou o Dr. Gasnelio, especialista em hanseníase. Como posso ajudá-lo hoje?"
    else:
        greeting = "Oi! Sou o Gá! 😊 Vou te ajudar a entender sobre hanseníase de um jeito bem simples!"
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat - Hanseníase - {personality_name}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }}
            
            .header {{
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .header-info {{
                display: flex;
                align-items: center;
                gap: 20px;
            }}
            
            .disease-badge {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
            }}
            
            .personality-badge {{
                background: #28a745;
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
            }}
            
            .back-btn {{
                background: #6c757d;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 20px;
                cursor: pointer;
                text-decoration: none;
                transition: background 0.3s ease;
            }}
            
            .back-btn:hover {{
                background: #5a6268;
            }}
            
            .chat-container {{
                flex: 1;
                display: flex;
                flex-direction: column;
                max-width: 800px;
                margin: 20px auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            
            .chat-header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            
            .chat-header h1 {{
                font-size: 2em;
                margin-bottom: 10px;
            }}
            
            .chat-header p {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            
            .chat-messages {{
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                max-height: 500px;
            }}
            
            .message {{
                margin-bottom: 20px;
                display: flex;
                align-items: flex-start;
                gap: 15px;
            }}
            
            .message.user {{
                flex-direction: row-reverse;
            }}
            
            .message-avatar {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: white;
                flex-shrink: 0;
            }}
            
            .message.user .message-avatar {{
                background: #667eea;
            }}
            
            .message.bot .message-avatar {{
                background: #28a745;
            }}
            
            .message-content {{
                background: #f8f9fa;
                padding: 15px 20px;
                border-radius: 20px;
                max-width: 70%;
                word-wrap: break-word;
            }}
            
            .message.user .message-content {{
                background: #667eea;
                color: white;
            }}
            
            .message.bot .message-content {{
                background: #e9ecef;
                color: #495057;
            }}
            
            .message-time {{
                font-size: 0.8em;
                opacity: 0.7;
                margin-top: 5px;
            }}
            
            .chat-input {{
                padding: 20px;
                border-top: 1px solid #dee2e6;
                background: #f8f9fa;
            }}
            
            .input-group {{
                display: flex;
                gap: 10px;
            }}
            
            .chat-input input {{
                flex: 1;
                padding: 15px 20px;
                border: 2px solid #dee2e6;
                border-radius: 25px;
                font-size: 1em;
                outline: none;
                transition: border-color 0.3s ease;
            }}
            
            .chat-input input:focus {{
                border-color: #667eea;
            }}
            
            .send-btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 25px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1em;
                transition: transform 0.3s ease;
            }}
            
            .send-btn:hover {{
                transform: translateY(-2px);
            }}
            
            .send-btn:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }}
            
            .typing-indicator {{
                display: none;
                padding: 15px 20px;
                background: #e9ecef;
                border-radius: 20px;
                margin-bottom: 20px;
                color: #6c757d;
                font-style: italic;
            }}
            
            .confidence-indicator {{
                font-size: 0.8em;
                opacity: 0.7;
                margin-top: 5px;
            }}
            
            .source-indicator {{
                font-size: 0.8em;
                opacity: 0.7;
                margin-top: 5px;
                font-style: italic;
            }}
            
            .no-answer {{
                color: #6c757d;
                font-style: italic;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="header-info">
                <span class="disease-badge">Hanseníase</span>
                <span class="personality-badge">{personality_name}</span>
            </div>
            <a href="/" class="back-btn">← Voltar</a>
        </div>
        
        <div class="chat-container">
            <div class="chat-header">
                <h1>{personality_name}</h1>
                <p>Especialista em Hanseníase - {personality_style}</p>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message bot">
                    <div class="message-avatar">{personality_name[0]}</div>
                    <div class="message-content">
                        {greeting}
                        <div class="message-time">{datetime.now().strftime('%H:%M')}</div>
                    </div>
                </div>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                {personality_name} está digitando...
            </div>
            
            <div class="chat-input">
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Digite sua pergunta sobre hanseníase..." onkeypress="handleKeyPress(event)">
                    <button class="send-btn" id="sendBtn" onclick="sendMessage()">Enviar</button>
                </div>
            </div>
        </div>
        
        <script>
            const personalityId = '{personality_id}';
            const personalityName = '{personality_name}';
            
            function addMessage(content, isUser = false, confidence = null, source = null) {{
                const messagesContainer = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${{isUser ? 'user' : 'bot'}}`;
                
                const avatar = document.createElement('div');
                avatar.className = 'message-avatar';
                avatar.textContent = isUser ? 'U' : personalityName[0];
                
                const messageContent = document.createElement('div');
                messageContent.className = 'message-content';
                
                if (content === '') {{
                    messageContent.innerHTML = '<span class="no-answer">Não encontrei essa informação na tese.</span>';
                }} else {{
                    messageContent.innerHTML = content;
                }}
                
                const time = document.createElement('div');
                time.className = 'message-time';
                time.textContent = new Date().toLocaleTimeString('pt-BR', {{hour: '2-digit', minute: '2-digit'}});
                messageContent.appendChild(time);
                
                if (confidence !== null && source !== null) {{
                    const confidenceDiv = document.createElement('div');
                    confidenceDiv.className = 'confidence-indicator';
                    confidenceDiv.textContent = `Confiança: ${{(confidence * 100).toFixed(1)}}%`;
                    messageContent.appendChild(confidenceDiv);
                    
                    const sourceDiv = document.createElement('div');
                    sourceDiv.className = 'source-indicator';
                    if (source === 'pdf') {{
                        sourceDiv.textContent = 'Fonte: PDF da tese';
                    }} else if (source === 'no_answer') {{
                        sourceDiv.textContent = 'Fonte: Sem resposta encontrada';
                    }} else if (source === 'context_extraction') {{
                        sourceDiv.textContent = 'Fonte: Extração de contexto';
                    }} else {{
                        sourceDiv.textContent = 'Fonte: Resposta padrão';
                    }}
                    messageContent.appendChild(sourceDiv);
                }}
                
                messageDiv.appendChild(avatar);
                messageDiv.appendChild(messageContent);
                messagesContainer.appendChild(messageDiv);
                
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }}
            
            function showTyping() {{
                document.getElementById('typingIndicator').style.display = 'block';
                document.getElementById('chatMessages').scrollTop = document.getElementById('chatMessages').scrollHeight;
            }}
            
            function hideTyping() {{
                document.getElementById('typingIndicator').style.display = 'none';
            }}
            
            async function sendMessage() {{
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Adicionar mensagem do usuário
                addMessage(message, true);
                input.value = '';
                
                // Mostrar indicador de digitação
                showTyping();
                
                try {{
                    const response = await fetch('/api/chat', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify({{
                            question: message,
                            personality_id: personalityId
                        }})
                    }});
                    
                    const data = await response.json();
                    
                    hideTyping();
                    
                    if (data.error) {{
                        addMessage(`Erro: ${{data.error}}`);
                    }} else {{
                        addMessage(data.answer, false, data.confidence, data.source);
                    }}
                }} catch (error) {{
                    hideTyping();
                    addMessage('Erro ao enviar mensagem. Tente novamente.');
                    console.error('Erro:', error);
                }}
            }}
            
            function handleKeyPress(event) {{
                if (event.key === 'Enter') {{
                    sendMessage();
                }}
            }}
            
            // Focar no input ao carregar
            document.getElementById('messageInput').focus();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        # Garante que o corpo é JSON válido
        if not request.is_json:
            return jsonify({"error": "Requisição deve ser JSON"}), 400

        data = request.get_json(force=True, silent=True)

        # Instancia o chatbot
        # dispensacao_bot = DispensacaoChatbot()  # Corrigido: linha removida/comentada pois estava fora do bloco correto

        question = data.get('question', '').strip()
        personality_id = data.get('personality_id')

        if not question:
            return jsonify({"error": "Pergunta não fornecida"}), 400

        if not personality_id:
            return jsonify({"error": "Personalidade não fornecida"}), 400

        response = chatbot.answer_question(question, personality_id)
        return jsonify(response)

    except Exception as e:
        logger.error(f"Erro na API de chat: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificação de saúde da API"""
    return jsonify({
        "status": "healthy",
        "pdf_loaded": len(chatbot.chunks) > 0,
        "models_loaded": chatbot.qa_pipeline is not None and chatbot.embedding_model is not None,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🏥 Chatbot Hanseníase iniciando...")
    print(f"📚 PDF carregado: {len(chatbot.chunks)} chunks")
    print("🌐 Servidor rodando em http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 
