from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from transformers import pipeline
import torch
import re
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis globais
MD_PATH = 'PDFs/Roteiro de Dsispensação - Hanseníase.md'
md_text = ""
qa_pipeline = None
tokenizer = None
model = None

def extract_md_text(md_path):
    """Extrai texto do arquivo Markdown"""
    global md_text
    try:
        with open(md_path, 'r', encoding='utf-8') as file:
            text = file.read()
        logger.info(f"Arquivo Markdown extraído com sucesso. Total de caracteres: {len(text)}")
        return text
    except Exception as e:
        logger.error(f"Erro ao extrair arquivo Markdown: {e}")
        return ""

def load_ai_model():
    """Carrega o modelo de IA gratuito do Hugging Face"""
    global qa_pipeline, tokenizer, model
    try:
        # Usando modelo gratuito e leve
        model_name = "kimie/kimie2-pt-qa:free"
        logger.info(f"Carregando modelo: {model_name}")
        
        qa_pipeline = pipeline(
            "question-answering",
            model=model_name,
            tokenizer=model_name,
            device=-1 if not torch.cuda.is_available() else 0
        )
        logger.info("Modelo carregado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {e}")
        qa_pipeline = None

def find_relevant_context(question, full_text, max_length=4000):
    """Encontra o contexto mais relevante para a pergunta"""
    # Divide o texto em chunks menores
    chunks = []
    chunk_size = 2000
    overlap = 200
    
    for i in range(0, len(full_text), chunk_size - overlap):
        chunk = full_text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    
    # Se temos poucos chunks, retorna o texto completo
    if len(chunks) <= 2:
        return full_text[:max_length]
    
    # Para perguntas simples, usa o primeiro chunk
    if len(question.split()) <= 5:
        return chunks[0][:max_length]
    
    # Busca por palavras-chave na pergunta
    question_words = set(re.findall(r'\w+', question.lower()))
    
    best_chunk = chunks[0]
    best_score = 0
    
    for chunk in chunks:
        chunk_words = set(re.findall(r'\w+', chunk.lower()))
        common_words = question_words.intersection(chunk_words)
        score = len(common_words) / len(question_words) if question_words else 0
        
        if score > best_score:
            best_score = score
            best_chunk = chunk
    
    return best_chunk[:max_length]

def answer_question(question, persona):
    """Responde à pergunta usando o modelo de IA"""
    global qa_pipeline, md_text
    
    if not qa_pipeline or not md_text:
        return fallback_response(persona, "Modelo não disponível")
    
    try:
        # Encontra contexto relevante
        context = find_relevant_context(question, md_text)
        
        # Faz a pergunta ao modelo
        result = qa_pipeline(
            question=question,
            context=context,
            max_answer_len=200,
            handle_impossible_answer=True
        )
        
        answer = result['answer'].strip()
        confidence = result['score']
        
        logger.info(f"Pergunta: {question}")
        logger.info(f"Confiança: {confidence}")
        logger.info(f"Resposta: {answer}")
        
        # Se a confiança for baixa ou resposta vazia, usa fallback aprimorado
        if not answer or confidence < 0.3:
            logger.info("Usando fallback aprimorado - confiança baixa")
            return enhanced_fallback_response(question, persona, context)
        
        return format_persona_answer(answer, persona, confidence)
        
    except Exception as e:
        logger.error(f"Erro ao processar pergunta: {e}")
        return fallback_response(persona, "Erro técnico")

