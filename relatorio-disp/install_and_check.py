#!/usr/bin/env python3
"""
Script de Instalação e Verificação de Compatibilidade
Chatbot Tese Hanseníase
"""

import os
import sys
import subprocess
import json
import time

def print_header():
    """Imprime cabeçalho do script"""
    print("="*60)
    print("🚀 INSTALADOR E VERIFICADOR DE COMPATIBILIDADE")
    print("   Chatbot Tese Hanseníase")
    print("="*60)

def print_step(step, message):
    """Imprime uma etapa do processo"""
    print(f"\n{step}. {message}")
    print("-" * 40)

def check_python_version():
    """Verifica versão do Python"""
    print_step(1, "Verificando versão do Python")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} não é suportado")
        print("   Requerido: Python 3.8+")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def check_pdf_file():
    """Verifica se o PDF existe"""
    print_step(2, "Verificando arquivo PDF")
    
    pdf_path = "Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF não encontrado: {pdf_path}")
        print("   Por favor, coloque o arquivo PDF na raiz do projeto")
        return False, None
    
    file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # MB
    print(f"✅ PDF encontrado: {pdf_path}")
    print(f"   Tamanho: {file_size:.2f} MB")
    
    return True, pdf_path

def install_dependencies():
    """Instala dependências"""
    print_step(3, "Instalando dependências")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def analyze_pdf_compatibility(pdf_path):
    """Analisa compatibilidade do PDF"""
    print_step(4, "Analisando compatibilidade do PDF")
    
    try:
        # Importar após instalação
        import pdfplumber
        
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            # Extrair amostra para análise
            sample_text = ""
            for i in range(min(5, total_pages)):  # Primeiras 5 páginas
                page_text = pdf.pages[i].extract_text()
                if page_text:
                    sample_text += page_text + "\n"
            
            # Estimar tamanho total
            avg_chars_per_page = len(sample_text) / min(5, total_pages)
            estimated_total_chars = avg_chars_per_page * total_pages
            
            # Classificar complexidade
            if estimated_total_chars < 50000:
                complexity = "LOW"
                recommendation = "PDF pequeno - processamento direto"
            elif estimated_total_chars < 100000:
                complexity = "MEDIUM"
                recommendation = "PDF médio - chunking recomendado"
            else:
                complexity = "HIGH"
                recommendation = "PDF grande - otimizações necessárias"
            
            print(f"📊 Análise do PDF:")
            print(f"   - Páginas: {total_pages}")
            print(f"   - Caracteres estimados: {estimated_total_chars:,.0f}")
            print(f"   - Complexidade: {complexity}")
            print(f"   - Recomendação: {recommendation}")
            
            return {
                "total_pages": total_pages,
                "estimated_chars": estimated_total_chars,
                "complexity": complexity,
                "recommendation": recommendation
            }
            
    except Exception as e:
        print(f"❌ Erro ao analisar PDF: {e}")
        return None

def generate_optimized_config(analysis):
    """Gera configuração otimizada"""
    print_step(5, "Gerando configuração otimizada")
    
    complexity = analysis["complexity"]
    
    if complexity == "LOW":
        config = {
            "chunk_size": 2000,
            "overlap": 200,
            "max_answer_length": 200,
            "confidence_threshold": 0.3,
            "use_semantic_search": False,
            "use_caching": False,
            "complexity_level": "LOW"
        }
    elif complexity == "MEDIUM":
        config = {
            "chunk_size": 2000,
            "overlap": 200,
            "max_answer_length": 200,
            "confidence_threshold": 0.35,
            "use_semantic_search": False,
            "use_caching": True,
            "complexity_level": "MEDIUM"
        }
    else:  # HIGH
        config = {
            "chunk_size": 1500,
            "overlap": 300,
            "max_answer_length": 150,
            "confidence_threshold": 0.4,
            "use_semantic_search": True,
            "use_caching": True,
            "complexity_level": "HIGH"
        }
    
    # Salvar configuração
    with open("optimized_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Configuração otimizada gerada:")
    for key, value in config.items():
        print(f"   - {key}: {value}")
    
    return config

