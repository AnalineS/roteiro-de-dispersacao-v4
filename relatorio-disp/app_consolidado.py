from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import hashlib
from datetime import datetime
import logging
import numpy as np
from transformers import pipeline
import torch
from sentence_transformers import SentenceTransformer
from app.services.text_utils import chunk_text, expand_query_with_synonyms
from app.services.pdf_utils import extract_text_from_pdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class MultiDiseaseChatbot:
    def __init__(self):
        self.diseases = {}
        self.qa_pipeline = None
        self.embedding_model = None
        self.cache = {}
        self.load_models()
        self.load_diseases()

    def load_models(self):
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

    def load_diseases(self):
        try:
            self.diseases = {
                "hanseniase": {
                    "name": "Hanseníase",
                    "pdf_path": "PDFs/Roteiro de Dsispensação - Hanseníase F.docx.pdf",
                    "description": "Doença infecciosa crônica causada pela bactéria Mycobacterium leprae",
                    "keywords": ["hanseníase", "lepra", "mycobacterium", "bacilo de hansen"],
                    "personalities": {
                        "dr_gasnelio": {
                            "name": "Dr. Gasnelio",
                            "style": "sério e técnico",
                            "greeting": "Olá! Sou o Dr. Gasnelio, especialista em hanseníase. Como posso ajudá-lo hoje?",
                            "fallback": "Baseado na literatura médica sobre hanseníase, posso orientar que esta condição requer avaliação médica especializada. Recomendo consultar um dermatologista ou infectologista para diagnóstico adequado."
                        },
                        "ga": {
                            "name": "Gá",
                            "style": "descontraído e simples",
                            "greeting": "Oi! Sou o Gá! 😊 Vou te ajudar a entender sobre hanseníase de um jeito bem simples!",
                            "fallback": "Olha, sobre isso eu não tenho certeza no material que tenho aqui. Mas posso te dizer que é sempre bom procurar um médico quando temos dúvidas sobre saúde, certo? 😊"
                        }
                    }
                },
                # Outras doenças podem ser adicionadas aqui
            }
            os.makedirs("PDFs", exist_ok=True)
            logger.info(f"Carregadas {len(self.diseases)} doenças configuradas")
        except Exception as e:
            logger.error(f"Erro ao carregar doenças: {e}")
            raise

    def get_available_diseases(self):
        return [
            {
                "id": disease_id,
                "name": disease["name"],
                "description": disease["description"],
                "pdf_exists": os.path.exists(disease["pdf_path"])
            }
            for disease_id, disease in self.diseases.items()
        ]

    def get_disease_personalities(self, disease_id):
        if disease_id not in self.diseases:
            return []
        return [
            {
                "id": personality_id,
                "name": personality["name"],
                "style": personality["style"],
                "greeting": personality["greeting"]
            }
            for personality_id, personality in self.diseases[disease_id]["personalities"].items()
        ]

    def get_relevant_chunks(self, question, disease_id, top_k=5):
        if disease_id not in self.diseases:
            return []
        pdf_path = self.diseases[disease_id]["pdf_path"]
        if not os.path.exists(pdf_path):
            logger.warning(f"PDF não encontrado: {pdf_path}")
            return []
        text = extract_text_from_pdf(pdf_path)
        if not text:
            return []
        chunks = chunk_text(text)
        if not chunks or self.embedding_model is None:
            return []
        try:
            keyword_scores = np.zeros(len(chunks))
            question_words = set(question.lower().split())
            for i, chunk in enumerate(chunks):
                chunk_words = set(chunk.lower().split())
                common_words = question_words.intersection(chunk_words)
                if common_words:
                    keyword_scores[i] = len(common_words) / len(question_words)
            keyword_chunks = [i for i, score in enumerate(keyword_scores) if score > 0.1]
            if keyword_chunks:
                selected_chunks = [chunks[i] for i in keyword_chunks]
                question_embedding = self.embedding_model.encode(question)
                chunk_embeddings = self.embedding_model.encode(selected_chunks)
                similarities = np.dot(chunk_embeddings, question_embedding) / (
                    np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(question_embedding)
                )
                final_scores = 0.6 * similarities + 0.4 * keyword_scores[keyword_chunks]
                top_indices = np.argsort(final_scores)[-top_k:][::-1]
                relevant_chunks = [selected_chunks[i] for i in top_indices if final_scores[i] > 0.05]
            else:
                question_embedding = self.embedding_model.encode(question)
                chunk_embeddings = self.embedding_model.encode(chunks)
                similarities = np.dot(chunk_embeddings, question_embedding) / (
                    np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(question_embedding)
                )
                top_indices = np.argsort(similarities)[-top_k:][::-1]
                relevant_chunks = [chunks[i] for i in top_indices if similarities[i] > 0.1]
            return relevant_chunks
        except Exception as e:
            logger.error(f"Erro ao calcular similaridade: {e}")
            return []

