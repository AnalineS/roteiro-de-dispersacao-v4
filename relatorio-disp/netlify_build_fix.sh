#!/bin/bash

# Script de build personalizado para Netlify
# Resolve problemas de build e configura o ambiente

set -e  # Parar em caso de erro

echo "🔧 Iniciando build personalizado para Netlify..."

# Verificar se estamos no ambiente do Netlify
if [ -n "$NETLIFY" ]; then
    echo "✅ Ambiente Netlify detectado"
    echo "📊 Informações do build:"
    echo "   - Build ID: $NETLIFY_BUILD_ID"
    echo "   - Deploy URL: $NETLIFY_DEPLOY_URL"
    echo "   - Site ID: $NETLIFY_SITE_ID"
else
    echo "⚠️  Executando fora do ambiente Netlify"
fi

# Função para criar arquivo com conteúdo
create_file() {
    local file_path="$1"
    local content="$2"
    
    echo "📝 Criando $file_path..."
    mkdir -p "$(dirname "$file_path")"
    cat > "$file_path" << 'EOF'
$content
EOF
    echo "✅ $file_path criado"
}

# 1. Criar requirements.txt otimizado
if [ ! -f "requirements.txt" ]; then
    create_file "requirements.txt" "flask==2.3.3
flask-cors==4.0.0
transformers==4.35.0
torch==2.1.0
sentence-transformers==2.2.2
PyPDF2==3.0.1
numpy==1.24.3
requests==2.31.0
python-dotenv==1.0.0
huggingface-hub==0.19.4
scikit-learn==1.3.0
scipy==1.11.1
accelerate==0.24.1
tokenizers==0.15.0
protobuf==4.24.4
packaging==23.2
regex==2023.10.3
tqdm==4.66.1
safetensors==0.4.0
filelock==3.13.1
typing-extensions==4.8.0
sympy==1.12
networkx==3.2.1
mpmath==1.3.0
markdown-it-py==3.0.0
mdurl==0.1.2
pyyaml==6.0.1
fsspec==2023.10.0
jinja2==3.1.2
psutil==5.9.6
pandas==2.1.3
pytz==2023.3
six==1.16.0
python-dateutil==2.8.2
pytz-deprecation-shim==0.1.0.post0
tzdata==2023.3
urllib3==2.0.7
certifi==2023.11.17
charset-normalizer==3.3.2
idna==3.6"
else
    echo "✅ requirements.txt já existe"
fi

# 2. Criar pasta functions e api.py
if [ ! -d "functions" ]; then
    echo "📁 Criando pasta functions..."
    mkdir -p functions
fi

# 3. Criar functions/api.py otimizado
if [ ! -f "functions/api.py" ]; then
    create_file "functions/api.py" "import json
import os
import sys
import logging
from datetime import datetime
import numpy as np
import hashlib
import re
import traceback

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from transformers import pipeline
    import torch
    from sentence_transformers import SentenceTransformer
    import PyPDF2
    logger.info('✅ Todas as dependências importadas com sucesso')
except ImportError as e:
    logger.error(f'❌ Erro ao importar dependências: {e}')
    logger.error(f'Traceback: {traceback.format_exc()}')
    raise

