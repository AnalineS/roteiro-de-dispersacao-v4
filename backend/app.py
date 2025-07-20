"""
Aplicação Flask principal para o backend do Roteiro de Dispersação v4
"""

import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from datetime import datetime

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa Flask
app = Flask(__name__)
CORS(app)  # Permite CORS para integração com frontend

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

# Importa módulos do projeto
from chatbot import ChatbotService
from personas import PersonaManager

# Inicializa serviços
chatbot_service = ChatbotService()
persona_manager = PersonaManager()

@app.route('/')
def index():
    """Página inicial do site"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check para o Render"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'roteiro-dispersacao-backend'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal do chatbot"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        message = data.get('message', '').strip()
        persona = data.get('persona', 'dr_gasnelio')  # default: técnica
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Valida persona
        if persona not in ['dr_gasnelio', 'ga']:
            return jsonify({'error': 'Invalid persona'}), 400
        
        logger.info(f"Chat request - Persona: {persona}, Message: {message[:50]}...")
        
        # Processa mensagem através do chatbot
        response = chatbot_service.process_message(message, persona)
        
        return jsonify({
            'response': response,
            'persona': persona,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/personas')
def get_personas():
    """Retorna informações sobre as personas disponíveis"""
    return jsonify(persona_manager.get_personas_info())

@app.route('/sobre')
def sobre():
    """Página sobre o projeto"""
    return render_template('sobre.html')

@app.route('/tese')
def tese():
    """Página sobre a tese"""
    return render_template('tese.html')

@app.route('/contato')
def contato():
    """Página de contato"""
    return render_template('contato.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])

