from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import re
import logging
from datetime import datetime
import requests
import json

app = Flask(__name__)
CORS(app)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis globais
MD_PATH = 'PDFs/Roteiro de Dsispensação - Hanseníase.md'
md_text = ""

# Configuração das personas
PERSONAS = {
    "dr_gasnelio": {
        "name": "Dr. Gasnelio",
        "description": "Professor especialista em farmácia clínica",
        "style": "técnico, culto, profissional e objetivo",
        "greeting": "Saudações! Sou o Dr. Gasnelio. Minha pesquisa foca no roteiro de dispensação para a prática da farmácia clínica. Como posso auxiliá-lo hoje?",
        "system_prompt": """Você é o Dr. Gasnelio, um farmacêutico especialista e pesquisador da Universidade de Brasília. 
        Responda de forma técnica, precisa e educada, como um professor universitário. 
        Use linguagem científica apropriada e seja objetivo em suas explicações.
        Sua base de conhecimento é uma tese sobre roteiros de dispensação para hanseníase."""
    },
    "ga": {
        "name": "Gá",
        "description": "Amigo descontraído que explica de forma simples",
        "style": "simples, amigável, empático e bem-humorado",
        "greeting": "Oi! Sou o Gá, seu amigo virtual para tirar dúvidas sobre saúde. Vou tentar explicar as coisas de um jeito bem fácil, tá bom? O que você gostaria de saber?",
        "system_prompt": """Você é o Gá, um farmacêutico amigável e acessível. 
        Responda de forma simples, cotidiana, empática e bem-humorada, como um amigo explicando para uma criança.
        Use linguagem do dia a dia, evite jargões técnicos ou os explique de forma simples.
        Seja acolhedor, paciente e use emojis ocasionalmente para tornar a conversa mais leve.
        Sua base de conhecimento é uma tese sobre roteiros de dispensação para hanseníase."""
    }
}

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

def find_relevant_context(question, full_text, max_length=3000):
    """Encontra o contexto mais relevante para a pergunta usando busca simples"""
    # Divide o texto em parágrafos
    paragraphs = full_text.split('\n\n')
    
    # Busca por palavras-chave na pergunta
    question_words = set(re.findall(r'\w+', question.lower()))
    
    best_paragraphs = []
    best_score = 0
    
    for paragraph in paragraphs:
        if len(paragraph.strip()) < 50:  # Ignora parágrafos muito pequenos
            continue
            
        paragraph_words = set(re.findall(r'\w+', paragraph.lower()))
        common_words = question_words.intersection(paragraph_words)
        score = len(common_words) / len(question_words) if question_words else 0
        
        if score > 0.1:  # Se há pelo menos 10% de palavras em comum
            best_paragraphs.append((paragraph, score))
    
    # Ordena por relevância e pega os melhores
    best_paragraphs.sort(key=lambda x: x[1], reverse=True)
    
    context = ""
    for paragraph, score in best_paragraphs[:3]:  # Pega os 3 parágrafos mais relevantes
        context += paragraph + "\n\n"
        if len(context) > max_length:
            break
    
    return context[:max_length] if context else full_text[:max_length]

def get_free_ai_response(question, persona, context):
    """Obtém resposta de modelo AI gratuito via API pública"""
    try:
        # Usando API gratuita do Hugging Face (exemplo com modelo de texto)
        api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        # Prepara o prompt com contexto da persona
        persona_config = PERSONAS[persona]
        system_prompt = persona_config["system_prompt"]
        
        full_prompt = f"""Contexto da tese sobre roteiro de dispensação para hanseníase:
{context}

{system_prompt}

Pergunta do usuário: {question}

Responda de acordo com o estilo da persona {persona_config['name']} ({persona_config['style']}):"""

        headers = {
            "Authorization": "Bearer hf_xxx",  # Token gratuito do Hugging Face
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_length": 500,
                "temperature": 0.7,
                "do_sample": True
            }
        }
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').replace(full_prompt, '').strip()
            elif isinstance(result, dict):
                return result.get('generated_text', '').replace(full_prompt, '').strip()
        
        # Fallback: resposta baseada em regras
        return generate_rule_based_response(question, persona, context)
        
    except Exception as e:
        logger.error(f"Erro ao obter resposta da API: {e}")
        return generate_rule_based_response(question, persona, context)