def simplify_text(text: str) -> str:
    """
    Simplifica o texto para respostas amigáveis (persona Gá).
    """
    replacements = {
        "dispensação": "entrega de remédios",
        "medicamentos": "remédios",
        "posologia": "como tomar",
        "administração": "como tomar",
        "via de administração": "como tomar",
        "reação adversa": "efeito colateral",
        "interação medicamentosa": "mistura de remédios",
        "protocolo": "guia",
        "orientação": "explicação",
        "adesão": "seguir o tratamento"
    }
    simplified = text
    for technical, simple in replacements.items():
        simplified = simplified.replace(technical, simple)
    return simplified


def format_persona_answer(answer: str, persona: str, confidence: float, disease: str) -> dict:
    """
    Formata a resposta de acordo com a persona.
    """
    if persona == "dr_gasnelio":
        return {
            "answer": f"Dr. Gasnelio responde:\n\n{answer}\n\n*Baseado na tese sobre roteiro de dispensação para {disease}. Confiança: {confidence:.1%}*",
            "persona": "dr_gasnelio",
            "confidence": confidence,
            "disease": disease,
            "source": "model"
        }
    elif persona == "ga":
        simple_answer = simplify_text(answer)
        return {
            "answer": f"Gá explica:\n\n{simple_answer}\n\n*Tá na tese, pode confiar! 😊*",
            "persona": "ga",
            "confidence": confidence,
            "disease": disease,
            "source": "model"
        }
    else:
        return {
            "answer": answer,
            "persona": "default",
            "confidence": confidence,
            "disease": disease,
            "source": "model"
        }


def fallback_response(persona: str, disease: str, reason: str = "") -> dict:
    """
    Resposta de fallback personalizada por persona.
    """
    if persona == "dr_gasnelio":
        return {
            "answer": f"Dr. Gasnelio responde:\n\nDesculpe, não encontrei essa informação específica na minha tese sobre roteiro de dispensação para {disease}. {reason}\n\nPosso ajudá-lo com outras questões relacionadas ao tema da pesquisa.",
            "persona": "dr_gasnelio",
            "confidence": 0.0,
            "disease": disease,
            "source": "fallback"
        }
    elif persona == "ga":
        return {
            "answer": f"Gá responde:\n\nIh, essa eu não sei! 😅 {reason}\n\nSó posso explicar coisas que estão na tese sobre {disease} e dispensação de remédios. Pergunta outra coisa sobre o tema?",
            "persona": "ga",
            "confidence": 0.0,
            "disease": disease,
            "source": "fallback"
        }
    else:
        return {
            "answer": f"Desculpe, não encontrei essa informação na tese. {reason}",
            "persona": "default",
            "confidence": 0.0,
            "disease": disease,
            "source": "fallback"
        }


