#!/usr/bin/env python3
"""
Script Consolidado de Testes, Debug e Análise
============================================

Este script reúne as melhores funções dos utilitários de debug, teste e análise do projeto Chatbot Hanseníase.

Funcionalidades:
- Verificação do ambiente Python e dependências
- Análise de compatibilidade do PDF
- Teste rápido do endpoint do chatbot
- Demonstração de chunking e busca semântica
- Geração de relatório resumido

Uso:
    python teste_consolidado.py [opção]

Opções disponíveis:
    ambiente      - Verifica ambiente Python e dependências
    pdf           - Analisa compatibilidade do PDF
    endpoint      - Testa o endpoint do chatbot
    chunking      - Demonstra chunking e busca semântica
    tudo          - Executa todos os testes acima

"""
import os
import sys
import subprocess
import json
import time
import re
from typing import List

# =====================
# Utilitários Gerais
# =====================
def print_header(title):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

def print_step(step, message):
    print(f"\n{step}. {message}")
    print("-" * 40)

# =====================
# 1. Verificação de Ambiente
# =====================
def check_python_environment():
    print_step(1, "Verificando Ambiente Python")
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ requerido")
        return False
    print("✅ Versão do Python OK")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Pip: {result.stdout.strip()}")
        else:
            print("❌ Pip não disponível")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar pip: {e}")
        return False
    return True

def check_dependencies():
    print_step(2, "Verificando Dependências")
    required_packages = [
        'flask', 'flask-cors', 'pdfplumber', 'transformers', 'torch', 'numpy', 'requests'
    ]
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NÃO INSTALADO")
            missing_packages.append(package)
    if missing_packages:
        print(f"⚠️  Pacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip install -r requirements.txt")
        return False
    print("✅ Todas as dependências estão instaladas")
    return True

# =====================
# 2. Análise de PDF
# =====================
def analyze_pdf(pdf_path="Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf"):
    print_step(3, "Analisando compatibilidade do PDF")
    try:
        import pdfplumber
        if not os.path.exists(pdf_path):
            print(f"❌ PDF não encontrado: {pdf_path}")
            return False
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            sample_text = ""
            for i in range(min(5, total_pages)):
                page_text = pdf.pages[i].extract_text()
                if page_text:
                    sample_text += page_text + "\n"
            avg_chars_per_page = len(sample_text) / min(5, total_pages)
            estimated_total_chars = avg_chars_per_page * total_pages
            if estimated_total_chars < 50000:
                complexity = "LOW"
                recommendation = "PDF pequeno - processamento direto"
            elif estimated_total_chars < 100000:
                complexity = "MEDIUM"
                recommendation = "PDF médio - chunking recomendado"
            else:
                complexity = "HIGH"
                recommendation = "PDF grande - otimizações necessárias"
            print(f"📊 Páginas: {total_pages}")
            print(f"📊 Caracteres estimados: {estimated_total_chars:,.0f}")
            print(f"📊 Complexidade: {complexity}")
            print(f"💡 Recomendação: {recommendation}")
            return True
    except Exception as e:
        print(f"❌ Erro ao analisar PDF: {e}")
        return False

# =====================
# 3. Teste de Endpoint
# =====================
def test_endpoint():
    print_step(4, "Testando endpoint do chatbot")
    try:
        import requests
        print("📝 Testando: 'O que é hanseníase?'")
        response = requests.post(
            'http://localhost:5000/api/chat',
            json={'question': 'O que é hanseníase?', 'personality_id': 'dr_gasnelio'},
            timeout=20
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"💬 Resposta: {data.get('answer', 'N/A')[:150]}...")
            print(f"📊 Confiança: {data.get('confidence', 0):.3f}")
            print(f"📚 Fonte: {data.get('source', 'N/A')}")
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")

# =====================
# 4. Chunking e Busca Semântica
# =====================
def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
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

def demo_chunking(pdf_path="Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf", chunk_size=800, overlap=400):
    print_step(5, "Demonstração de chunking e busca semântica")
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        print(f"Texto extraído: {len(text)} caracteres")
        chunks = chunk_text(text, chunk_size, overlap)
        print(f"Chunks criados: {len(chunks)}")
        question = "O que é a poliquimioterapia única (PQT-U) para hanseníase?"
        best_chunk = find_best_chunk(question, chunks)
        print(f"Melhor chunk encontrado:\n{best_chunk[:500]}...")
    except Exception as e:
        print(f"❌ Erro na demonstração de chunking: {e}")

def find_best_chunk(question: str, chunks: List[str]) -> str:
    question_lower = question.lower()
    best_chunk = chunks[0] if chunks else ""
    best_score = 0
    keywords = ['poliquimioterapia', 'pqt', 'pqt-u', 'hanseniase', 'lepra']
    for i, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        score = 0
        for word in keywords:
            if word in question_lower and word in chunk_lower:
                score += 5.0
        question_words = set(re.findall(r'\w+', question_lower))
        chunk_words = set(re.findall(r'\w+', chunk_lower))
        common_words = question_words.intersection(chunk_words)
        if question_words:
            score += len(common_words) / len(question_words)
        if score > best_score:
            best_score = score
            best_chunk = chunk
    return best_chunk

# =====================
# Execução Principal
# =====================
def main():
    print_header("SCRIPT CONSOLIDADO DE TESTES E DEBUG")
    args = sys.argv[1:]
    if not args:
        print("\nUso: python teste_consolidado.py [opção]")
        print("Opções: ambiente | pdf | endpoint | chunking | tudo")
        return
    if "ambiente" in args or "tudo" in args:
        check_python_environment()
        check_dependencies()
    if "pdf" in args or "tudo" in args:
        analyze_pdf()
    if "endpoint" in args or "tudo" in args:
        test_endpoint()
    if "chunking" in args or "tudo" in args:
        demo_chunking()
    print("\n✅ Testes concluídos!")

if __name__ == "__main__":
    main() 