"""
Funções utilitárias para processamento de texto, como chunking.
"""

from typing import List


def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 300) -> List[str]:
    """
    Divide um texto em chunks de tamanho definido, com sobreposição opcional.

    Parâmetros:
        text (str): Texto a ser dividido.
        chunk_size (int): Tamanho de cada chunk.
        overlap (int): Número de caracteres de sobreposição entre chunks.

    Retorna:
        List[str]: Lista de chunks de texto.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += chunk_size - overlap
    return chunks


def expand_query_with_synonyms(question: str) -> str:
    """
    Expande a pergunta com sinônimos e termos relacionados (exemplo simplificado).

    Parâmetros:
        question (str): Pergunta original.

    Retorna:
        str: Pergunta expandida com sinônimos.
    """
    # Exemplo simples: adicionar alguns sinônimos manualmente
    synonyms = {
        "dispensação": ["entrega", "fornecimento"],
        "medicamento": ["remédio", "fármaco"],
        "paciente": ["usuário", "cliente"],
    }
    expanded = question
    for word, syns in synonyms.items():
        if word in question:
            expanded += " " + " ".join(syns)
    return expanded


def find_best_chunk(question: str, chunks: list) -> str:
    """
    Encontra o chunk mais relevante para a pergunta, baseado em similaridade simples.

    Parâmetros:
        question (str): Pergunta do usuário.
        chunks (list): Lista de chunks de texto.

    Retorna:
        str: Chunk mais relevante.
    """
    # Exemplo simplificado: retorna o chunk que contém mais palavras da pergunta
    question_words = set(question.lower().split())
    best_chunk = ""
    best_score = 0
    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(question_words & chunk_words)
        if score > best_score:
            best_score = score
            best_chunk = chunk
    return best_chunk