class HanseniaseChatbot:
    def __init__(self):
        self.pdf_path = 'PDFs/Roteiro de Dsispensação - Hanseníase F.docx.pdf'
        self.qa_pipeline = None
        self.embedding_model = None
        self.cache = {}
        self.chunks = []
        self.synonyms = {
            'hanseníase': ['lepra', 'doença de hansen', 'mal de hansen'],
            'medicamento': ['fármaco', 'remédio', 'droga', 'medicação'],
            'tratamento': ['terapia', 'cura', 'medicação', 'tratar'],
            'sintoma': ['sinal', 'manifestação', 'indício', 'sintomas'],
            'diagnóstico': ['diagnosticar', 'identificar', 'detectar'],
            'contágio': ['transmissão', 'contaminação', 'infecção'],
            'prevenção': ['prevenir', 'evitar', 'proteger'],
            'cura': ['tratamento', 'recuperação', 'melhora'],
            'bacilo': ['bactéria', 'microorganismo', 'germe'],
            'lesão': ['ferida', 'machucado', 'dano', 'injury'],
            'nervo': ['nervoso', 'neural', 'neurológico'],
            'pele': ['cutâneo', 'dérmico', 'epidérmico'],
            'olho': ['ocular', 'visual', 'oftálmico'],
            'mão': ['manual', 'palmar', 'carpal'],
            'pé': ['pedal', 'plantar', 'podal'],
            'face': ['facial', 'rosto', 'cara'],
            'dor': ['doloroso', 'dolorido', 'dolor'],
            'formigamento': ['parestesia', 'adormecimento', 'dormência'],
            'dormência': ['anestesia', 'insensibilidade', 'formigamento'],
            'deformidade': ['deformação', 'alteração', 'mudança'],
            'úlcera': ['ferida', 'lesão', 'machucado'],
            'mancha': ['mácula', 'pigmentação', 'alteração cutânea'],
            'nódulo': ['caroço', 'protuberância', 'inchaço'],
            'infiltração': ['infiltrado', 'acúmulo', 'depósito'],
            'atrofia': ['diminuição', 'redução', 'perda'],
            'paralisia': ['paralisado', 'imobilidade', 'perda de movimento'],
            'anestesia': ['insensibilidade', 'perda de sensibilidade'],
            'hiperestesia': ['aumento de sensibilidade', 'hipersensibilidade'],
            'poliomielite': ['polio', 'paralisia infantil'],
            'tuberculose': ['tb', 'tbc', 'bacilo de koch'],
            'sífilis': ['lues', 'treponema pallidum'],
            'micose': ['fungo', 'infecção fúngica', 'dermatofitose']
        }
        self.load_models()
        self.load_pdf()
    
    def load_models(self):
        try:
            logger.info('Carregando modelos de IA...')
            
            # Configurar device
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            logger.info(f'Device set to use {device}')
            
            # Carregar modelo de embeddings
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
            
            # Carregar pipeline de QA
            self.qa_pipeline = pipeline(
                'question-answering',
                model='distilbert-base-cased-distilled-squad',
                device=0 if device == 'cuda' else -1
            )
            
            logger.info('✅ Modelos carregados com sucesso!')
            
        except Exception as e:
            logger.error(f'❌ Erro ao carregar modelos: {e}')
            logger.error(f'Traceback: {traceback.format_exc()}')
            raise
    
    def load_pdf(self):
        try:
            logger.info('Carregando PDF...')
            
            if not os.path.exists(self.pdf_path):
                logger.warning(f'⚠️ PDF não encontrado: {self.pdf_path}')
                # Criar chunks de exemplo se PDF não existir
                self.chunks = [
                    'Hanseníase é uma doença infecciosa crônica causada pela bactéria Mycobacterium leprae.',
                    'A hanseníase afeta principalmente a pele, nervos periféricos e mucosas.',
                    'O tratamento da hanseníase é feito com antibióticos específicos.',
                    'O diagnóstico precoce é fundamental para evitar sequelas.',
                    'A hanseníase tem cura quando tratada adequadamente.'
                ]
                logger.info(f'📚 Chunks de exemplo criados: {len(self.chunks)} chunks')
                return
            
            # Ler PDF
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            # Processar texto em chunks
            self.chunks = self.create_chunks(text)
            logger.info(f'📚 PDF carregado: {len(self.chunks)} chunks')
            
        except Exception as e:
            logger.error(f'❌ Erro ao carregar PDF: {e}')
            logger.error(f'Traceback: {traceback.format_exc()}')
            # Criar chunks de exemplo em caso de erro
            self.chunks = [
                'Hanseníase é uma doença infecciosa crônica causada pela bactéria Mycobacterium leprae.',
                'A hanseníase afeta principalmente a pele, nervos periféricos e mucosas.',
                'O tratamento da hanseníase é feito com antibióticos específicos.',
                'O diagnóstico precoce é fundamental para evitar sequelas.',
                'A hanseníase tem cura quando tratada adequadamente.'
            ]
            logger.info(f'📚 Chunks de exemplo criados: {len(self.chunks)} chunks')
    
    def create_chunks(self, text, chunk_size=1500, overlap=300):
        chunks = []
        
        # Limpar texto
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Dividir em parágrafos primeiro
        paragraphs = text.split('\n\n')
        
        current_chunk = ''
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Se o parágrafo é muito grande, dividir em frases
            if len(paragraph) > chunk_size:
                sentences = re.split(r'[.!?]+', paragraph)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    if len(current_chunk) + len(sentence) > chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            # Overlap com o final do chunk anterior
                            overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                            current_chunk = overlap_text + ' ' + sentence
                        else:
                            current_chunk = sentence
                    else:
                        current_chunk += ' ' + sentence
            else:
                if len(current_chunk) + len(paragraph) > chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                        # Overlap com o final do chunk anterior
                        overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                        current_chunk = overlap_text + ' ' + paragraph
                    else:
                        current_chunk = paragraph
                else:
                    current_chunk += ' ' + paragraph
        
        # Adicionar o último chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def expand_question_with_synonyms(self, question):
        expanded_questions = [question]
        
        question_lower = question.lower()
        
        for term, synonyms in self.synonyms.items():
            if term in question_lower:
                for synonym in synonyms:
                    new_question = question_lower.replace(term, synonym)
                    if new_question != question_lower:
                        expanded_questions.append(new_question)
        
        return expanded_questions[:3]  # Limitar a 3 variações
    
    def semantic_search(self, question, top_k=3):
        try:
            # Expandir pergunta com sinônimos
            expanded_questions = self.expand_question_with_synonyms(question)
            
            best_chunks = []
            best_scores = []
            
            for expanded_question in expanded_questions:
                # Calcular embeddings
                question_embedding = self.embedding_model.encode([expanded_question])
                chunk_embeddings = self.embedding_model.encode(self.chunks)
                
                # Calcular similaridade
                similarities = np.dot(chunk_embeddings, question_embedding.T).flatten()
                
                # Busca por palavras-chave também
                keyword_scores = []
                for chunk in self.chunks:
                    chunk_lower = chunk.lower()
                    score = 0
                    for term, synonyms in self.synonyms.items():
                        if term in chunk_lower or any(syn in chunk_lower for syn in synonyms):
                            score += 1
                    keyword_scores.append(score)
                
                # Combinar scores
                combined_scores = similarities + np.array(keyword_scores) * 0.1
                
                # Pegar os melhores chunks
                top_indices = np.argsort(combined_scores)[-top_k:][::-1]
                
                for idx in top_indices:
                    if combined_scores[idx] > 0.3:  # Threshold de confiança
                        if idx not in [c[0] for c in best_chunks]:
                            best_chunks.append((idx, self.chunks[idx], combined_scores[idx]))
                            best_scores.append(combined_scores[idx])
            
            # Ordenar por score e retornar os melhores
            best_chunks.sort(key=lambda x: x[2], reverse=True)
            return [chunk[1] for chunk in best_chunks[:top_k]], max(best_scores) if best_scores else 0
            
        except Exception as e:
            logger.error(f'❌ Erro na busca semântica: {e}')
            return [], 0
    
    def extract_context(self, relevant_chunks, question):
        context = ' '.join(relevant_chunks)
        
        # Limitar contexto se muito longo
        if len(context) > 3000:
            # Priorizar chunks com mais palavras-chave da pergunta
            question_words = set(question.lower().split())
            chunk_scores = []
            
            for chunk in relevant_chunks:
                chunk_words = set(chunk.lower().split())
                score = len(question_words.intersection(chunk_words))
                chunk_scores.append((score, chunk))
            
            chunk_scores.sort(reverse=True)
            context = ' '.join([chunk for _, chunk in chunk_scores[:2]])
        
        return context
    
    def generate_response(self, question, context, persona='dr_gasnelio'):
        try:
            # Preparar prompt baseado na personalidade
            if persona == 'dr_gasnelio':
                prompt = f'''Como Dr. Gasnelio, um especialista técnico em hanseníase, responda de forma científica e detalhada:

Contexto: {context}

Pergunta: {question}

Resposta técnica:'''
            else:  # persona == 'ga'
                prompt = f'''Como Gá, um profissional descontraído mas competente, responda de forma amigável e acessível:

Contexto: {context}

Pergunta: {question}

Resposta amigável:'''
            
            # Usar o pipeline de QA
            result = self.qa_pipeline(
                question=question,
                context=context,
                max_answer_len=200,
                handle_impossible_answer=True
            )
            
            answer = result['answer']
            confidence = result['score']
            
            # Se a confiança for baixa, tentar extrair informações do contexto
            if confidence < 0.3:
                # Buscar frases relevantes no contexto
                relevant_sentences = []
                sentences = re.split(r'[.!?]+', context)
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) > 20:
                        sentence_lower = sentence.lower()
                        question_lower = question.lower()
                        
                        # Verificar se a frase contém palavras da pergunta
                        question_words = set(question_lower.split())
                        sentence_words = set(sentence_lower.split())
                        
                        if len(question_words.intersection(sentence_words)) > 0:
                            relevant_sentences.append(sentence)
                
                if relevant_sentences:
                    answer = ' '.join(relevant_sentences[:2])
                    confidence = 0.2  # Confiança baixa mas não zero
            
            return answer, confidence
            
        except Exception as e:
            logger.error(f'❌ Erro ao gerar resposta: {e}')
            return 'Desculpe, não consegui processar sua pergunta no momento.', 0.0
    
    def get_cached_response(self, question_hash):
        return self.cache.get(question_hash)
    
    def cache_response(self, question_hash, response):
        self.cache[question_hash] = response
    
    def answer_question(self, question, persona='dr_gasnelio'):
        try:
            # Criar hash da pergunta para cache
            question_hash = hashlib.md5(question.encode()).hexdigest()
            
            # Verificar cache
            cached_response = self.get_cached_response(question_hash)
            if cached_response:
                return cached_response
            
            # Busca semântica
            relevant_chunks, search_confidence = self.semantic_search(question)
            
            if not relevant_chunks or search_confidence < 0.3:
                # Tentar busca mais ampla
                expanded_questions = self.expand_question_with_synonyms(question)
                for expanded_question in expanded_questions[1:]:
                    relevant_chunks, search_confidence = self.semantic_search(expanded_question)
                    if relevant_chunks and search_confidence >= 0.2:
                        break
            
            if not relevant_chunks:
                response = {
                    'answer': 'Desculpe, não encontrei informações específicas sobre isso no material disponível. Pode reformular sua pergunta ou perguntar sobre outro aspecto da hanseníase?',
                    'confidence': 0.0,
                    'source': 'Nenhuma fonte encontrada'
                }
                self.cache_response(question_hash, response)
                return response
            
            # Extrair contexto
            context = self.extract_context(relevant_chunks, question)
            
            # Gerar resposta
            answer, answer_confidence = self.generate_response(question, context, persona)
            
            # Calcular confiança final
            final_confidence = (search_confidence + answer_confidence) / 2
            
            # Preparar resposta
            response = {
                'answer': answer,
                'confidence': final_confidence,
                'source': f'Baseado em {len(relevant_chunks)} trechos do material de referência',
                'search_confidence': search_confidence,
                'answer_confidence': answer_confidence
            }
            
            # Cache da resposta
            self.cache_response(question_hash, response)
            
            return response
            
        except Exception as e:
            logger.error(f'❌ Erro ao responder pergunta: {e}')
            return {
                'answer': 'Ocorreu um erro ao processar sua pergunta. Tente novamente.',
                'confidence': 0.0,
                'source': 'Erro interno'
            }