class MultiDiseaseChatbot:
    def __init__(self):
        self.diseases = {}
        self.qa_pipeline = None
        self.embedding_model = None
        self.cache = {}
        self.load_models()
        self.load_diseases()

    def load_models(self):
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

    def load_diseases(self):
        try:
            self.diseases = {
                "hanseniase": {
                    "name": "Hanseníase",
                    "pdf_path": "PDFs/Roteiro de Dsispensação - Hanseníase F.docx.pdf",
                    "description": "Doença infecciosa crônica causada pela bactéria Mycobacterium leprae",
                    "keywords": ["hanseníase", "lepra", "mycobacterium", "bacilo de hansen"],
                    "personalities": {
                        "dr_gasnelio": {
                            "name": "Dr. Gasnelio",
                            "style": "sério e técnico",
                            "greeting": "Olá! Sou o Dr. Gasnelio, especialista em hanseníase. Como posso ajudá-lo hoje?",
                            "fallback": "Baseado na literatura médica sobre hanseníase, posso orientar que esta condição requer avaliação médica especializada. Recomendo consultar um dermatologista ou infectologista para diagnóstico adequado."
                        },
                        "ga": {
                            "name": "Gá",
                            "style": "descontraído e simples",
                            "greeting": "Oi! Sou o Gá! 😊 Vou te ajudar a entender sobre hanseníase de um jeito bem simples!",
                            "fallback": "Olha, sobre isso eu não tenho certeza no material que tenho aqui. Mas posso te dizer que é sempre bom procurar um médico quando temos dúvidas sobre saúde, certo? 😊"
                        }
                    }
                },
                # Outras doenças podem ser adicionadas aqui
            }
            os.makedirs("PDFs", exist_ok=True)
            logger.info(f"Carregadas {len(self.diseases)} doenças configuradas")
        except Exception as e:
            logger.error(f"Erro ao carregar doenças: {e}")
            raise

    def get_available_diseases(self):
        return [
            {
                "id": disease_id,
                "name": disease["name"],
                "description": disease["description"],
                "pdf_exists": os.path.exists(disease["pdf_path"])
            }
            for disease_id, disease in self.diseases.items()
        ]

    def get_disease_personalities(self, disease_id):
        if disease_id not in self.diseases:
            return []
        return [
            {
                "id": personality_id,
                "name": personality["name"],
                "style": personality["style"],
                "greeting": personality["greeting"]
            }
            for personality_id, personality in self.diseases[disease_id]["personalities"].items()
        ]

    def get_relevant_chunks(self, question, disease_id, top_k=5):
        if disease_id not in self.diseases:
            return []
        pdf_path = self.diseases[disease_id]["pdf_path"]
        if not os.path.exists(pdf_path):
            logger.warning(f"PDF não encontrado: {pdf_path}")
            return []
        text = extract_text_from_pdf(pdf_path)
        if not text:
            return []
        chunks = chunk_text(text)
        if not chunks or self.embedding_model is None:
            return []
        try:
            keyword_scores = np.zeros(len(chunks))
            question_words = set(question.lower().split())
            for i, chunk in enumerate(chunks):
                chunk_words = set(chunk.lower().split())
                common_words = question_words.intersection(chunk_words)
                if common_words:
                    keyword_scores[i] = len(common_words) / len(question_words)
            keyword_chunks = [i for i, score in enumerate(keyword_scores) if score > 0.1]
            if keyword_chunks:
                selected_chunks = [chunks[i] for i in keyword_chunks]
                question_embedding = self.embedding_model.encode(question)
                chunk_embeddings = self.embedding_model.encode(selected_chunks)
                similarities = np.dot(chunk_embeddings, question_embedding) / (
                    np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(question_embedding)
                )
                final_scores = 0.6 * similarities + 0.4 * keyword_scores[keyword_chunks]
                top_indices = np.argsort(final_scores)[-top_k:][::-1]
                relevant_chunks = [selected_chunks[i] for i in top_indices if final_scores[i] > 0.05]
            else:
                question_embedding = self.embedding_model.encode(question)
                chunk_embeddings = self.embedding_model.encode(chunks)
                similarities = np.dot(chunk_embeddings, question_embedding) / (
                    np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(question_embedding)
                )
                top_indices = np.argsort(similarities)[-top_k:][::-1]
                relevant_chunks = [chunks[i] for i in top_indices if similarities[i] > 0.1]
            return relevant_chunks
        except Exception as e:
            logger.error(f"Erro ao calcular similaridade: {e}")
            return []

    def answer_question(self, question, disease_id, personality_id):
        if disease_id not in self.diseases:
            return {
                "error": "Doença não encontrada",
                "available_diseases": self.get_available_diseases()
            }
        if personality_id not in self.diseases[disease_id]["personalities"]:
            return {
                "error": "Personalidade não encontrada",
                "available_personalities": self.get_disease_personalities(disease_id)
            }
        cache_key = f"{disease_id}_{personality_id}_{hashlib.md5(question.encode()).hexdigest()}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        relevant_chunks = self.get_relevant_chunks(question, disease_id, top_k=5)
        personality = self.diseases[disease_id]["personalities"][personality_id]
        disease_name = self.diseases[disease_id]["name"]
        if not relevant_chunks:
            response = fallback_response(personality_id, disease_name)
            self.cache[cache_key] = response
            return response
        context = " ".join(relevant_chunks)
        try:
            if self.qa_pipeline is None:
                raise Exception("Pipeline de QA não disponível")
            question_variations = [question, question.replace("?", "").strip()]
            best_result = None
            best_confidence = 0.0
            for q_var in question_variations:
                try:
                    result = self.qa_pipeline(
                        question=q_var,
                        context=context,
                        max_answer_len=200,
                        handle_impossible_answer=True
                    )
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
            confidence = best_confidence
            if confidence < 0.3:
                if len(context) > 100:
                    sentences = context.split('.')
                    relevant_sentences = []
                    question_words = set(question.lower().split())
                    for sentence in sentences:
                        sentence_words = set(sentence.lower().split())
                        if question_words.intersection(sentence_words):
                            relevant_sentences.append(sentence.strip())
                    if relevant_sentences:
                        answer = relevant_sentences[0] + "."
                        source = "context_extraction"
                    else:
                        answer = personality["fallback"]
                        source = "no_answer"
                else:
                    answer = personality["fallback"]
                    source = "no_answer"
                response = format_persona_answer(answer, personality_id, confidence, disease_name)
            else:
                answer = best_result.get('answer', '')
                response = format_persona_answer(answer, personality_id, confidence, disease_name)
            self.cache[cache_key] = response
            return response
        except Exception as e:
            logger.error(f"Erro ao processar pergunta: {e}")
            response = fallback_response(personality_id, disease_name, reason="Erro técnico")
            self.cache[cache_key] = response
            return response

