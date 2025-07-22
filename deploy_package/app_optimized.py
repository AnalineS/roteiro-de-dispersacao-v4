from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from transformers.pipelines import pipeline
import torch
import re
import logging
from datetime import datetime
import random
import requests

app = Flask(__name__)
CORS(app)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis globais
MD_PATH = 'PDFs/Roteiro de Dsispensação - Hanseníase.md'
md_text = ""
qa_pipeline = None
text_generation_pipeline = None
sentiment_pipeline = None
tokenizer = None
model = None

# Três chaves e modelos
OPENROUTER_API_KEY_LLAMA = os.environ.get("OPENROUTER_API_KEY_LLAMA", "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")
OPENROUTER_API_KEY_QWEN = os.environ.get("OPENROUTER_API_KEY_QWEN", "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")
OPENROUTER_API_KEY_GEMINI = os.environ.get("OPENROUTER_API_KEY_GEMINI", "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")
LLAMA3_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
QWEN_MODEL = "qwen/qwen3-14b:free"
GEMINI_MODEL = "google/gemini-2.0-flash-exp:free"

# Templates de linguagem natural para cada persona
NATURAL_TEMPLATES = {
    "dr_gasnelio": {
        "greeting": [
            "Saudações! Sou o Dr. Gasnelio. Minha pesquisa foca no roteiro de dispensação para a prática da farmácia clínica. Como posso auxiliá-lo hoje?",
            "Olá! Aqui é o Dr. Gasnelio. Tenho dedicado minha carreira ao estudo da dispensação farmacêutica. Em que posso ajudá-lo?",
            "Bem-vindo! Sou o Dr. Gasnelio, especialista em farmácia clínica. Como posso contribuir com sua consulta hoje?"
        ],
        "thinking": [
            "Deixe-me analisar essa questão com base na minha pesquisa...",
            "Interessante pergunta. Vou consultar os dados da tese...",
            "Essa é uma questão importante. Permita-me buscar nas fontes..."
        ],
        "confidence_high": [
            "Baseado na minha pesquisa, posso afirmar com confiança que:",
            "Os dados da tese são bastante claros sobre isso:",
            "Minha análise da literatura confirma que:"
        ],
        "confidence_medium": [
            "Com base no que encontrei na tese, posso sugerir que:",
            "Os dados disponíveis indicam que:",
            "Baseado na pesquisa, parece que:"
        ],
        "confidence_low": [
            "Essa questão é interessante, mas não encontrei dados específicos na tese. Sugiro consultar:",
            "Não tenho informações detalhadas sobre isso na pesquisa, mas posso orientar para:",
            "Essa área não foi coberta especificamente na tese, mas posso sugerir:"
        ]
    },
    "ga": {
        "greeting": [
            "Opa, tudo certo? Aqui é o Gá! Tô aqui pra gente desenrolar qualquer dúvida sobre o uso correto de medicamentos e o roteiro de dispensação. Manda a ver!",
            "E aí, beleza? Sou o Gá! Tô aqui pra te ajudar com qualquer parada sobre remédios e farmácia. Fala aí!",
            "Oi! Aqui é o Gá! Tô aqui pra gente conversar sobre medicamentos e como usar direitinho. Qual é a boa?"
        ],
        "thinking": [
            "Deixa eu dar uma olhada na tese aqui...",
            "Hmm, deixa eu ver o que tem sobre isso...",
            "Vou procurar essa informação pra você..."
        ],
        "confidence_high": [
            "Olha só, encontrei isso na tese:",
            "Tá aqui, direto da pesquisa:",
            "Dá uma olhada nisso que achei:"
        ],
        "confidence_medium": [
            "Olha, pelo que vi na tese:",
            "Acho que é mais ou menos assim:",
            "Pelo que entendi da pesquisa:"
        ],
        "confidence_low": [
            "Ih, essa eu não sei certinho, mas posso te ajudar a procurar!",
            "Não achei essa informação específica, mas posso te orientar!",
            "Essa parte não tá muito clara na tese, mas vamos ver o que tem!"
        ]
    }
}

def extract_md_text(md_path):
    """Extrai texto do arquivo Markdown"""
    global md_text
    try:
        with open(md_path, "r", encoding="utf-8") as file:
            text = file.read()
        logger.info(f"Arquivo Markdown extraído com sucesso. Total de caracteres: {len(text)}")
        return text
    except Exception as e:
        logger.error(f"Erro ao extrair arquivo Markdown: {e}")
        return ""