def test_model_loading():
    """Testa carregamento do modelo"""
    print_step(6, "Testando carregamento do modelo")
    
    try:
        from transformers import pipeline
        
        print("🔄 Carregando modelo (pode demorar alguns minutos)...")
        start_time = time.time()
        
        qa_pipeline = pipeline(
            "question-answering",
            model="deepset/roberta-base-squad2",
            device=-1  # CPU
        )
        
        load_time = time.time() - start_time
        print(f"✅ Modelo carregado em {load_time:.1f} segundos")
        
        # Teste simples
        test_result = qa_pipeline(
            question="O que é hanseníase?",
            context="Hanseníase é uma doença infecciosa causada pela bactéria Mycobacterium leprae.",
            max_answer_len=50
        )
        
        if test_result and test_result['answer']:
            print("✅ Teste do modelo bem-sucedido")
            return True
        else:
            print("❌ Teste do modelo falhou")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        return False

def create_startup_script():
    """Cria script de inicialização"""
    print_step(7, "Criando script de inicialização")
    
    script_content = """#!/bin/bash
# Script de inicialização do Chatbot Tese Hanseníase

echo "🚀 Iniciando Chatbot Tese Hanseníase..."

# Verificar se o PDF existe
if [ ! -f "Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf" ]; then
    echo "❌ PDF não encontrado!"
    echo "   Coloque o arquivo PDF na raiz do projeto"
    exit 1
fi

# Verificar se as dependências estão instaladas
if ! python3 -c "import flask, pdfplumber, transformers" 2>/dev/null; then
    echo "❌ Dependências não instaladas!"
    echo "   Execute: pip install -r requirements.txt"
    exit 1
fi

# Iniciar aplicação
echo "✅ Iniciando servidor..."
python3 app_optimized.py
"""
    
    with open("start.sh", "w") as f:
        f.write(script_content)
    
    # Tornar executável (Linux/Mac)
    try:
        os.chmod("start.sh", 0o755)
    except:
        pass
    
    print("✅ Script de inicialização criado: start.sh")

def print_summary(analysis, config):
    """Imprime resumo da instalação"""
    print("\n" + "="*60)
    print("📋 RESUMO DA INSTALAÇÃO")
    print("="*60)
    
    print(f"✅ Python: {sys.version.split()[0]}")
    print(f"✅ PDF: {analysis['total_pages']} páginas ({analysis['estimated_chars']:,.0f} chars)")
    print(f"✅ Complexidade: {analysis['complexity']}")
    print(f"✅ Configuração: {config['complexity_level']}")
    
    print(f"\n🚀 Para iniciar:")
    print(f"   python3 app_optimized.py")
    print(f"   ou")
    print(f"   ./start.sh")
    
    print(f"\n🌐 Acesse: http://localhost:5000")
    
    print(f"\n📊 Performance esperada:")
    if analysis['complexity'] == "LOW":
        print(f"   - Tempo de resposta: < 2 segundos")
        print(f"   - Uso de memória: < 500MB")
    elif analysis['complexity'] == "MEDIUM":
        print(f"   - Tempo de resposta: 2-5 segundos")
        print(f"   - Uso de memória: 500MB-1GB")
    else:
        print(f"   - Tempo de resposta: 5-10 segundos")
        print(f"   - Uso de memória: 1GB-2GB")
    
    print("="*60)

def main():
    """Função principal"""
    print_header()
    
    # Verificações iniciais
    if not check_python_version():
        return False
    
    pdf_exists, pdf_path = check_pdf_file()
    if not pdf_exists:
        return False
    
    # Instalação
    if not install_dependencies():
        return False
    
    # Análise
    analysis = analyze_pdf_compatibility(pdf_path)
    if not analysis:
        return False
    
    # Configuração
    config = generate_optimized_config(analysis)
    
    # Teste do modelo
    if not test_model_loading():
        print("⚠️  Modelo não pôde ser carregado, mas a instalação continuará")
    
    # Script de inicialização
    create_startup_script()
    
    # Resumo
    print_summary(analysis, config)
    
    print("\n🎉 Instalação concluída com sucesso!")
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Instalação falhou. Verifique os erros acima.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalação interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1) 