chatbot = MultiDiseaseChatbot()

@app.route('/')
def index():
    html_template = """
    <!DOCTYPE html>
    <html lang=\"pt-BR\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>Chatbot Multi-Doenças</title>
        <!-- (HTML e CSS do app_multi_disease.py, mantido moderno e responsivo) -->
    </head>
    <body>
        <!-- Conteúdo da interface de seleção de doença e personalidade -->
        <!-- (Pode ser copiado do app_multi_disease.py) -->
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    return jsonify(chatbot.get_available_diseases())

@app.route('/api/diseases/<disease_id>/personalities', methods=['GET'])
def get_personalities(disease_id):
    return jsonify(chatbot.get_disease_personalities(disease_id))

@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        disease_id = data.get('disease_id')
        personality_id = data.get('personality_id')
        if not question:
            return jsonify({"error": "Pergunta não fornecida"}), 400
        if not disease_id or not personality_id:
            return jsonify({"error": "Doença ou personalidade não fornecida"}), 400
        response = chatbot.answer_question(question, disease_id, personality_id)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Erro na API de chat: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "diseases_loaded": len(chatbot.diseases),
        "models_loaded": chatbot.qa_pipeline is not None and chatbot.embedding_model is not None,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🏥 Chatbot Multi-Doenças iniciando...")
    print(f"📚 Doenças carregadas: {len(chatbot.diseases)}")
    print("🌐 Servidor rodando em http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 