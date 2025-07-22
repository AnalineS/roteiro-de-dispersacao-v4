"""
Interface Streamlit para o chatbot de Roteiro de Dispensação
"""

import streamlit as st
import requests
import os

# Configuração da página
st.set_page_config(
    page_title="Chatbot - Roteiro de Dispensação",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL do backend
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

def init_session_state():
    """Inicializa o estado da sessão"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_persona' not in st.session_state:
        st.session_state.current_persona = 'dr_gasnelio'
    if 'personas_info' not in st.session_state:
        st.session_state.personas_info = {}

def load_personas_info():
    """Carrega informações das personas do backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/personas", timeout=10)
        if response.status_code == 200:
            st.session_state.personas_info = response.json()
        else:
            st.error("Erro ao carregar informações das personas")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão com o backend: {str(e)}")

def send_message(message: str, persona: str) -> str:
    """Envia mensagem para o backend e retorna a resposta"""
    try:
        payload = {
            'message': message,
            'persona': persona
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('response', 'Erro: resposta vazia')
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            error_msg = error_data.get('error', f'Erro HTTP {response.status_code}')
            return f"Erro: {error_msg}"
            
    except requests.exceptions.Timeout:
        return "Erro: Timeout - o servidor demorou muito para responder"
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão: {str(e)}"
    except Exception as e:
        return f"Erro inesperado: {str(e)}"

def render_sidebar():
    """Renderiza a barra lateral com seleção de persona"""
    st.sidebar.title("🤖 Chatbot Configuração")
    
    # Seleção de persona
    st.sidebar.subheader("Escolha sua Persona")
    
    if st.session_state.personas_info:
        persona_options = {
            'dr_gasnelio': f"👨‍⚕️ {st.session_state.personas_info['dr_gasnelio']['name']} (Técnica)",
            'ga': f"😊 {st.session_state.personas_info['ga']['name']} (Leiga)"
        }
        
        selected_persona = st.sidebar.radio(
            "Selecione o estilo de conversa:",
            options=list(persona_options.keys()),
            format_func=lambda x: persona_options[x],
            index=0 if st.session_state.current_persona == 'dr_gasnelio' else 1
        )
        
        # Atualiza persona se mudou
        if selected_persona != st.session_state.current_persona:
            st.session_state.current_persona = selected_persona
            st.rerun()
        
        # Mostra descrição da persona atual
        current_info = st.session_state.personas_info[st.session_state.current_persona]
        st.sidebar.info(f"**{current_info['name']}**: {current_info['description']}")
    
    else:
        st.sidebar.error("Não foi possível carregar informações das personas")
    
    # Botão para limpar conversa
    if st.sidebar.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()
    
    # Informações sobre o projeto
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ Sobre o Projeto")
    st.sidebar.markdown("""
    Este chatbot utiliza inteligência artificial para responder perguntas sobre 
    o roteiro de dispensação baseado em uma tese de doutorado.
    
    **Tecnologias:**
    - RAG (Retrieval-Augmented Generation)
    - LangFlow
    - Kimie K2 via OpenRouter
    - FAISS para busca vetorial
    """)

def render_chat_interface():
    """Renderiza a interface principal do chat"""
    st.title("💊 Chatbot - Roteiro de Dispensação")
    
    # Mostra persona atual
    if st.session_state.personas_info:
        current_info = st.session_state.personas_info[st.session_state.current_persona]
        st.info(f"🤖 Conversando com: **{current_info['name']}** ({current_info['type']})")
    
    # Container para mensagens
    chat_container = st.container()
    
    with chat_container:
        # Exibe mensagens do histórico
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Input para nova mensagem
    if prompt := st.chat_input("Digite sua pergunta sobre roteiro de dispensação..."):
        # Adiciona mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        
        # Gera resposta do assistente
        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    response = send_message(prompt, st.session_state.current_persona)
                st.markdown(response)
        
        # Adiciona resposta ao histórico
        st.session_state.messages.append({"role": "assistant", "content": response})

def render_welcome_message():
    """Renderiza mensagem de boas-vindas se não há mensagens"""
    if not st.session_state.messages and st.session_state.personas_info:
        current_info = st.session_state.personas_info[st.session_state.current_persona]
        greeting = current_info.get('greeting', 'Olá! Como posso ajudá-lo?')
        
        with st.chat_message("assistant"):
            st.markdown(greeting)

def main():
    """Função principal"""
    init_session_state()
    
    # Carrega informações das personas na primeira execução
    if not st.session_state.personas_info:
        load_personas_info()
    
    # Renderiza interface
    render_sidebar()
    render_chat_interface()
    render_welcome_message()
    
    # Status do backend (debug)
    if st.sidebar.checkbox("Mostrar Status Debug"):
        try:
            health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if health_response.status_code == 200:
                st.sidebar.success("✅ Backend conectado")
                if st.sidebar.checkbox("Detalhes do Status"):
                    st.sidebar.json(health_response.json())
            else:
                st.sidebar.error("❌ Backend com problemas")
        except:
            st.sidebar.error("❌ Backend desconectado")

if __name__ == "__main__":
    main()

