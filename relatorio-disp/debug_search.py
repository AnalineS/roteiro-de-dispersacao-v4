import json
import re
from typing import List

def load_config():
    """Carrega configurações do arquivo JSON"""
    try:
        with open('optimized_config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar configuração: {e}")
        return {}

def extract_pdf_text(pdf_path: str) -> str:
    """Extrai texto do PDF"""
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return ""

def create_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Cria chunks do texto"""
    if not text:
        return []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        
        if start >= len(text):
            break
    
    return chunks

def find_best_chunk(question: str, chunks: List[str]) -> str:
    """Encontra o chunk mais relevante para a pergunta com busca semântica melhorada"""
    if not chunks:
        return ""
    
    # Se temos poucos chunks, retorna o primeiro
    if len(chunks) <= 2:
        return chunks[0]
    
    # Palavras-chave específicas para hanseníase e PQT-U
    keywords = {
        'poliquimioterapia': ['poliquimioterapia', 'pqt', 'pqt-u', 'pqt u', 'quimioterapia', 'poliquimioterapia única'],
        'hanseniase': ['hanseniase', 'lepra', 'mycobacterium leprae', 'hanseníase'],
        'medicamentos': ['rifampicina', 'dapsona', 'clofazimina', 'talidomida', 'minociclina', 'ofloxacino'],
        'tratamento': ['tratamento', 'terapia', 'esquema', 'protocolo', 'dose', 'posologia'],
        'dispensacao': ['dispensacao', 'dispensação', 'medicamento', 'remedio', 'cartela'],
        'apresentacoes': ['apresentações', 'disponíveis', 'comprimido', 'mg', 'dose mensal']
    }
    
    # Normalizar pergunta
    question_lower = question.lower()
    
    # Busca por palavras-chave específicas primeiro
    best_chunk = chunks[0]
    best_score = 0
    
    print(f"🔍 Procurando por: '{question}'")
    print(f"📊 Analisando {len(chunks)} chunks...")
    
    for i, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        score = 0
        
        # Verificar palavras-chave específicas com peso maior
        for category, words in keywords.items():
            for word in words:
                if word in question_lower and word in chunk_lower:
                    score += 5.0  # Peso muito maior para palavras-chave específicas
                    print(f"  ✅ Chunk {i}: encontrou '{word}' (score +5.0)")
        
        # Bônus especial para PQT-U
        if 'pqt' in question_lower and ('pqt' in chunk_lower or 'poliquimioterapia' in chunk_lower):
            score += 10.0  # Bônus máximo para PQT-U
            print(f"  🎯 Chunk {i}: BÔNUS PQT-U (score +10.0)")
        
        # Busca por palavras comuns
        question_words = set(re.findall(r'\w+', question_lower))
        chunk_words = set(re.findall(r'\w+', chunk_lower))
        common_words = question_words.intersection(chunk_words)
        
        if question_words:
            score += len(common_words) / len(question_words)
        
        # Bônus para chunks que contêm termos médicos
        medical_terms = ['hanseníase', 'poliquimioterapia', 'rifampicina', 'dapsona', 'clofazimina', 'pqt-u']
        for term in medical_terms:
            if term in chunk_lower:
                score += 1.0
        
        # Bônus para chunks que contêm informações sobre doses
        if any(term in chunk_lower for term in ['mg', 'dose', 'comprimido', 'cartela']):
            score += 0.5
        
        if score > best_score:
            best_score = score
            best_chunk = chunk
            print(f"  🏆 Chunk {i} é o melhor até agora (score: {score:.2f})")
    
    print(f"🎯 Melhor chunk encontrado com score: {best_score:.2f}")
    
    # Se não encontrou nada relevante, procurar por chunks que contenham PQT-U
    if best_score == 0:
        print("⚠️ Nenhum chunk relevante encontrado, procurando por PQT-U...")
        for i, chunk in enumerate(chunks):
            if 'poliquimioterapia' in chunk.lower() or 'pqt' in chunk.lower():
                print(f"  📍 Encontrou PQT-U no chunk {i}")
                return chunk
    
    return best_chunk

def main():
    """Função principal para debug"""
    print("🔧 DEBUG: Testando busca por PQT-U")
    
    # Carregar configurações
    config = load_config()
    print(f"📋 Configurações: {config}")
    
    # Caminho do PDF
    pdf_path = "PDFs/Roteiro de Dsispensação - Hanseníase F.docx.pdf"
    
    # Extrair texto
    print(f"📄 Extraindo texto de: {pdf_path}")
    text = extract_pdf_text(pdf_path)
    
    if not text:
        print("❌ Não foi possível extrair texto do PDF")
        return
    
    print(f"📊 Texto extraído: {len(text)} caracteres")
    
    # Criar chunks
    chunk_size = config.get('chunk_size', 800)
    overlap = config.get('overlap', 400)
    
    print(f"✂️ Criando chunks (tamanho: {chunk_size}, overlap: {overlap})")
    chunks = create_chunks(text, chunk_size, overlap)
    print(f"📦 Criados {len(chunks)} chunks")
    
    # Testar busca
    question = "O que é a poliquimioterapia única (PQT-U) para hanseníase?"
    
    print("\n" + "="*60)
    print("🔍 TESTANDO BUSCA")
    print("="*60)
    
    best_chunk = find_best_chunk(question, chunks)
    
    print("\n" + "="*60)
    print("📄 MELHOR CHUNK ENCONTRADO")
    print("="*60)
    print(best_chunk[:500] + "..." if len(best_chunk) > 500 else best_chunk)
    
    # Verificar se contém informações sobre PQT-U
    chunk_lower = best_chunk.lower()
    pqt_terms = ['poliquimioterapia', 'pqt', 'pqt-u', 'pqt u']
    
    found_terms = [term for term in pqt_terms if term in chunk_lower]
    
    print(f"\n✅ Termos PQT-U encontrados: {found_terms}")
    
    if found_terms:
        print("🎉 SUCCESS: Chunk contém informações sobre PQT-U!")
    else:
        print("❌ FAIL: Chunk não contém informações sobre PQT-U")

if __name__ == "__main__":
    main() 