# Instância global do chatbot
chatbot = None

def handler(event, context):
    global chatbot
    
    try:
        # Configurar CORS
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        }
        
        # Responder a requisições OPTIONS (preflight)
        if event['httpMethod'] == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Verificar método HTTP
        if event['httpMethod'] != 'POST':
            return {
                'statusCode': 405,
                'headers': headers,
                'body': json.dumps({'error': 'Método não permitido'})
            }
        
        # Inicializar chatbot se necessário
        if chatbot is None:
            logger.info('🚀 Inicializando chatbot...')
            chatbot = HanseniaseChatbot()
            logger.info('✅ Chatbot inicializado com sucesso!')
        
        # Parse do JSON
        try:
            body = json.loads(event['body'])
            question = body.get('question', '').strip()
            persona = body.get('persona', 'dr_gasnelio')
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'JSON inválido'})
            }
        
        # Validar pergunta
        if not question:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Pergunta é obrigatória'})
            }
        
        # Responder pergunta
        logger.info(f'🤔 Processando pergunta: {question[:50]}...')
        response = chatbot.answer_question(question, persona)
        logger.info(f'✅ Resposta gerada com confiança: {response.get("confidence", 0):.2f}')
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response, ensure_ascii=False)
        }
        
    except Exception as e:
        logger.error(f'❌ Erro no handler: {e}')
        logger.error(f'Traceback: {traceback.format_exc()}')
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Erro interno do servidor',
                'message': str(e)
            })
        }"