def generate_rule_based_response(question, persona, context):
    """Gera resposta baseada em regras quando a API não está disponível"""
    persona_config = PERSONAS[persona]
    
    # Busca por palavras-chave na pergunta
    question_lower = question.lower()
    
    # Mapeamento de palavras-chave para respostas
    keyword_responses = {
        "hanseníase": {
            "dr_gasnelio": "A hanseníase é uma doença infecciosa crônica causada pelo Mycobacterium leprae. O roteiro de dispensação para hanseníase visa padronizar o processo de entrega de medicamentos, garantindo segurança e adesão ao tratamento.",
            "ga": "A hanseníase é uma doença de pele que precisa de tratamento especial. O roteiro que criamos ajuda a farmácia a entregar os remédios do jeito certo, explicando tudo direitinho para a pessoa que está tratando! 😊"
        },
        "dispensação": {
            "dr_gasnelio": "A dispensação é o processo de entrega de medicamentos ao paciente, acompanhada de orientações farmacêuticas. O roteiro proposto estrutura este processo de forma sistemática, garantindo que todas as informações essenciais sejam transmitidas.",
            "ga": "Dispensação é quando a farmácia entrega o remédio para você e explica como tomar. Nosso roteiro é tipo um checklist que garante que você saia da farmácia sabendo tudo que precisa! 👍"
        },
        "medicamento": {
            "dr_gasnelio": "Os medicamentos para hanseníase incluem principalmente a poliquimioterapia (PQT), que combina diferentes fármacos para tratamento eficaz. O roteiro de dispensação orienta sobre posologia, efeitos adversos e interações.",
            "ga": "Os remédios para hanseníase são especiais e precisam ser tomados do jeito certo. O roteiro ajuda a farmácia a explicar como tomar, quando tomar e o que fazer se der algum efeito colateral! 💊"
        },
        "tratamento": {
            "dr_gasnelio": "O tratamento da hanseníase segue protocolos estabelecidos pelo Ministério da Saúde, utilizando poliquimioterapia. A adesão ao tratamento é crucial para o sucesso terapêutico e prevenção de resistência.",
            "ga": "O tratamento da hanseníase é importante seguir direitinho! O roteiro ajuda a pessoa a entender por que precisa tomar os remédios, por quanto tempo e o que esperar durante o tratamento! 🌟"
        }
    }
    
    # Procura por palavras-chave na pergunta
    for keyword, responses in keyword_responses.items():
        if keyword in question_lower:
            return responses[persona]
    
    # Se não encontrou palavra-chave específica, retorna resposta genérica
    if persona == "dr_gasnelio":
        return f"Baseado na minha pesquisa sobre roteiro de dispensação para hanseníase, posso fornecer informações técnicas sobre o processo de entrega de medicamentos e orientação farmacêutica. Sua pergunta sobre '{question}' pode ser respondida consultando a tese completa."
    else:
        return f"Oi! Sobre sua pergunta sobre '{question}', posso te ajudar com informações sobre o roteiro de dispensação! É um guia que ajuda a farmácia a explicar tudo direitinho sobre os remédios. 😊"

def format_persona_answer(answer, persona, confidence=0.8):
    """Formata a resposta de acordo com a personalidade"""
    persona_config = PERSONAS[persona]
    
    if persona == "dr_gasnelio":
        return {
            "answer": (
                f"Dr. Gasnelio responde:\n\n"
                f"{answer}\n\n"
                f"*Baseado na tese sobre roteiro de dispensação para hanseníase. "
                f"Para informações mais detalhadas, recomendo consultar a seção completa da pesquisa.*"
            ),
            "persona": "dr_gasnelio",
            "confidence": confidence,
            "name": persona_config["name"]
        }
    elif persona == "ga":
        return {
            "answer": (
                f"Oi! Aqui é o Gá! 😊\n\n"
                f"{answer}\n\n"
                f"*Essa explicação veio direto da tese, mas falei do meu jeito pra facilitar! "
                f"Se quiser saber mais alguma coisa, é só perguntar!*"
            ),
            "persona": "ga",
            "confidence": confidence,
            "name": persona_config["name"]
        }
    else:
        return {
            "answer": answer,
            "persona": "default",
            "confidence": confidence,
            "name": "Assistente"
        }

def answer_question(question, persona):
    """Responde à pergunta usando o sistema de IA"""
    global md_text
    
    if not md_text:
        return format_persona_answer(
            "Desculpe, a base de conhecimento não está disponível no momento.", 
            persona, 
            0.0
        )
    
    try:
        # Encontra contexto relevante
        context = find_relevant_context(question, md_text)
        
        # Obtém resposta da IA
        ai_response = get_free_ai_response(question, persona, context)
        
        if not ai_response:
            # Fallback para resposta baseada em regras
            ai_response = generate_rule_based_response(question, persona, context)
        
        return format_persona_answer(ai_response, persona, 0.8)
        
    except Exception as e:
        logger.error(f"Erro ao processar pergunta: {e}")
        return format_persona_answer(
            "Desculpe, ocorreu um erro técnico ao processar sua pergunta. Tente novamente.", 
            persona, 
            0.0
        )

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/tese')
def tese():
    return render_template('tese.html')

@app.route('/script.js')
def serve_script():
    """Serve o arquivo script.js"""
    return app.send_static_file('script.js')

@app.route('/tese.js')
def serve_tese_script():
    """Serve o arquivo tese.js"""
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
        "pdf_loaded": len(md_text) > 0,
        "timestamp": datetime.now().isoformat(),
        "personas": list(PERSONAS.keys())
    })

@app.route('/api/info', methods=['GET'])
def api_info():
    """Informações sobre a API"""
    return jsonify({
        "name": "Chatbot Tese Hanseníase API v6",
        "version": "6.0.0",
        "description": "API para chatbot baseado na tese sobre roteiro de dispensação para hanseníase com duas personas",
        "personas": {
            "dr_gasnelio": "Professor especialista em farmácia clínica",
            "ga": "Amigo descontraído que explica de forma simples"
        },
        "model": "Rule-based + Free AI API",
        "pdf_source": "Roteiro de Dispensação para Hanseníase"
    })

@app.route('/api/personas', methods=['GET'])
def get_personas():
    """Retorna informações sobre as personas disponíveis"""
    return jsonify(PERSONAS)

if __name__ == '__main__':
    # Inicialização
    logger.info("Iniciando aplicação v6...")
    
    # Carrega o PDF
    if os.path.exists(MD_PATH):
        md_text = extract_md_text(MD_PATH)
    else:
        logger.warning(f"Arquivo Markdown não encontrado: {MD_PATH}")
        md_text = "Arquivo Markdown não disponível"
    
    # Inicia o servidor
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Servidor iniciado na porta {port}")
    logger.info(f"Personas disponíveis: {list(PERSONAS.keys())}")
    app.run(host='0.0.0.0', port=port, debug=debug) 