def format_persona_answer(answer, persona, confidence):
    """Formata a resposta de acordo com a personalidade, usando linguagem natural"""
    if persona == "dr_gasnelio":
        # Resposta técnica, mas acolhedora e natural
        return {
            "answer": (
                f"Olá! Aqui é o Dr. Gasnelio. Sobre sua dúvida:\n\n"
                f"{answer}\n\n"
                f"Se precisar de mais detalhes ou exemplos, posso explicar de outra forma.\n"
                f"*Baseado na tese sobre roteiro de dispensação para hanseníase. Confiança: {confidence:.1%}*"
            ),
            "persona": "dr_gasnelio",
            "confidence": confidence
        }
    elif persona == "ga":
        # Simplifica e deixa a resposta ainda mais próxima do cotidiano
        simple_answer = simplify_text(answer)
        return {
            "answer": (
                f"Oi! Eu sou o Gá. Olha só, de um jeito bem simples:\n\n"
                f"{simple_answer}\n\n"
                f"Se quiser, posso dar um exemplo ou explicar de outro jeito. É só pedir! 😊\n"
                f"*Essa explicação veio direto da tese, mas falei do meu jeito pra facilitar.*"
            ),
            "persona": "ga",
            "confidence": confidence
        }
    else:
        return {
            "answer": answer,
            "persona": "default",
            "confidence": confidence
        }

def simplify_text(text):
    """Simplifica o texto para o Gá, deixando mais natural e próximo do cotidiano"""
    replacements = {
        "dispensação": "entrega do remédio na farmácia",
        "farmacêutico": "farmacêutico (quem trabalha na farmácia)",
        "medicamentos": "remédios",
        "tratamento": "tratamento (o que a pessoa faz para melhorar)",
        "hanseníase": "hanseníase (doença de pele)",
        "protocolo": "guia de cuidados",
        "orientação": "explicação",
        "paciente": "pessoa que está tratando",
        "adesão": "seguir direitinho o tratamento",
        "posologia": "como tomar o remédio",
        "administração": "como usar o remédio",
        "via de administração": "jeito de tomar o remédio",
        "reação adversa": "efeito colateral (coisa ruim que pode acontecer)",
        "interação medicamentosa": "mistura de remédios que pode dar problema",
        "supervisionada": "com alguém olhando junto",
        "autoadministrada": "a própria pessoa toma sozinha",
        "prescrição": "receita do médico",
        "dose": "quantidade do remédio",
        "contraindicação": "quando não pode usar",
        "indicação": "quando é recomendado usar"
    }
    simplified = text
    for technical, simple in replacements.items():
        simplified = simplified.replace(technical, simple)
    # Deixar frases mais curtas e naturais
    simplified = simplified.replace(". ", ".\n")
    return simplified

def enhanced_fallback_response(question, persona, context):
    """Fallback aprimorado que retorna trecho relevante do PDF"""
    logger.info("Executando fallback aprimorado")
    
    # Busca por palavras-chave na pergunta
    question_words = set(re.findall(r'\w+', question.lower()))
    
    # Divide o contexto em parágrafos
    paragraphs = context.split('\n\n')
    
    best_paragraph = ""
    best_score = 0
    
    for paragraph in paragraphs:
        if len(paragraph.strip()) < 50:  # Ignora parágrafos muito pequenos
            continue
            
        paragraph_words = set(re.findall(r'\w+', paragraph.lower()))
        common_words = question_words.intersection(paragraph_words)
        score = len(common_words) / len(question_words) if question_words else 0
        
        if score > best_score:
            best_score = score
            best_paragraph = paragraph
    
    # Se encontrou um parágrafo relevante
    if best_paragraph and best_score > 0.1:
        logger.info(f"Parágrafo relevante encontrado com score: {best_score}")
        
        if persona == "dr_gasnelio":
            return {
                "answer": f"Dr. Gasnelio responde:\n\nBaseado na minha tese sobre roteiro de dispensação para hanseníase, encontrei esta informação técnica relevante:\n\n\"{best_paragraph.strip()}\"\n\n*Esta é uma extração direta do texto da tese. Para informações mais específicas, recomendo consultar a seção completa.*",
                "persona": "dr_gasnelio",
                "confidence": best_score
            }
        elif persona == "ga":
            # Simplifica o texto para o Gá
            simple_paragraph = simplify_text(best_paragraph.strip())
            return {
                "answer": f"Gá responde:\n\nOlha só o que encontrei na tese:\n\n\"{simple_paragraph}\"\n\n*Tá na tese, pode confiar! 😊*",
                "persona": "ga",
                "confidence": best_score
            }
        else:
            return {
                "answer": f"Encontrei esta informação na tese:\n\n\"{best_paragraph.strip()}\"",
                "persona": "default",
                "confidence": best_score
            }
    
    # Se não encontrou nada relevante, usa fallback padrão
    logger.info("Nenhum parágrafo relevante encontrado, usando fallback padrão")
    return fallback_response(persona, "Informação não encontrada na tese")