def load_ai_models():
    """Carrega múltiplos modelos de IA gratuitos do Hugging Face"""
    global qa_pipeline, text_generation_pipeline, sentiment_pipeline, tokenizer, model
    try:
        # Modelo principal para QA (mais robusto)
        model_name = "deepset/roberta-base-squad2"
        logger.info(f"Carregando modelo QA: {model_name}")
        
        qa_pipeline = pipeline(
            "question-answering",
            model=model_name,
            tokenizer=model_name,
            device=-1 if not torch.cuda.is_available() else 0
        )
        
        # Modelo para geração de texto (mais natural)
        generation_model = "microsoft/DialoGPT-medium"
        logger.info(f"Carregando modelo de geração: {generation_model}")
        
        text_generation_pipeline = pipeline(
            "text-generation",
            model=generation_model,
            tokenizer=generation_model,
            device=-1 if not torch.cuda.is_available() else 0,
            max_length=100,
            do_sample=True,
            temperature=0.7
        )
        
        # Modelo para análise de sentimento/contexto (comentado temporariamente)
        # sentiment_model = "cardiffnlp/twitter-roberta-base-sentiment"
        # logger.info(f"Carregando modelo de sentimento: {sentiment_model}")
        
        # sentiment_pipeline = pipeline(
        #     "sentiment-analysis",
        #     model=sentiment_model,
        #     device=-1 if not torch.cuda.is_available() else 0
        # )
        sentiment_pipeline = None
        
        logger.info("Todos os modelos carregados com sucesso")
    except Exception as e:
        logger.error(f"Erro ao carregar modelos: {e}")
        # Fallback para modelo único se houver erro
        try:
            qa_pipeline = pipeline(
                "question-answering",
                model="deepset/roberta-base-squad2",
                device=-1 if not torch.cuda.is_available() else 0
            )
        except Exception as e2:
            logger.error(f"Erro no fallback: {e2}")
            qa_pipeline = None

def get_natural_phrase(persona, category, confidence_level="medium"):
    """Retorna uma frase natural baseada na persona e contexto"""
    templates = NATURAL_TEMPLATES.get(persona, {})
    category_templates = templates.get(category, [])
    
    if category == "confidence":
        confidence_key = f"confidence_{confidence_level}"
        category_templates = templates.get(confidence_key, [])
    
    if category_templates:
        return random.choice(category_templates)
    return ""

def find_relevant_context_enhanced(question, full_text, max_length=800):
    """Encontra contexto mais relevante usando múltiplas estratégias"""
    # Divide o texto em chunks menores com overlap
    chunks = []
    chunk_size = 1000  # Aumentado para pegar mais contexto
    overlap = 300      # Aumentado o overlap
    
    for i in range(0, len(full_text), chunk_size - overlap):
        chunk = full_text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    
    if len(chunks) <= 2:
        return full_text[:max_length]
    
    # Busca por palavras-chave na pergunta
    question_words = set(re.findall(r'\w+', question.lower()))
    
    chunk_scores = []
    
    for chunk in chunks:
        chunk_words = set(re.findall(r'\w+', chunk.lower()))
        common_words = question_words.intersection(chunk_words)
        score = len(common_words) / len(question_words) if question_words else 0
        
        # Bônus para chunks que contêm termos médicos específicos
        medical_terms = ['medicamento', 'dose', 'tratamento', 'reação', 'efeito', 'hanseníase', 'clofazimina', 'rifampicina', 'dapsona', 'acompanhamento', 'dispensação', 'paciente']
        for term in medical_terms:
            if term in chunk.lower():
                score += 0.1
        
        chunk_scores.append((chunk, score))
    
    # Ordena por score e pega os melhores
    chunk_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Combina os 2 melhores chunks
    combined_context = ""
    for chunk, score in chunk_scores[:2]:
        if score > 0.05:  # Threshold mínimo
            combined_context += chunk + "\n\n"
    
    return combined_context[:max_length] if combined_context else chunks[0][:max_length]

