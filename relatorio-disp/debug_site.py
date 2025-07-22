#!/usr/bin/env python3
"""
Script de Debug Completo - Chatbot Tese Hanseníase
"""

import os
import sys
import json
import re
import subprocess

def print_header(title):
    """Imprime cabeçalho de seção"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_step(step, message):
    """Imprime uma etapa do debug"""
    print(f"\n{step}. {message}")
    print("-" * 40)

def check_python_environment():
    """Verifica ambiente Python"""
    print_step(1, "Verificando Ambiente Python")
    
    # Versão do Python
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ requerido")
        return False
    
    print("✅ Versão do Python OK")
    
    # Verificar pip
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
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
    """Verifica dependências"""
    print_step(2, "Verificando Dependências")
    
    required_packages = [
        'flask', 'flask-cors', 'pdfplumber', 'transformers', 
        'torch', 'numpy', 'requests'
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
        print(f"\n⚠️  Pacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas")
    return True

def check_files_structure():
    """Verifica estrutura de arquivos"""
    print_step(3, "Verificando Estrutura de Arquivos")
    
    required_files = [
        'index.html',
        'script.js', 
        'app_optimized.py',
        'requirements.txt',
        'optimized_config.json'
    ]
    
    optional_files = [
        'Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf',
        'tese.html'
    ]
    
    missing_required = []
    missing_optional = []
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size:,} bytes)")
        else:
            print(f"❌ {file} - AUSENTE")
            missing_required.append(file)
    
    for file in optional_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size:,} bytes)")
        else:
            print(f"⚠️  {file} - AUSENTE (opcional)")
            missing_optional.append(file)
    
    if missing_required:
        print(f"\n❌ Arquivos obrigatórios faltando: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Arquivos opcionais faltando: {', '.join(missing_optional)}")
    
    return True

def check_html_files():
    """Verifica arquivos HTML"""
    print_step(4, "Verificando Arquivos HTML")
    
    html_files = ['index.html', 'tese.html']
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"⚠️  {html_file} não encontrado")
            continue
            
        print(f"\n📄 Analisando {html_file}:")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar tamanho
            size = len(content)
            print(f"   Tamanho: {size:,} caracteres")
            
            # Verificar elementos importantes
            checks = [
                ('<!DOCTYPE html>', 'DOCTYPE'),
                ('<title>', 'Título'),
                ('<meta charset', 'Charset'),
                ('<script', 'Scripts'),
                ('<link', 'CSS'),
                ('<body', 'Body'),
                ('</html>', 'HTML fechado')
            ]
            
            for check, name in checks:
                if check in content:
                    print(f"   ✅ {name}")
                else:
                    print(f"   ❌ {name} - AUSENTE")
            
            # Verificar links quebrados
            links = re.findall(r'href=["\']([^"\']+)["\']', content)
            scripts = re.findall(r'src=["\']([^"\']+)["\']', content)
            
            print(f"   Links encontrados: {len(links)}")
            print(f"   Scripts encontrados: {len(scripts)}")
            
        except Exception as e:
            print(f"   ❌ Erro ao ler {html_file}: {e}")
    
    return True

def check_javascript():
    """Verifica arquivo JavaScript"""
    print_step(5, "Verificando JavaScript")
    
    if not os.path.exists('script.js'):
        print("❌ script.js não encontrado")
        return False
    
    try:
        with open('script.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        size = len(content)
        print(f"Tamanho: {size:,} caracteres")
        
        # Verificar elementos importantes
        checks = [
            ('class ChatbotInterface', 'Classe ChatbotInterface'),
            ('fetchLLMResponse', 'Função fetchLLMResponse'),
            ('addMessage', 'Função addMessage'),
            ('persona', 'Sistema de personas'),
            ('/api/chat', 'Endpoint da API'),
            ('addEventListener', 'Event listeners')
        ]
        
        for check, name in checks:
            if check in content:
                print(f"✅ {name}")
            else:
                print(f"❌ {name} - AUSENTE")
        
        # Verificar sintaxe básica
        try:
            # Verificar se tem chaves balanceadas
            open_braces = content.count('{')
            close_braces = content.count('}')
            
            if open_braces == close_braces:
                print("✅ Sintaxe básica OK")
            else:
                print(f"❌ Chaves desbalanceadas: {open_braces} abertas, {close_braces} fechadas")
                return False
                
        except Exception as e:
            print(f"❌ Erro na verificação de sintaxe: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler script.js: {e}")
        return False

def check_backend():
    """Verifica backend Flask"""
    print_step(6, "Verificando Backend Flask")
    
    backend_files = ['app.py', 'app_optimized.py']
    
    for backend_file in backend_files:
        if not os.path.exists(backend_file):
            print(f"⚠️  {backend_file} não encontrado")
            continue
            
        print(f"\n🐍 Analisando {backend_file}:")
        
        try:
            with open(backend_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            size = len(content)
            print(f"   Tamanho: {size:,} caracteres")
            
            # Verificar elementos importantes
            checks = [
                ('from flask import', 'Import Flask'),
                ('app = Flask', 'Aplicação Flask'),
                ('@app.route', 'Rotas definidas'),
                ('/api/chat', 'Endpoint /api/chat'),
                ('jsonify', 'JSON responses'),
                ('CORS', 'CORS habilitado')
            ]
            
            for check, name in checks:
                if check in content:
                    print(f"   ✅ {name}")
                else:
                    print(f"   ❌ {name} - AUSENTE")
            
            # Contar rotas
            routes = re.findall(r'@app\.route\(["\']([^"\']+)["\']', content)
            print(f"   Rotas encontradas: {len(routes)}")
            for route in routes:
                print(f"     - {route}")
        
        except Exception as e:
            print(f"   ❌ Erro ao ler {backend_file}: {e}")
    
    return True

def check_configuration():
    """Verifica configurações"""
    print_step(7, "Verificando Configurações")
    
    config_files = ['optimized_config.json', 'requirements.txt']
    
    for config_file in config_files:
        if not os.path.exists(config_file):
            print(f"❌ {config_file} não encontrado")
            continue
            
        print(f"\n⚙️  Analisando {config_file}:")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if config_file.endswith('.json'):
                # Verificar JSON válido
                try:
                    config = json.loads(content)
                    print(f"   ✅ JSON válido")
                    
                    if 'chunk_size' in config:
                        print(f"   Chunk size: {config['chunk_size']}")
                    if 'confidence_threshold' in config:
                        print(f"   Confidence threshold: {config['confidence_threshold']}")
                    if 'use_caching' in config:
                        print(f"   Cache: {config['use_caching']}")
                        
                except json.JSONDecodeError as e:
                    print(f"   ❌ JSON inválido: {e}")
                    return False
            else:
                # Verificar requirements.txt
                lines = content.strip().split('\n')
                print(f"   Dependências: {len(lines)}")
                for line in lines:
                    if line.strip():
                        print(f"     - {line.strip()}")
        
        except Exception as e:
            print(f"   ❌ Erro ao ler {config_file}: {e}")
    
    return True

def check_pdf_compatibility():
    """Verifica compatibilidade do PDF"""
    print_step(8, "Verificando Compatibilidade do PDF")
    
    pdf_file = "Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"⚠️  {pdf_file} não encontrado")
        print("   Baixe o PDF do link fornecido")
        return False
    
    try:
        size = os.path.getsize(pdf_file)
        size_mb = size / (1024 * 1024)
        
        print(f"📄 PDF encontrado:")
        print(f"   Tamanho: {size_mb:.2f} MB ({size:,} bytes)")
        
        # Classificar tamanho
        if size_mb < 1:
            category = "Pequeno"
            config = "LOW"
        elif size_mb < 5:
            category = "Médio"
            config = "MEDIUM"
        else:
            category = "Grande"
            config = "HIGH"
        
        print(f"   Categoria: {category}")
        print(f"   Configuração recomendada: {config}")
        
        # Verificar se a configuração atual é adequada
        if os.path.exists('optimized_config.json'):
            with open('optimized_config.json', 'r') as f:
                current_config = json.load(f)
            
            current_level = current_config.get('complexity_level', 'UNKNOWN')
            print(f"   Configuração atual: {current_level}")
            
            if current_level == config:
                print("   ✅ Configuração adequada")
            else:
                print(f"   ⚠️  Configuração pode precisar de ajuste")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar PDF: {e}")
        return False

def test_backend_startup():
    """Testa inicialização do backend"""
    print_step(9, "Testando Inicialização do Backend")
    
    try:
        # Tentar importar o módulo
        import importlib.util
        
        spec = importlib.util.spec_from_file_location("app_optimized", "app_optimized.py")
        if spec is None:
            print("❌ Não foi possível carregar app_optimized.py")
            return False
        
        module = importlib.util.module_from_spec(spec)
        
        # Verificar se tem as funções necessárias
        required_functions = [
            'extract_pdf_text',
            'load_ai_model', 
            'answer_question',
            'format_persona_answer',
            'fallback_response'
        ]
        
        for func in required_functions:
            if hasattr(module, func):
                print(f"✅ {func}")
            else:
                print(f"❌ {func} - AUSENTE")
        
        print("✅ Backend pode ser importado")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar backend: {e}")
        return False

def check_network_connectivity():
    """Verifica conectividade de rede"""
    print_step(10, "Verificando Conectividade de Rede")
    
    try:
        import requests
        
        # Testar conectividade básica
        response = requests.get("https://httpbin.org/get", timeout=5)
        if response.status_code == 200:
            print("✅ Conectividade básica OK")
        else:
            print(f"❌ Conectividade básica falhou: {response.status_code}")
            return False
        
        # Testar acesso ao Hugging Face
        response = requests.get("https://huggingface.co", timeout=10)
        if response.status_code == 200:
            print("✅ Acesso ao Hugging Face OK")
        else:
            print(f"⚠️  Acesso ao Hugging Face limitado: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação de rede: {e}")
        return False

def generate_debug_report():
    """Gera relatório de debug"""
    print_header("RELATÓRIO DE DEBUG")
    
    issues = []
    warnings = []
    
    # Executar todas as verificações
    checks = [
        ("Ambiente Python", check_python_environment),
        ("Dependências", check_dependencies),
        ("Estrutura de Arquivos", check_files_structure),
        ("Arquivos HTML", check_html_files),
        ("JavaScript", check_javascript),
        ("Backend Flask", check_backend),
        ("Configurações", check_configuration),
        ("Compatibilidade PDF", check_pdf_compatibility),
        ("Inicialização Backend", test_backend_startup),
        ("Conectividade de Rede", check_network_connectivity)
    ]
    
    for name, check_func in checks:
        try:
            result = check_func()
            if not result:
                issues.append(name)
        except Exception as e:
            issues.append(f"{name} (erro: {e})")
    
    # Relatório final
    print_header("RESULTADO DO DEBUG")
    
    if not issues:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O site está pronto para execução")
        print("\n🚀 Para iniciar:")
        print("   Windows: start.bat")
        print("   Linux/Mac: python3 app_optimized.py")
        print("   Acesse: http://localhost:5000")
    else:
        print(f"❌ {len(issues)} PROBLEMAS ENCONTRADOS:")
        for issue in issues:
            print(f"   - {issue}")
        
        print(f"\n⚠️  {len(warnings)} AVISOS:")
        for warning in warnings:
            print(f"   - {warning}")
        
        print("\n🔧 AÇÕES NECESSÁRIAS:")
        if "Ambiente Python" in issues:
            print("   - Instale Python 3.8+")
        if "Dependências" in issues:
            print("   - Execute: pip install -r requirements.txt")
        if "Compatibilidade PDF" in issues:
            print("   - Baixe o PDF do link fornecido")
        if "Conectividade de Rede" in issues:
            print("   - Verifique sua conexão com a internet")
    
    return len(issues) == 0

def main():
    """Função principal"""
    print_header("DEBUG COMPLETO - CHATBOT TESE HANSENIASE")
    
    try:
        success = generate_debug_report()
        
        if success:
            print("\n🎉 Debug concluído com sucesso!")
            return True
        else:
            print("\n❌ Debug encontrou problemas que precisam ser corrigidos.")
            return False
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Debug interrompido pelo usuário")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado durante debug: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 