def fallback_response(persona, reason=""):
    """Resposta de fallback quando não encontra informação"""
    logger.info(f"Executando fallback padrão para persona: {persona}")
    
    if persona == "dr_gasnelio":
        return {
            "answer": f"Dr. Gasnelio responde:\n\nDesculpe, não encontrei essa informação específica na minha tese sobre roteiro de dispensação para hanseníase. {reason}\n\nPosso ajudá-lo com outras questões relacionadas ao tema da pesquisa.",
            "persona": "dr_gasnelio",
            "confidence": 0.0
        }
    elif persona == "ga":
        return {
            "answer": f"Gá responde:\n\nIh, essa eu não sei! 😅 {reason}\n\nSó posso explicar coisas que estão na tese sobre hanseníase e dispensação de remédios. Pergunta outra coisa sobre o tema?",
            "persona": "ga",
            "confidence": 0.0
        }
    else:
        return {
            "answer": f"Desculpe, não encontrei essa informação na tese. {reason}",
            "persona": "default",
            "confidence": 0.0
        }

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/tese')
def tese():
    return render_template('tese.html')

@app.route('/script.js')
def serve_script():
    """Serve o arquivo script.js na raiz do projeto"""
    return app.send_static_file('script.js')

@app.route('/tese.js')
def serve_tese_script():
    """Serve o arquivo tese.js na raiz do projeto"""
    return app.send_static_file('tese.js')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        # Garante que o corpo é JSON válido
        if not request.is_json:
            return jsonify({"error": "Requisição deve ser JSON"}), 400

        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "JSON inválido ou vazio"}), 400

        question = data.get('question', '').strip()
        personality_id = data.get('personality_id')

        if not question:
            return jsonify({"error": "Pergunta não fornecida"}), 400

        if not personality_id or personality_id not in ['dr_gasnelio', 'ga']:
            return jsonify({"error": "Personalidade inválida"}), 400

        # Responder pergunta
        response = answer_question(question, personality_id)
        return jsonify(response)

    except Exception as e:
        logger.error(f"Erro na API de chat: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificação de saúde da API"""
    return jsonify({
        "status": "healthy",
        "model_loaded": qa_pipeline is not None,
        "pdf_loaded": len(md_text) > 0,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/info', methods=['GET'])
def api_info():
    """Informações sobre a API"""
    return jsonify({
        "name": "Chatbot Tese Hanseníase API",
        "version": "1.0.0",
        "description": "API para chatbot baseado na tese sobre roteiro de dispensação para hanseníase",
        "personas": {
            "dr_gasnelio": "Professor sério e técnico",
            "ga": "Amigo descontraído que explica de forma simples"
        },
        "model": "kimie/kimie2-pt-qa:free",
        "pdf_source": "Roteiro de Dispensação para Hanseníase"
    })

if __name__ == '__main__':
    # Inicialização
    logger.info("Iniciando aplicação...")
    
    # Carrega o PDF
    if os.path.exists(MD_PATH):
        md_text = extract_md_text(MD_PATH)
    else:
        logger.warning(f"Arquivo Markdown não encontrado: {MD_PATH}")
        md_text = "Arquivo Markdown não disponível"
    
    # Carrega o modelo de IA
    load_ai_model()
    
    # Inicia o servidor
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Servidor iniciado na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) 