else
    echo "✅ functions/api.py já existe"
fi

# 4. Criar netlify.toml otimizado
if [ ! -f "netlify.toml" ]; then
    create_file "netlify.toml" "[build]
  publish = \".\"
  command = \"bash netlify_build_fix.sh\"
  functions = \"functions\"

[[redirects]]
  from = \"/api/*\"
  to = \"/.netlify/functions/api/:splat\"
  status = 200
  force = true

[[redirects]]
  from = \"/*\"
  to = \"/index.html\"
  status = 200

[build.environment]
  PYTHON_VERSION = \"3.9\"
  NODE_VERSION = \"18\"
  ENABLE_SYNONYMS = \"true\"
  ENABLE_CONTEXT_EXTRACTION = \"true\"
  CONFIDENCE_THRESHOLD = \"0.3\"
  MAX_CHUNKS = \"3\"
  CHUNK_SIZE = \"1500\"
  CHUNK_OVERLAP = \"300\"

[functions]
  directory = \"functions\"
  node_bundler = \"esbuild\"
  included_files = [\"PDFs/**/*\"]
  external_node_modules = [\"@netlify/functions\"]

[[headers]]
  for = \"/api/*\"
  [headers.values]
    Access-Control-Allow-Origin = \"*\"
    Access-Control-Allow-Headers = \"Content-Type\"
    Access-Control-Allow-Methods = \"POST, OPTIONS\""
else
    echo "✅ netlify.toml já existe"
fi

# 5. Criar index.html otimizado
if [ ! -f "index.html" ]; then
    create_file "index.html" "<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Chatbot Hanseníase</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .chat-container {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            background: #f9f9f9;
        }
        .message {
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background: #007bff;
            color: white;
            margin-left: auto;
        }
        .bot-message {
            background: #e9ecef;
            color: #333;
        }
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #ddd;
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        input[type=\"text\"] {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
        }
        button {
            padding: 12px 25px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #45a049;
        }
        .persona-selector {
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-bottom: 1px solid #ddd;
        }
        .persona-btn {
            margin: 0 10px;
            padding: 8px 20px;
            border: 2px solid #4CAF50;
            background: white;
            color: #4CAF50;
            border-radius: 20px;
            cursor: pointer;
        }
        .persona-btn.active {
            background: #4CAF50;
            color: white;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #4CAF50;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class=\"container\">
        <div class=\"header\">
            <h1>🏥 Chatbot Hanseníase</h1>
            <p>Especialista em informações sobre hanseníase</p>
        </div>
        
        <div class=\"persona-selector\">
            <button class=\"persona-btn active\" onclick=\"setPersona('dr_gasnelio')\">👨‍⚕️ Dr. Gasnelio (Técnico)</button>
            <button class=\"persona-btn\" onclick=\"setPersona('ga')\">😊 Gá (Descontraído)</button>
        </div>
        
        <div class=\"chat-container\" id=\"chatContainer\">
            <div class=\"message bot-message\">
                Olá! Sou o chatbot especialista em hanseníase. Como posso ajudá-lo hoje?
            </div>
        </div>
        
        <div class=\"input-container\">
            <div class=\"input-group\">
                <input type=\"text\" id=\"userInput\" placeholder=\"Digite sua pergunta sobre hanseníase...\" onkeypress=\"handleKeyPress(event)\">
                <button onclick=\"sendMessage()\">Enviar</button>
            </div>
        </div>
    </div>

    <script>
        let currentPersona = 'dr_gasnelio';
        
        function setPersona(persona) {
            currentPersona = persona;
            document.querySelectorAll('.persona-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Adicionar mensagem do usuário
            addMessage(message, 'user');
            input.value = '';
            
            // Mostrar loading
            const loadingId = addMessage('<div class=\"loading\"></div> Processando...', 'bot');
            
            try {
                const response = await fetch('/.netlify/functions/api', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        question: message,
                        persona: currentPersona
                    })
                });
                
                const data = await response.json();
                
                // Remover loading
                removeMessage(loadingId);
                
                if (data.error) {
                    addMessage(`❌ Erro: ${data.error}`, 'bot');
                } else {
                    addMessage(data.answer, 'bot');
                }
                
            } catch (error) {
                removeMessage(loadingId);
                addMessage('❌ Erro de conexão. Tente novamente.', 'bot');
                console.error('Erro:', error);
            }
        }
        
        function addMessage(text, type) {
            const container = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            const messageId = Date.now();
            messageDiv.id = `msg-${messageId}`;
            messageDiv.className = `message ${type}-message`;
            messageDiv.innerHTML = text;
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
            return messageId;
        }
        
        function removeMessage(messageId) {
            const message = document.getElementById(`msg-${messageId}`);
            if (message) {
                message.remove();
            }
        }
    </script>