def enhance_response_with_generation(base_answer, question, persona):
    """Melhora a resposta usando geração de texto natural"""
    if not text_generation_pipeline or not base_answer:
        return base_answer
    
    try:
        # Cria um prompt contextual
        if persona == "dr_gasnelio":
            prompt = f"Como um farmacêutico especialista, responda de forma técnica mas acessível: {question} Resposta base: {base_answer}"
        else:
            prompt = f"Como um farmacêutico amigável, explique de forma simples: {question} Resposta base: {base_answer}"
        
        # Gera texto complementar
        generated = text_generation_pipeline(
            prompt,
            max_length=len(prompt.split()) + 20,
            do_sample=True,
            temperature=0.6
        )
        
        if generated and len(generated) > 0:
            enhanced_text = generated[0]['generated_text']
            # Extrai apenas a parte gerada (remove o prompt)
            if len(enhanced_text) > len(prompt):
                new_content = enhanced_text[len(prompt):].strip()
                if new_content:
                    return f"{base_answer}\n\n{new_content}"
        
        return base_answer
    except Exception as e:
        logger.error(f"Erro na geração de texto: {e}")
        return base_answer

def answer_question_enhanced(question, persona, conversation_history=None):
    """Resposta aprimorada usando múltiplos modelos"""
    global qa_pipeline, md_text
    
    if not qa_pipeline or not md_text:
        return enhanced_fallback_response(question, persona, "")
    
    try:
        # Encontra contexto relevante
        context = find_relevant_context_enhanced(question, md_text)
        
        # Faz a pergunta ao modelo QA
        result = qa_pipeline(
            question=question,
            context=context,
            max_answer_len=300,
            handle_impossible_answer=True
        )
        
        # Acessa os resultados de forma segura
        if isinstance(result, dict):
            answer = result.get('answer', '').strip()
            confidence = result.get('score', 0.0)
        else:
            answer = ''
            confidence = 0.0
        
        logger.info(f"Pergunta: {question}")
        logger.info(f"Confiança QA: {confidence}")
        logger.info(f"Resposta base: {answer}")
        
        # Determina o nível de confiança
        if confidence > 0.6:
            confidence_level = "high"
        elif confidence > 0.3:
            confidence_level = "medium"
        else:
            confidence_level = "low"
        
        # Se a confiança for baixa ou resposta vazia, usa fallback aprimorado
        if not answer or confidence < 0.2:
            logger.info("Usando fallback aprimorado - confiança baixa")
            return enhanced_fallback_response(question, persona, context)
        
        # Melhora a resposta com geração de texto
        enhanced_answer = enhance_response_with_generation(answer, question, persona)
        
        # Formata com linguagem natural
        return format_persona_answer_enhanced(enhanced_answer, persona, confidence_level)
        
    except Exception as e:
        logger.error(f"Erro ao processar pergunta: {e}")
        return enhanced_fallback_response(question, persona, "")

def format_persona_answer_enhanced(answer, persona, confidence_level):
    """Formata a resposta com linguagem natural aprimorada"""
    
    # Pega frase de introdução baseada na confiança
    intro_phrase = get_natural_phrase(persona, "confidence", confidence_level)
    
    if persona == "dr_gasnelio":
        return {
            "answer": (
                f"Dr. Gasnelio responde:\n\n"
                f"{intro_phrase}\n\n"
                f"{answer}\n\n"
                f"*Baseado na minha tese sobre roteiro de dispensação para hanseníase. "
                f"Nível de confiança: {'Alto' if confidence_level == 'high' else 'Médio' if confidence_level == 'medium' else 'Baixo'}.*"
            ),
            "persona": "dr_gasnelio",
            "confidence": confidence_level
        }
    elif persona == "ga":
        # Transforma completamente a resposta para o Gá - mais descontraída e explicativa
        simple_answer = transform_for_ga(answer)
        return {
            "answer": (
                f"Gá responde:\n\n"
                f"{intro_phrase}\n\n"
                f"{simple_answer}\n\n"
                f"*Tá na tese, pode confiar! 😊*"
            ),
            "persona": "ga",
            "confidence": confidence_level
        }
    else:
        return {
            "answer": answer,
            "persona": "default",
            "confidence": confidence_level
        }

