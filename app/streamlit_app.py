"""
Interface Streamlit para o chatbot de roteiro de dispersão
"""

import logging
import time
import uuid
from typing import Dict

import streamlit as st
from config.settings import settings

from app.rag_system import get_rag_system

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da página
st.set_page_config(
    page_title="Roteiro de Dispersão Bot v4",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f1f8e9;
        border-left: 4px solid #4caf50;
    }
    .persona-selector {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Inicializa variáveis de sessão"""
    # Decisão de design: usar session_state do Streamlit para manter contexto entre interações do usuário.
    # Permite persistir histórico de mensagens, persona selecionada e instância do sistema RAG.
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "rag_system" not in st.session_state:
        with st.spinner("Inicializando sistema RAG..."):
            st.session_state.rag_system = get_rag_system()

    if "current_persona" not in st.session_state:
        st.session_state.current_persona = "Dr. Gasnelio"


def display_chat_message(message: Dict[str, str], is_user: bool = False):
    """Exibe uma mensagem do chat"""
    css_class = "user-message" if is_user else "bot-message"
    role = "Você" if is_user else message.get("persona", "Bot")

    st.markdown(
        f"""
    <div class="chat-message {css_class}">
        <strong>{role}:</strong><br>
        {message['content']}
    </div>
    """,
        unsafe_allow_html=True,
    )


def main():
    """Função principal da aplicação"""
    initialize_session_state()

    # Header customizado com CSS para identidade visual.
    st.markdown(
        '<h1 class="main-header">🌪️ Roteiro de Dispersão Bot v4</h1>',
        unsafe_allow_html=True,
    )

    # Sidebar com seleção de persona, informações da sessão e botões de controle.
    with st.sidebar:
        st.header("⚙️ Configurações")

        # Seletor de persona: permite ao usuário alternar entre respostas técnicas e amigáveis.
        st.markdown('<div class="persona-selector">', unsafe_allow_html=True)
        st.subheader("👤 Escolha a Persona")

        persona = st.radio(
            "Selecione o estilo de resposta:",
            ["Dr. Gasnelio", "Gá"],
            index=0 if st.session_state.current_persona == "Dr. Gasnelio" else 1,
            help="Dr. Gasnelio: Respostas técnicas e precisas\nGá: Explicações simples e acessíveis",
        )

        if persona != st.session_state.current_persona:
            st.session_state.current_persona = persona
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # Informações da sessão e botão para limpar histórico.
        st.subheader("📊 Informações da Sessão")
        st.text(f"ID: {st.session_state.session_id[:8]}...")
        st.text(f"Mensagens: {len(st.session_state.messages)}")
        st.text(f"Persona: {st.session_state.current_persona}")

        if st.button("🗑️ Limpar Chat", type="secondary"):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()

        # Informações do sistema e tecnologias utilizadas.
        st.subheader("ℹ️ Sobre o Sistema")
        st.info(
            f"""
        **Versão:** {settings.APP_VERSION}
        
        **Tecnologias:**
        - RAG com FAISS
        - LangFlow
        - Astra DB
        - OpenRouter (Claude-3)
        
        **Personas:**
        - **Dr. Gasnelio**: Especialista técnico
        - **Gá**: Assistente amigável
        """
        )

    # Área principal do chat: exibe histórico e permite envio de novas mensagens.
    st.subheader(f"💬 Chat com {st.session_state.current_persona}")

    # Container para mensagens do chat.
    chat_container = st.container()

    with chat_container:
        # Exibir mensagens existentes (usuário e bot).
        for message in st.session_state.messages:
            if message["role"] == "user":
                display_chat_message({"content": message["content"]}, is_user=True)
            else:
                display_chat_message(
                    {
                        "content": message["content"],
                        "persona": message.get("persona", "Bot"),
                    }
                )

    # Formulário para envio de nova mensagem.
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])

        with col1:
            user_input = st.text_input(
                "Digite sua pergunta sobre roteiro de dispersão:",
                placeholder="Ex: Como calcular a dispersão de gases tóxicos?",
                label_visibility="collapsed",
            )

        with col2:
            submit_button = st.form_submit_button("Enviar", type="primary")

    # Processar nova mensagem: adiciona ao histórico e gera resposta via RAG.
    if submit_button and user_input.strip():
        st.session_state.messages.append(
            {"role": "user", "content": user_input, "timestamp": time.time()}
        )

        with st.spinner(f"{st.session_state.current_persona} está pensando..."):
            try:
                response = st.session_state.rag_system.generate_response(
                    query=user_input,
                    persona=st.session_state.current_persona,
                    session_id=st.session_state.session_id,
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                        "persona": st.session_state.current_persona,
                        "timestamp": time.time(),
                    }
                )

            except Exception as e:
                logger.error(f"Erro ao gerar resposta: {e}")
                st.error(
                    "Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente."
                )

        st.rerun()

    # Exibir exemplos de perguntas quando o chat está vazio.
    if len(st.session_state.messages) == 0:
        st.subheader("💡 Exemplos de Perguntas")

        example_questions = [
            "O que é roteiro de dispersão?",
            "Como os fatores meteorológicos afetam a dispersão?",
            "Quais são os principais modelos de dispersão atmosférica?",
            "Como calcular a concentração de poluentes?",
            "Qual a diferença entre dispersão e difusão?",
        ]

        cols = st.columns(2)
        for i, question in enumerate(example_questions):
            with cols[i % 2]:
                if st.button(question, key=f"example_{i}"):
                    # Simular envio da pergunta para facilitar onboarding do usuário.
                    st.session_state.messages.append(
                        {"role": "user", "content": question, "timestamp": time.time()}
                    )
                    st.rerun()


if __name__ == "__main__":
    main()