</body>
</html>"
else
    echo "✅ index.html já existe"
fi

# 6. Criar pasta PDFs se não existir
if [ ! -d "PDFs" ]; then
    echo "📁 Criando pasta PDFs..."
    mkdir -p PDFs
    echo "⚠️  ATENÇÃO: Adicione o PDF da tese na pasta PDFs/"
fi

# 7. Criar arquivo .gitignore
if [ ! -f ".gitignore" ]; then
    create_file ".gitignore" "# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Cache
.cache/
*.cache

# Netlify
.netlify/

# Temporary files
*.tmp
*.temp"
else
    echo "✅ .gitignore já existe"
fi

# 8. Criar arquivo runtime.txt para especificar versão do Python
if [ ! -f "runtime.txt" ]; then
    create_file "runtime.txt" "python-3.9.18"
else
    echo "✅ runtime.txt já existe"
fi

# 9. Criar arquivo .python-version
if [ ! -f ".python-version" ]; then
    create_file ".python-version" "3.9.18"
else
    echo "✅ .python-version já existe"
fi

echo "✅ Build personalizado concluído!"
echo "🚀 Arquivos criados/verificados:"
echo "   - requirements.txt (dependências Python)"
echo "   - functions/api.py (API do chatbot)"
echo "   - netlify.toml (configuração do Netlify)"
echo "   - index.html (interface do usuário)"
echo "   - pasta PDFs/ (para o arquivo da tese)"
echo "   - .gitignore (arquivos ignorados)"
echo "   - runtime.txt (versão do Python)"
echo "   - .python-version (versão do Python)"

# Verificar se estamos no ambiente do Netlify
if [ -n "$NETLIFY" ]; then
    echo "🌐 Ambiente Netlify detectado - instalando dependências..."
    
    # Instalar dependências Python
    echo "📦 Instalando dependências Python..."
    pip install -r requirements.txt --quiet
    
    echo "🎉 Deploy pronto! O Netlify deve conseguir fazer o build agora."
else
    echo "💻 Ambiente local - para testar localmente:"
    echo "   1. Adicione o PDF na pasta PDFs/"
    echo "   2. Execute: python -m flask run"
    echo "   3. Acesse: http://localhost:5000"
fi

echo "✅ Script netlify_build_fix.sh executado com sucesso!" 