def transform_for_ga(text):
    """Transforma o texto técnico em linguagem descontraída e explicativa para o Gá"""
    # Remove aspas e formatações técnicas
    text = text.replace('"', '').replace('"', '').replace('"', '')
    
    # Simplifica termos técnicos
    replacements = {
        "dispensação": "entrega do remédio na farmácia",
        "medicamentos": "remédios",
        "posologia": "como tomar o remédio",
        "administração": "como usar o remédio",
        "reação adversa": "efeito colateral",
        "interação medicamentosa": "mistura de remédios que pode dar problema",
        "protocolo": "guia de cuidados",
        "orientação": "explicação",
        "adesão": "seguir direitinho o tratamento",
        "tratamento": "tratamento",
        "hanseníase": "hanseníase",
        "paciente": "pessoa que está tratando",
        "supervisionada": "com alguém olhando junto",
        "autoadministrada": "a própria pessoa toma sozinha",
        "prescrição": "receita do médico",
        "dose": "quantidade do remédio",
        "contraindicação": "quando não pode usar",
        "indicação": "quando é recomendado usar",
        "poliquimioterapia": "mistura de remédios",
        "rifampicina": "rifampicina",
        "clofazimina": "clofazimina",
        "dapsona": "dapsona",
        "mg": "miligramas",
        "dose mensal": "remédio que toma uma vez por mês",
        "dose diária": "remédio que toma todo dia",
        "supervisionada": "com alguém olhando",
        "autoadministrada": "a pessoa toma sozinha"
    }
    
    # Aplica as substituições
    for technical, simple in replacements.items():
        text = text.replace(technical, simple)
    
    # Adiciona expressões descontraídas
    casual_expressions = [
        "Olha só, ",
        "Então, ",
        "Tipo assim, ",
        "Sabe como é, ",
        "É o seguinte, ",
        "Fica ligado, ",
        "Cara, ",
        "Mano, ",
        "Beleza, ",
        "Tranquilo, "
    ]
    
    # Quebra o texto em frases e adiciona expressões casuais
    sentences = text.split('. ')
    if sentences and len(sentences) > 0:
        first_sentence = sentences[0]
        if not any(expr in first_sentence for expr in casual_expressions):
            sentences[0] = random.choice(casual_expressions) + first_sentence.lower()
    
    # Reconstrói o texto
    transformed_text = '. '.join(sentences)
    
    # Adiciona emojis e expressões informais
    emoji_replacements = {
        "importante": "importante ⚠️",
        "cuidado": "cuidado ⚠️",
        "atenção": "atenção 👀",
        "lembre": "lembre 💡",
        "consulte": "consulte 👨‍⚕️",
        "médico": "médico 👨‍⚕️",
        "farmacêutico": "farmacêutico 💊",
        "remédio": "remédio 💊",
        "tratamento": "tratamento 🏥"
    }
    
    for word, replacement in emoji_replacements.items():
        transformed_text = transformed_text.replace(word, replacement)
    
    return transformed_text

def enhanced_fallback_response(question, persona, context):
    """Fallback aprimorado que retorna trecho relevante do PDF"""
    logger.info("Executando fallback aprimorado")
    
    # Busca por palavras-chave na pergunta
    question_words = set(re.findall(r'\w+', question.lower()))
    
    # Divide o contexto em parágrafos
    paragraphs = context.split('\n\n') if context else md_text.split('\n\n')
    
    best_paragraph = None
    best_score = 0.0
    
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
            # Para o Dr. Gasnelio, retorna o parágrafo completo sem cortes
            complete_paragraph = best_paragraph.strip()
            
            # Se o parágrafo parece estar cortado, tenta encontrar o contexto completo
            if complete_paragraph.endswith('...') or len(complete_paragraph) < 100:
                # Busca por parágrafos relacionados
                related_paragraphs = []
                for para in paragraphs:
                    if any(word in para.lower() for word in question_words):
                        related_paragraphs.append(para.strip())
                
                if related_paragraphs:
                    complete_paragraph = '\n\n'.join(related_paragraphs[:2])  # Pega até 2 parágrafos relacionados
            
            return {
                "answer": (
                    f"Dr. Gasnelio responde:\n\n"
                    f"Baseado na minha tese sobre roteiro de dispensação para hanseníase, encontrei esta informação técnica relevante:\n\n"
                    f"\"{complete_paragraph}\"\n\n"
                    f"*Esta é uma extração direta do texto da tese. Para informações mais específicas, recomendo consultar a seção completa.*"
                ),
                "persona": "dr_gasnelio",
                "confidence": "low"
            }
        elif persona == "ga":
            # Transforma completamente para o Gá - não copia texto direto
            ga_explanation = explain_like_ga(best_paragraph.strip(), question)
            return {
                "answer": (
                    f"Gá responde:\n\n"
                    f"Olha só, encontrei algumas informações sobre isso na tese! 😊\n\n"
                    f"{ga_explanation}\n\n"
                    f"*Tá na tese, pode confiar! Mas se tiver dúvida, é só perguntar de novo! 😉*"
                ),
                "persona": "ga",
                "confidence": "low"
            }
        else:
            return {
                "answer": (
                    f"Encontrei esta informação na tese:\n\n"
                    f"\"{best_paragraph.strip()}\""
                ),
                "persona": "default",
                "confidence": "low"
            }
    
    # Se não encontrou nada relevante, usa fallback padrão
    logger.info("Nenhum parágrafo relevante encontrado, usando fallback padrão")
    return fallback_response(persona, "Informação não encontrada na tese")

