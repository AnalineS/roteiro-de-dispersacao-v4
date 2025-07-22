#!/usr/bin/env python3
"""
Teste de Integração com Langflow
Verifica se a integração está funcionando corretamente
"""

import sys
import os
import requests
from datetime import datetime

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def print_step(step, description):
    """Imprime passo do teste"""
    print(f"\n[{step}] {description}")
    print("-" * 40)

def test_langflow_installation():
    """Testa se o Langflow está instalado"""
    print_step("1", "Verificando instalação do Langflow")
    
    try:
        print("✅ Langflow instalado")
        return True
    except ImportError:
        print("❌ Langflow não instalado")
        print("💡 Execute: pip install langflow")
        return False

def test_langflow_server():
    """Testa se o servidor Langflow está rodando"""
    print_step("2", "Verificando servidor Langflow")
    
    try:
        response = requests.get("http://localhost:7860/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor Langflow rodando")
            return True
        else:
            print(f"❌ Servidor Langflow retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print("❌ Servidor Langflow não acessível")
        print(f"💡 Erro: {e}")
        print("💡 Execute: langflow run")
        return False

def test_integration_module():
    """Testa se o módulo de integração está funcionando"""
    print_step("3", "Testando módulo de integração")
    
    try:
        from langflow_integration import HanseniaseLangflowBridge
        print("✅ Módulo de integração importado")
        
        # Criar bridge
        bridge = HanseniaseLangflowBridge()
        print(f"✅ Bridge criada (Langflow ativo: {bridge.use_langflow})")
        
        return True
    except ImportError as e:
        print("❌ Erro ao importar módulo de integração")
        print(f"💡 Erro: {e}")
        return False
    except Exception as e:
        print("❌ Erro ao criar bridge")
        print(f"💡 Erro: {e}")
        return False

def test_app_integration():
    """Testa se o app com Langflow está funcionando"""
    print_step("4", "Testando app com integração")
    
    try:
        # Importar app
        from app_with_langflow import chatbot
        
        print("✅ App com Langflow importado")
        print(f"✅ Chatbot criado (Langflow ativo: {chatbot.use_langflow})")
        
        # Testar resposta
        test_question = "O que é hanseníase?"
        result = chatbot.answer_question(test_question, "dr_gasnelio")
        
        if result.get("success"):
            print("✅ Resposta gerada com sucesso")
            print(f"   Fonte: {result.get('source', 'unknown')}")
            print(f"   Confiança: {result.get('confidence', 0):.2f}")
        else:
            print("❌ Erro ao gerar resposta")
            print(f"   Erro: {result.get('error', 'unknown')}")
        
        return True
    except ImportError as e:
        print("❌ Erro ao importar app com Langflow")
        print(f"💡 Erro: {e}")
        return False
    except Exception as e:
        print("❌ Erro ao testar app")
        print(f"💡 Erro: {e}")
        return False

def test_api_endpoints():
    """Testa os endpoints da API"""
    print_step("5", "Testando endpoints da API")
    
    try:
        # Iniciar app em thread separada
        import threading
        import time
        from app_with_langflow import app
        
        def run_app():
            app.run(debug=False, host='localhost', port=5001)
        
        # Iniciar app
        app_thread = threading.Thread(target=run_app, daemon=True)
        app_thread.start()
        
        # Aguardar app iniciar
        time.sleep(3)
        
        # Testar endpoints
        base_url = "http://localhost:5001"
        
        # Health check
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ Health check funcionando")
            health_data = response.json()
            print(f"   Status: {health_data.get('status')}")
        else:
            print("❌ Health check falhou")
        
        # System status
        response = requests.get(f"{base_url}/api/system-status")
        if response.status_code == 200:
            print("✅ System status funcionando")
            status_data = response.json()
            print(f"   Langflow ativo: {status_data.get('langflow', {}).get('active', False)}")
        else:
            print("❌ System status falhou")
        
        # Chat endpoint
        chat_data = {
            "question": "O que é hanseníase?",
            "personality": "dr_gasnelio"
        }
        response = requests.post(f"{base_url}/api/chat", json=chat_data)
        if response.status_code == 200:
            print("✅ Chat endpoint funcionando")
            chat_result = response.json()
            print(f"   Sucesso: {chat_result.get('success')}")
            print(f"   Fonte: {chat_result.get('source')}")
        else:
            print("❌ Chat endpoint falhou")
        
        return True
        
    except Exception as e:
        print("❌ Erro ao testar endpoints")
        print(f"💡 Erro: {e}")
        return False

def test_pdf_content():
    """Testa se o conteúdo do PDF está disponível"""
    print_step("6", "Verificando conteúdo do PDF")
    
    pdf_path = "PDFs/Roteiro de Dsispensação - Hanseníase.md"
    
    if os.path.exists(pdf_path):
        try:
            with open(pdf_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"✅ PDF encontrado ({len(content)} caracteres)")
            
            if len(content) > 1000:
                print("✅ Conteúdo suficiente para processamento")
                return True
            else:
                print("⚠️ Conteúdo muito pequeno")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao ler PDF: {e}")
            return False
    else:
        print("❌ PDF não encontrado")
        print(f"💡 Caminho esperado: {pdf_path}")
        return False

def generate_test_report(results):
    """Gera relatório de teste"""
    print_header("RELATÓRIO DE TESTE")
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"\n📊 Resumo:")
    print(f"   Total de testes: {total_tests}")
    print(f"   ✅ Passou: {passed_tests}")
    print(f"   ❌ Falhou: {failed_tests}")
    print(f"   📈 Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
    
    print(f"\n📋 Detalhes:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Recomendações:")
    if failed_tests == 0:
        print("   🎉 Todos os testes passaram! Integração funcionando perfeitamente.")
    else:
        print("   🔧 Alguns testes falharam. Verifique as recomendações acima.")
    
    if not results.get("langflow_server"):
        print("   💡 Para usar Langflow: Execute 'langflow run' em outro terminal")
    
    if not results.get("pdf_content"):
        print("   💡 Adicione o PDF da tese na pasta PDFs/")
    
    return passed_tests == total_tests

def main():
    """Função principal"""
    print_header("TESTE DE INTEGRAÇÃO LANGFLOW")
    print(f"🕐 Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Executar testes
    results = {
        "langflow_installation": test_langflow_installation(),
        "langflow_server": test_langflow_server(),
        "integration_module": test_integration_module(),
        "app_integration": test_app_integration(),
        "api_endpoints": test_api_endpoints(),
        "pdf_content": test_pdf_content()
    }
    
    # Gerar relatório
    success = generate_test_report(results)
    
    # Resultado final
    print_header("RESULTADO FINAL")
    if success:
        print("🎉 INTEGRAÇÃO FUNCIONANDO PERFEITAMENTE!")
        print("\n🚀 Próximos passos:")
        print("   1. Execute: langflow run")
        print("   2. Execute: python app_with_langflow.py")
        print("   3. Acesse: http://localhost:5000")
        print("   4. Configure fluxos no Langflow: http://localhost:7860")
    else:
        print("⚠️ ALGUNS PROBLEMAS ENCONTRADOS")
        print("\n🔧 Verifique:")
        print("   1. Se o Langflow está instalado")
        print("   2. Se o servidor Langflow está rodando")
        print("   3. Se o PDF da tese está presente")
        print("   4. Se todas as dependências estão instaladas")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 