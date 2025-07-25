#!/usr/bin/env python3
"""
Script para carregar o conteúdo da tese na base de dados Astra DB
"""

import os
import sys
import logging
from pathlib import Path

# Adiciona o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from rag_service_openai import RAGService
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def split_text_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> list:
    """Divide o texto em chunks para processamento"""
    chunks = []
    start = 0
    
    while start < len(text):
        # Define o fim do chunk
        end = start + chunk_size
        
        # Se não chegamos ao fim do texto, procura quebra de parágrafo
        if end < len(text):
            # Procura por quebra de parágrafo mais próxima
            paragraph_break = text.rfind('\n\n', start, end)
            if paragraph_break != -1:
                end = paragraph_break
            else:
                # Se não encontrou parágrafo, procura por quebra de linha
                line_break = text.rfind('\n', start, end)
                if line_break != -1:
                    end = line_break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move o início considerando o overlap
        start = end - overlap if end < len(text) else end
    
    return chunks

def load_knowledge_base():
    """Carrega o conteúdo da tese na base de dados"""
    try:
        # Localiza o arquivo da tese
        thesis_path = Path("/app/PDFs/Roteiro de Dsispensação - Hanseníase.md")
        
        if not thesis_path.exists():
            logger.error(f"Arquivo da tese não encontrado: {thesis_path}")
            return False
        
        # Lê o conteúdo do arquivo
        logger.info("Carregando conteúdo da tese...")
        with open(thesis_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        logger.info(f"Conteúdo carregado: {len(content)} caracteres")
        
        # Divide em chunks
        logger.info("Dividindo conteúdo em chunks...")
        chunks = split_text_into_chunks(content, chunk_size=800, overlap=100)
        logger.info(f"Criados {len(chunks)} chunks")
        
        # Inicializa o serviço RAG
        logger.info("Inicializando serviço RAG...")
        rag_service = RAGService()
        
        if not rag_service.is_ready():
            logger.error("Serviço RAG não está pronto")
            return False
        
        # Prepara documentos para inserção
        documents = []
        for i, chunk in enumerate(chunks):
            documents.append({
                'id': f'thesis_chunk_{i}',
                'content': chunk,
                'metadata': {
                    'source': 'roteiro_hanseniase_thesis',
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                }
            })
        
        # Adiciona documentos à base de dados
        logger.info("Adicionando documentos à base de dados...")
        success = rag_service.add_documents(documents)
        
        if success:
            logger.info("✅ Base de conhecimento carregada com sucesso!")
            return True
        else:
            logger.error("❌ Falha ao carregar base de conhecimento")
            return False
            
    except Exception as e:
        logger.error(f"Erro ao carregar base de conhecimento: {str(e)}")
        return False

def test_rag_service():
    """Testa o serviço RAG com uma pergunta"""
    try:
        logger.info("Testando serviço RAG...")
        rag_service = RAGService()
        
        if not rag_service.is_ready():
            logger.error("Serviço RAG não está pronto para teste")
            return False
        
        # Faz uma pergunta de teste
        test_query = "O que é hanseníase?"
        context = rag_service.retrieve_context(test_query, top_k=2)
        
        logger.info(f"Pergunta teste: {test_query}")
        logger.info(f"Contexto recuperado: {context[:200]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro no teste RAG: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("=== Iniciando carregamento da base de conhecimento ===")
    
    # Carrega a base de conhecimento
    if load_knowledge_base():
        logger.info("=== Base de conhecimento carregada ===")
        
        # Testa o serviço
        if test_rag_service():
            logger.info("=== Teste RAG concluído com sucesso ===")
        else:
            logger.error("=== Falha no teste RAG ===")
    else:
        logger.error("=== Falha no carregamento da base de conhecimento ===")