def explain_like_ga(technical_text, question):
    """Explica o texto técnico de forma descontraída como o Gá faria"""
    
    # Identifica o tipo de pergunta para dar uma resposta mais contextual
    question_lower = question.lower()
    
    if "reação" in question_lower or "efeito" in question_lower or "colateral" in question_lower:
        return (
            "Cara, sobre efeitos colaterais, é sempre bom ficar ligado! ⚠️ "
            "Os remédios podem dar algumas reações, sabe? Tipo, pode dar dor de barriga, "
            "enjoo, ou até mudar a cor da pele. Mas não se preocupa, isso é normal! "
            "O importante é sempre conversar com o médico se sentir algo estranho. "
            "E lembra: cada pessoa reage diferente, então não se compara com os outros! 😊"
        )
    
    elif "dose" in question_lower or "como tomar" in question_lower or "posologia" in question_lower:
        return (
            "Beleza, sobre como tomar os remédios! 💊 "
            "Tem alguns que você toma todo dia, outros que toma uma vez por mês com alguém olhando. "
            "É tipo assim: alguns são pra tomar com comida, outros não podem tomar com suco de laranja. "
            "O importante é seguir direitinho o que o médico passou! "
            "Se esquecer de tomar, não se desespera, só toma quando lembrar. "
            "Mas se estiver muito perto da próxima dose, pula a que esqueceu! 😉"
        )
    
    elif "acompanhamento" in question_lower or "seguimento" in question_lower:
        return (
            "Então, sobre o acompanhamento! 👨‍⚕️ "
            "É super importante ir nas consultas direitinho, sabe? "
            "O médico vai ficar de olho pra ver se está tudo funcionando bem. "
            "Tem que fazer alguns exames também, pra garantir que está tudo certo. "
            "E se sentir qualquer coisa estranha, corre falar com eles! "
            "Não fica com vergonha de perguntar, eles estão lá pra isso! 😊"
        )
    
    elif "hanseníase" in question_lower or "tratamento" in question_lower:
        return (
            "Cara, sobre o tratamento da hanseníase! 🏥 "
            "É um tratamento que demora um pouco, mas funciona super bem! "
            "Você vai tomar alguns remédios juntos, tipo uma mistura. "
            "Alguns são pra tomar todo dia, outros uma vez por mês. "
            "O importante é não parar no meio, mesmo que melhore! "
            "Se parar, pode voltar pior. Então firmeza, vamo até o final! 💪"
        )
    
    else:
        # Resposta genérica mas descontraída
        return (
            "Olha só, encontrei algumas informações legais sobre isso! 💡 "
            "É sempre bom ficar ligado nos detalhes, sabe? "
            "Cada coisa tem seu jeito certo de fazer. "
            "Se tiver dúvida sobre algo específico, é só perguntar! "
            "Tô aqui pra ajudar! 😊"
        )

def fallback_response(persona, reason=""):
    """Resposta de fallback quando não encontra informação"""
    logger.info(f"Executando fallback padrão para persona: {persona}")
    
    if persona == "dr_gasnelio":
        return {
            "answer": (
                f"Dr. Gasnelio responde:\n\n"
                f"Não encontrei uma resposta exata na tese para sua pergunta. Recomendo consultar as seções de Segurança, Reações Adversas ou Interações para mais detalhes.\n\n"
                f"Se quiser, posso tentar explicar de outra forma ou buscar em outra parte do texto. Fique à vontade para perguntar novamente! {reason}"
            ),
            "persona": "dr_gasnelio",
            "confidence": "low"
        }
    elif persona == "ga":
        return {
            "answer": (
                f"Gá responde:\n\n"
                f"Ih, não achei uma resposta certinha na tese, mas posso te ajudar a procurar! Dá uma olhada nas partes de efeitos colaterais ou segurança, ou me pergunte de outro jeito que eu tento de novo! {reason}"
            ),
            "persona": "ga",
            "confidence": "low"
        }
    else:
        return {
            "answer": (
                f"Desculpe, não encontrei essa informação na tese. {reason}"
            ),
            "persona": "default",
            "confidence": "low"
        }

