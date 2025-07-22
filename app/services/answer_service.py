"""
Módulo centralizado para responder perguntas do chatbot farmacêutico.
Contém a função principal answer_question, que pode ser importada por diferentes apps.
"""

from typing import Dict


# Exemplo de função centralizada (ajuste conforme a lógica principal do seu projeto)
def answer_question(
    question: str, persona: str = "professor", session_id: str = None
) -> Dict:
    """
    Gera uma resposta para a pergunta do usuário, considerando a persona e session_id.

    Parâmetros:
        question (str): Pergunta do usuário.
        persona (str): Persona selecionada (ex: 'professor', 'amigavel').
        session_id (str, opcional): ID da sessão do usuário.

    Retorna:
        Dict: Resposta formatada.
    """
    # Aqui você pode integrar com o pipeline RAG, banco de dados, etc.
    # Exemplo: delegar para o pipeline real se disponível
    try:
        from app.rag_system import get_rag_system

        rag_system = get_rag_system()
        resposta = rag_system.generate_response(question, persona, session_id)
        return {"answer": resposta, "persona": persona}
    except Exception as e:
        # Fallback simples
        if persona == "amigavel":
            resposta = f"Olá! 😊 Sobre sua dúvida: {question} ... (resposta amigável)"
        else:
            resposta = f"Resposta técnica para: {question} ... (resposta professor)"
        return {"answer": resposta, "persona": persona, "error": str(e)}
