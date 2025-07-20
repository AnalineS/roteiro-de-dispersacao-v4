#!/usr/bin/env python3
"""
Interface Streamlit Amigável para o Roteiro de Dispensação
Inspirada no design do site original
"""

import streamlit as st
import uuid
import time
import logging
import os
from typing import List, Dict, Any
from datetime import datetime
import sys

# Adicionar diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar pipeline RAG
from rag_pipeline import RAGPipeline

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da página
st.set_page_config(
    page_title="Roteiro de Dispensação - Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado inspirado no site original
st.markdown("""
<style>
    /* Importar fonte similar */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset e configurações globais */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 600;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Navegação */
    .nav-header {
        background: white;
        padding: 1rem 0;
        margin: -1rem -1rem 1rem -1rem;
        border-bottom: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        color: #2c3e50;
        font-size: 1.1rem;
    }
    
    .nav-brand .logo {
        background: #27ae60;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    
    /* Seção do chatbot */
    .chatbot-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .chatbot-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .chatbot-description {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Card do Dr. Gasnelio */
    .doctor-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
    
    .doctor-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .doctor-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
        font-weight: 600;
    }
    
    .doctor-info h3 {
        margin: 0;
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .doctor-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.3rem 0;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: #27ae60;
        border-radius: 50%;
    }
    
    .status-text {
        color: #27ae60;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Mensagens do chat */
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .chat-message {
        margin: 1rem 0;
        display: flex;
        gap: 0.8rem;
    }
    
    .message-user {
        justify-content: flex-end;
    }
    
    .message-bubble {
        max-width: 70%;
        padding: 0.8rem 1rem;
        border-radius: 18px;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    
    .bubble-user {
        background: #3498db;
        color: white;
        border-bottom-right-radius: 6px;
    }
    
    .bubble-bot {
        background: white;
        color: #2c3e50;
        border: 1px solid #e0e0e0;
        border-bottom-left-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .message-time {
        font-size: 0.75rem;
        color: #999;
        margin-top: 0.3rem;
    }
    
    /* Botões */
    .btn-primary {
        background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .btn-primary:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .btn-secondary {
        background: linear-gradient(135deg, #16a085 0%, #1abc9c 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 6px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0.3rem;
    }
    
    /* Cards de exemplo */
    .example-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .example-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .example-card:hover {
        border-color: #3498db;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.15);
        transform: translateY(-2px);
    }
    
    .example-card h4 {
        color: #2c3e50;
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .example-card p {
        color: #666;
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Sidebar */
    .sidebar-content {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Input personalizado */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem 1.2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    /* Esconder elementos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsividade */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .example-cards {
            grid-template-columns: 1fr;
        }
        
        .message-bubble {
            max-width: 85%;
        }
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Inicializa variáveis de sessão"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'rag_pipeline' not in st.session_state:
        with st.spinner("🚀 Inicializando Dr. Gasnelio..."):
            try:
                st.session_state.rag_pipeline = RAGPipeline()
                st.success("✅ Dr. Gasnelio está pronto para conversar!")
                time.sleep(1)
            except Exception as e:
                st.error(f"❌ Erro ao inicializar: {e}")
                st.session_state.rag_pipeline = None
    
    if 'current_persona' not in st.session_state:
        st.session_state.current_persona = "Professor"
    
    if 'total_queries' not in st.session_state:
        st.session_state.total_queries = 0


def display_header():
    """Exibe o header principal"""
    st.markdown("""
    <div class="nav-header">
        <div class="nav-brand">
            <span class="logo">UnB</span>
            Roteiro de Dispensação
        </div>
    </div>
    
    <div class="main-header">
        <h1 class="main-title">Roteiro de Dispensação</h1>
        <p class="main-subtitle">Uma tese de doutorado sobre a otimização do cuidado farmacêutico.</p>
    </div>
    """, unsafe_allow_html=True)


def display_doctor_card():
    """Exibe o card do Dr. Gasnelio"""
    st.markdown("""
    <div class="doctor-card">
        <div class="doctor-header">
            <div class="doctor-avatar">DG</div>
            <div class="doctor-info">
                <h3>Dr. Gasnelio</h3>
                <div class="doctor-status">
                    <span class="status-dot"></span>
                    <span class="status-text">Online</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_chat_message(message: Dict[str, Any], is_user: bool = False):
    """Exibe uma mensagem do chat"""
    css_class = "message-user" if is_user else ""
    bubble_class = "bubble-user" if is_user else "bubble-bot"
    
    timestamp = ""
    if 'timestamp' in message:
        dt = datetime.fromtimestamp(message['timestamp'])
        timestamp = dt.strftime('%H:%M')
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <div class="message-bubble {bubble_class}">
            {message['content']}
            <div class="message-time">{timestamp}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_example_questions():
    """Exibe exemplos de perguntas"""
    st.markdown("### 💡 Exemplos de Perguntas")
    
    examples = [
        {
            "title": "Sobre o Roteiro",
            "question": "O que é roteiro de dispensação?",
            "description": "Entenda os conceitos fundamentais"
        },
        {
            "title": "Metodologia",
            "question": "Como foi validado o roteiro?",
            "description": "Processo de validação por especialistas"
        },
        {
            "title": "Aplicação Prática",
            "question": "Como aplicar o roteiro na prática?",
            "description": "Orientações para implementação"
        },
        {
            "title": "Resultados",
            "question": "Quais foram os principais resultados?",
            "description": "Descobertas e conclusões da pesquisa"
        },
        {
            "title": "Farmácia Clínica",
            "question": "Como melhorar o cuidado farmacêutico?",
            "description": "Estratégias para otimização"
        },
        {
            "title": "Adesão ao Tratamento",
            "question": "Como aumentar a adesão dos pacientes?",
            "description": "Técnicas de comunicação eficaz"
        }
    ]
    
    # Criar grid de exemplos
    cols = st.columns(3)
    for i, example in enumerate(examples):
        with cols[i % 3]:
            if st.button(
                f"**{example['title']}**\n\n{example['description']}", 
                key=f"example_{i}",
                help=example['question']
            ):
                # Adicionar pergunta às mensagens
                st.session_state.messages.append({
                    'role': 'user',
                    'content': example['question'],
                    'timestamp': time.time()
                })
                st.session_state.total_queries += 1
                st.rerun()


def generate_response(query: str) -> Dict[str, Any]:
    """Gera resposta usando o pipeline RAG"""
    if not st.session_state.rag_pipeline:
        return {
            "answer": "Desculpe, o Dr. Gasnelio não está disponível no momento. Tente novamente mais tarde.",
            "sources": []
        }
    
    try:
        # Buscar no pipeline RAG
        result = st.session_state.rag_pipeline.query(query)
        
        # Personalizar resposta baseada na persona
        if st.session_state.current_persona == "Amigável":
            base_answer = result.get('answer', 'Não encontrei informações específicas sobre isso.')
            if base_answer == "Não encontrei informações relevantes para responder sua pergunta.":
                answer = """Olá! 😊 
                
Essa é uma ótima pergunta! Embora eu não tenha informações específicas sobre isso na minha base de conhecimento atual, posso te ajudar com questões sobre:

• **Roteiro de dispensação** e sua aplicação prática
• **Cuidado farmacêutico** e comunicação com pacientes  
• **Metodologia de pesquisa** utilizada na tese
• **Validação por especialistas** e resultados obtidos

Que tal reformular sua pergunta ou escolher um dos exemplos acima? Estou aqui para ajudar! 🏥"""
            else:
                answer = f"Ótima pergunta! 😊\n\n{base_answer}\n\nEspero ter esclarecido sua dúvida! Se precisar de mais detalhes, é só perguntar. 🏥"
        else:
            # Modo Professor - mais técnico
            answer = result.get('answer', 'Não encontrei informações relevantes para responder sua pergunta.')
            if answer == "Não encontrei informações relevantes para responder sua pergunta.":
                answer = """Saudações! Sou o Dr. Gasnelio. 

Sua pergunta é interessante, porém não localizei informações específicas em minha base de conhecimento atual sobre este tópico.

Minha expertise está focada em:
• Roteiro de dispensação farmacêutica
• Metodologias de validação por especialistas
• Cuidado farmacêutico centrado no paciente
• Comunicação clínica estruturada

Poderia reformular sua questão direcionando-a para estes temas? Assim poderei fornecer uma resposta mais precisa e fundamentada."""
        
        return {
            "answer": answer,
            "sources": result.get('sources', [])
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar resposta: {e}")
        return {
            "answer": "Desculpe, ocorreu um erro técnico. Tente novamente em alguns instantes.",
            "sources": []
        }


def main():
    """Função principal da aplicação"""
    initialize_session_state()
    
    # Header
    display_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        st.subheader("⚙️ Configurações")
        
        # Seletor de persona
        persona = st.radio(
            "**Modo de Conversa**",
            ["Professor", "Amigável"],
            index=0 if st.session_state.current_persona == "Professor" else 1,
            help="**Professor**: Respostas técnicas e acadêmicas\n**Amigável**: Explicações simples e acessíveis"
        )
        
        if persona != st.session_state.current_persona:
            st.session_state.current_persona = persona
            st.rerun()
        
        st.markdown("---")
        
        # Estatísticas
        st.subheader("📊 Estatísticas")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Mensagens", len(st.session_state.messages))
        with col2:
            st.metric("Consultas", st.session_state.total_queries)
        
        st.markdown("---")
        
        # Controles
        st.subheader("🔧 Controles")
        if st.button("🗑️ Limpar Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("🔄 Nova Sessão", type="secondary"):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.total_queries = 0
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Seção principal do chatbot
    st.markdown("""
    <div class="chatbot-section">
        <h2 class="chatbot-title">Conheça o Dr. Gasnelio</h2>
        <p class="chatbot-description">
            Meu assistente de IA, treinado com o conteúdo desta tese. Ele pode responder 
            dúvidas sobre o roteiro de dispensação, seus métodos, resultados ou qualquer 
            outro aspecto da pesquisa. Escolha uma persona e interaja!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Card do Dr. Gasnelio
    display_doctor_card()
    
    # Container do chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Mensagem inicial se não houver mensagens
    if len(st.session_state.messages) == 0:
        if st.session_state.current_persona == "Professor":
            initial_message = """Saudações! Sou o Dr. Gasnelio. Minha pesquisa foca no roteiro de dispensação para a prática da farmácia clínica. Como posso auxiliá-lo hoje?"""
        else:
            initial_message = """Olá! 😊 Eu sou o Dr. Gasnelio! Estou aqui para conversar sobre roteiro de dispensação de medicamentos de forma simples e clara. Como posso te ajudar hoje?"""
        
        st.markdown(f"""
        <div class="chat-message">
            <div class="message-bubble bubble-bot">
                {initial_message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Exibir mensagens existentes
    for message in st.session_state.messages:
        if message['role'] == 'user':
            display_chat_message(message, is_user=True)
        else:
            display_chat_message(message)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input para nova mensagem
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Digite sua pergunta sobre roteiro de dispensação:",
                placeholder="Ex: Como aplicar o roteiro na prática farmacêutica?",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button("💬 Enviar", type="primary")
    
    # Processar nova mensagem
    if submit_button and user_input.strip():
        # Adicionar mensagem do usuário
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': time.time()
        })
        
        # Incrementar contador
        st.session_state.total_queries += 1
        
        # Gerar resposta
        with st.spinner(f"🤔 Dr. Gasnelio está pensando..."):
            response_data = generate_response(user_input)
            
            # Adicionar resposta do bot
            st.session_state.messages.append({
                'role': 'assistant',
                'content': response_data['answer'],
                'sources': response_data['sources'],
                'timestamp': time.time()
            })
        
        # Recarregar para mostrar nova mensagem
        st.rerun()
    
    # Exemplos de perguntas (apenas se não houver mensagens)
    if len(st.session_state.messages) == 0:
        display_example_questions()


if __name__ == "__main__":
    main()