def call_openrouter_model(question, context, persona, model, api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Chatbot Tese Hanseniase"
    }
    if persona == "dr_gasnelio":
        system_prompt = (
            "Você é o Dr. Gasnelio, farmacêutico pesquisador, responde de forma técnica, formal e baseada em evidências. Use o contexto abaixo para responder de forma precisa e objetiva."
        )
    else:
        system_prompt = (
            "Você é a Gá, uma assistente amigável e didática. Explique de forma simples, acessível e acolhedora, usando o contexto abaixo."
        )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": f"{system_prompt}\n\nContexto:\n{context}"},
            {"role": "user", "content": question}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code != 200:
            raise Exception(f"Erro OpenRouter: {response.status_code} - {response.text}")
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        print(f"Erro ao chamar OpenRouter ({model}): {e}\nResposta: {getattr(e, 'response', None)}")
        return None

# Função principal com fallback (Llama -> Qwen -> Gemini)
def call_chatbot_with_fallback(question, context, persona):
    # 1. Llama
    resposta = call_openrouter_model(question, context, persona, LLAMA3_MODEL, OPENROUTER_API_KEY_LLAMA)
    if resposta:
        return resposta
    # 2. Qwen
    resposta = call_openrouter_model(question, context, persona, QWEN_MODEL, OPENROUTER_API_KEY_QWEN)
    if resposta:
        return resposta
    # 3. Gemini
    resposta = call_openrouter_model(question, context, persona, GEMINI_MODEL, OPENROUTER_API_KEY_GEMINI)
    if resposta:
        return resposta
    return "[Erro ao consultar os modelos OpenRouter. Por favor, tente novamente mais tarde.]"

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

@app.route('/test')
def test_page():
    """Página de teste"""
    return render_template('test_js.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        if not request.is_json:
            return jsonify({"error": "Requisição deve ser JSON"}), 400
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "JSON inválido ou vazio"}), 400
        question = data.get('question', '').strip()
        personality_id = data.get('personality_id', 'dr_gasnelio')
        if not question:
            return jsonify({"error": "Pergunta não fornecida"}), 400
        if personality_id not in ['dr_gasnelio', 'ga']:
            return jsonify({"error": "Personalidade inválida"}), 400
        # Extrai contexto relevante do Markdown
        context = find_relevant_context_enhanced(question, md_text, max_length=800)
        # Chama o modelo Llama-3 via OpenRouter
        resposta = call_chatbot_with_fallback(question, context, personality_id)
        return jsonify({"answer": resposta})
    except Exception as e:
        logger.error(f"Erro na API de chat: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificação de saúde da API"""
    return jsonify({
        "status": "healthy",
        "qa_model_loaded": qa_pipeline is not None,
        "generation_model_loaded": text_generation_pipeline is not None,
        "sentiment_model_loaded": sentiment_pipeline is not None,
        "md_loaded": len(md_text) > 0,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/info', methods=['GET'])
def api_info():
    """Informações sobre a API"""
    return jsonify({
        "name": "Chatbot Tese Hanseníase API - Versão Híbrida",
        "version": "3.0.0",
        "description": "API híbrida otimizada para chatbot baseado na tese sobre roteiro de dispensação para hanseníase, combinando múltiplos modelos de IA gratuitos",
        "personas": {
            "dr_gasnelio": "Professor sério e técnico",
            "ga": "Amigo descontraído que explica de forma simples"
        },
        "models": {
            "qa_model": "deepset/roberta-base-squad2",
            "generation_model": "microsoft/DialoGPT-medium",
            "sentiment_model": "cardiffnlp/twitter-roberta-base-sentiment"
        },
        "source": "Roteiro de Dispensação para Hanseníase (Markdown)",
        "features": [
            "Sistema híbrido com múltiplos modelos de IA",
            "Linguagem natural contextual para ambas as personas",
            "Geração de texto complementar",
            "Análise de sentimento para contexto",
            "Fallback aprimorado com trechos relevantes",
            "Simplificação automática para o Gá",
            "Contexto inteligente para perguntas"
        ]
    })

if __name__ == '__main__':
    # Inicialização
    logger.info("Iniciando aplicação híbrida otimizada...")
    
    # Carrega o arquivo Markdown
    if os.path.exists(MD_PATH):
        md_text = extract_md_text(MD_PATH)
    else:
        logger.warning(f"Arquivo Markdown não encontrado: {MD_PATH}")
        md_text = "Arquivo Markdown não disponível"
    
    # Carrega os modelos de IA
    load_ai_models()
    
    # Inicia o servidor
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Servidor híbrido otimizado iniciado na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) 