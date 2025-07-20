"""
Script para processar a tese de doutorado e construir a base de conhecimento RAG
"""

import os
import sys
import logging
from pathlib import Path
from typing import List
import PyPDF2
import re

# Adiciona o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from rag_service import RAGService

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Processador de documentos para criar chunks da base de conhecimento"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process_pdf(self, pdf_path: str) -> List[str]:
        """Processa um arquivo PDF e retorna lista de chunks"""
        try:
            logger.info(f"Processando PDF: {pdf_path}")
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        text += page_text + "\n"
                        logger.info(f"Processada página {page_num + 1}")
                    except Exception as e:
                        logger.warning(f"Erro ao processar página {page_num + 1}: {str(e)}")
                        continue
            
            # Limpa e processa o texto
            cleaned_text = self._clean_text(text)
            
            # Divide em chunks
            chunks = self._create_chunks(cleaned_text)
            
            logger.info(f"PDF processado: {len(chunks)} chunks criados")
            return chunks
            
        except Exception as e:
            logger.error(f"Erro ao processar PDF: {str(e)}")
            return []
    
    def process_markdown(self, md_path: str) -> List[str]:
        """Processa um arquivo Markdown e retorna lista de chunks"""
        try:
            logger.info(f"Processando Markdown: {md_path}")
            
            with open(md_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            # Limpa e processa o texto
            cleaned_text = self._clean_text(text)
            
            # Divide em chunks
            chunks = self._create_chunks(cleaned_text)
            
            logger.info(f"Markdown processado: {len(chunks)} chunks criados")
            return chunks
            
        except Exception as e:
            logger.error(f"Erro ao processar Markdown: {str(e)}")
            return []
    
    def _clean_text(self, text: str) -> str:
        """Limpa e normaliza o texto"""
        # Remove quebras de linha excessivas
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Remove espaços excessivos
        text = re.sub(r' +', ' ', text)
        
        # Remove caracteres especiais problemáticos
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}\"\'\/\\\n]', '', text)
        
        return text.strip()
    
    def _create_chunks(self, text: str) -> List[str]:
        """Divide o texto em chunks com sobreposição"""
        chunks = []
        
        # Divide por parágrafos primeiro
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        
        for paragraph in paragraphs:
            # Se adicionar este parágrafo não exceder o tamanho máximo
            if len(current_chunk) + len(paragraph) <= self.chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                # Salva chunk atual se não estiver vazio
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                # Inicia novo chunk
                if len(paragraph) <= self.chunk_size:
                    current_chunk = paragraph + "\n\n"
                else:
                    # Parágrafo muito grande, divide por sentenças
                    sentences = paragraph.split('. ')
                    temp_chunk = ""
                    
                    for sentence in sentences:
                        if len(temp_chunk) + len(sentence) <= self.chunk_size:
                            temp_chunk += sentence + ". "
                        else:
                            if temp_chunk.strip():
                                chunks.append(temp_chunk.strip())
                            temp_chunk = sentence + ". "
                    
                    current_chunk = temp_chunk
        
        # Adiciona último chunk se não estiver vazio
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # Remove chunks muito pequenos
        chunks = [chunk for chunk in chunks if len(chunk) > 100]
        
        return chunks

def main():
    """Função principal"""
    logger.info("Iniciando construção da base de conhecimento...")
    
    # Diretórios
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'
    
    # Cria diretório de dados se não existir
    data_dir.mkdir(exist_ok=True)
    
    # Processa documentos
    processor = DocumentProcessor()
    all_chunks = []
    
    # Procura por arquivos PDF na pasta data
    pdf_files = list(data_dir.glob('*.pdf'))
    if pdf_files:
        logger.info(f"Encontrados {len(pdf_files)} arquivos PDF")
        for pdf_file in pdf_files:
            chunks = processor.process_pdf(str(pdf_file))
            all_chunks.extend(chunks)
    
    # Procura por arquivos Markdown na pasta data
    md_files = list(data_dir.glob('*.md'))
    if md_files:
        logger.info(f"Encontrados {len(md_files)} arquivos Markdown")
        for md_file in md_files:
            if md_file.name != 'README.md':  # Ignora README
                chunks = processor.process_markdown(str(md_file))
                all_chunks.extend(chunks)
    
    if not all_chunks:
        logger.error("Nenhum documento encontrado para processar!")
        logger.info("Coloque arquivos PDF ou Markdown na pasta 'data/'")
        return False
    
    logger.info(f"Total de chunks criados: {len(all_chunks)}")
    
    # Constrói índice RAG no Astra DB
    logger.info("Construindo índice no Astra DB...")
    rag_service = RAGService()
    
    if rag_service.build_index(all_chunks):
        logger.info("✅ Base de conhecimento construída com sucesso no Astra DB!")
        
        # Mostra estatísticas
        stats = rag_service.get_stats()
        logger.info(f"Estatísticas: {stats}")
        
        return True
    else:
        logger.error("❌ Erro ao construir base de conhecimento no Astra DB")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

