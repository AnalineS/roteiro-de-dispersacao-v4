import json
import os
import sys
import logging
from datetime import datetime
import numpy as np
import hashlib

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionar o diretório atual ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from transformers.pipelines import pipeline
    import torch
    from sentence_transformers import SentenceTransformer
    import PyPDF2
    from app.services.text_utils import chunk_text, expand_query_with_synonyms
    from app.services.pdf_utils import extract_text_from_pdf
except ImportError as e:
    logger.error(f"Erro ao importar dependências: {e}")
    raise

class HanseniaseChatbot:
    def __init__(self):
        self.pdf_path = "PDFs/Roteiro de Dsispensação - Hanseníase F.docx.pdf"
        self.qa_pipeline = None
        self.embedding_model = None
        self.cache = {}
        
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
        
        self.load_models()
        self.load_pdf_content()
    
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
        relevant_chunks = self.get_relevant_chunks(question, top_k=3)
        
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

# Inicializar chatbot globalmente
chatbot = None

def handler(event, context):
    """Handler principal para o Netlify Functions"""
    global chatbot
    
    # Configurar CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    }
    
    # Responder a requisições OPTIONS (preflight)
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # Inicializar chatbot se necessário
        if chatbot is None:
            chatbot = HanseniaseChatbot()
        
        # Verificar se é uma requisição de health check
        if event['httpMethod'] == 'GET' and event['path'] == '/api/health':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    "status": "healthy",
                    "pdf_loaded": len(chatbot.chunks) > 0,
                    "models_loaded": chatbot.qa_pipeline is not None and chatbot.embedding_model is not None,
                    "timestamp": datetime.now().isoformat()
                })
            }
        
        # Verificar se é uma requisição de chat
        if event['httpMethod'] == 'POST' and event['path'] == '/api/chat':
            # Garantir que o corpo é JSON válido
            if not event.get('body'):
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({"error": "Corpo da requisição vazio"})
                }
            
            try:
                data = json.loads(event['body'])
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({"error": "JSON inválido"})
                }
            
            question = data.get('question', '').strip()
            personality_id = data.get('personality_id')
            
            if not question:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({"error": "Pergunta não fornecida"})
                }
            
            if not personality_id or personality_id not in ['dr_gasnelio', 'ga']:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({"error": "Personalidade inválida"})
                }
            
            # Responder pergunta
            response = chatbot.answer_question(question, personality_id)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response)
            }
        
        # Rota não encontrada
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({"error": "Rota não encontrada"})
        }
        
    except Exception as e:
        logger.error(f"Erro no handler: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"error": "Erro interno do servidor"})
        } 