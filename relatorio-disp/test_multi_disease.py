#!/usr/bin/env python3
"""
Script de teste para o sistema multi-doenças
"""

import requests
import time
import sys

def test_api_endpoint(url, method="GET", data=None):
    """Testa um endpoint da API"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Erro {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Erro de conexão: {e}"

def test_health_check():
    """Testa o endpoint de saúde"""
    print("🏥 Testando saúde do sistema...")
    success, result = test_api_endpoint("http://localhost:5000/api/health")
    
    if success:
        print("✅ Sistema saudável!")
        print(f"   - Doenças carregadas: {result.get('diseases_loaded', 0)}")
        print(f"   - Modelos carregados: {result.get('models_loaded', False)}")
        print(f"   - Timestamp: {result.get('timestamp', 'N/A')}")
        return True
    else:
        print(f"❌ Erro: {result}")
        return False

def test_diseases_list():
    """Testa a listagem de doenças"""
    print("\n📚 Testando listagem de doenças...")
    success, result = test_api_endpoint("http://localhost:5000/api/diseases")
    
    if success:
        print(f"✅ {len(result)} doenças encontradas:")
        for disease in result:
            status = "✅" if disease.get('pdf_exists') else "❌"
            print(f"   {status} {disease['name']} ({disease['id']})")
        return True
    else:
        print(f"❌ Erro: {result}")
        return False

def test_personalities():
    """Testa a listagem de personalidades"""
    print("\n👨‍⚕️ Testando personalidades...")
    
    # Testar para hanseníase
    success, result = test_api_endpoint("http://localhost:5000/api/diseases/hanseniase/personalities")
    
    if success:
        print(f"✅ {len(result)} personalidades para hanseníase:")
        for personality in result:
            print(f"   - {personality['name']} ({personality['style']})")
        return True
    else:
        print(f"❌ Erro: {result}")
        return False

def test_chat_questions():
    """Testa perguntas no chat"""
    print("\n💬 Testando perguntas no chat...")
    
    test_questions = [
        {
            "question": "O que é hanseníase?",
            "disease_id": "hanseniase",
            "personality_id": "dr_gasnelio"
        },
        {
            "question": "Como tratar diabetes?",
            "disease_id": "diabetes",
            "personality_id": "ga"
        },
        {
            "question": "Quais são os sintomas da hipertensão?",
            "disease_id": "hipertensao",
            "personality_id": "dr_gasnelio"
        }
    ]
    
    all_success = True
    
    for i, test in enumerate(test_questions, 1):
        print(f"\n   Teste {i}: {test['question']}")
        print(f"   Doença: {test['disease_id']}, Personalidade: {test['personality_id']}")
        
        success, result = test_api_endpoint(
            "http://localhost:5000/api/chat",
            method="POST",
            data=test
        )
        
        if success:
            print(f"   ✅ Resposta recebida")
            print(f"   - Personalidade: {result.get('personality', 'N/A')}")
            print(f"   - Confiança: {result.get('confidence', 0):.2f}")
            print(f"   - Fonte: {result.get('source', 'N/A')}")
            print(f"   - Resposta: {result.get('answer', 'N/A')[:100]}...")
        else:
            print(f"   ❌ Erro: {result}")
            all_success = False
    
    return all_success

def test_web_interface():
    """Testa a interface web"""
    print("\n🌐 Testando interface web...")
    
    # Testar página inicial
    success, result = test_api_endpoint("http://localhost:5000/")
    
    if success:
        print("✅ Página inicial carregada")
    else:
        print(f"❌ Erro na página inicial: {result}")
        return False
    
    # Testar página de chat
    success, result = test_api_endpoint("http://localhost:5000/chat?disease=hanseniase&personality=dr_gasnelio")
    
    if success:
        print("✅ Página de chat carregada")
        return True
    else:
        print(f"❌ Erro na página de chat: {result}")
        return False

def test_performance():
    """Testa performance do sistema"""
    print("\n⚡ Testando performance...")
    
    start_time = time.time()
    
    # Fazer 5 perguntas rápidas
    for i in range(5):
        success, result = test_api_endpoint(
            "http://localhost:5000/api/chat",
            method="POST",
            data={
                "question": f"Pergunta teste {i+1}",
                "disease_id": "hanseniase",
                "personality_id": "dr_gasnelio"
            }
        )
        
        if not success:
            print(f"❌ Erro na pergunta {i+1}: {result}")
            return False
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / 5
    
    print(f"✅ Performance OK")
    print(f"   - Tempo total: {total_time:.2f}s")
    print(f"   - Tempo médio por pergunta: {avg_time:.2f}s")
    
    if avg_time < 5.0:  # Menos de 5 segundos por pergunta
        print("   - Performance: Boa")
        return True
    else:
        print("   - Performance: Lenta")
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("=" * 60)
    print("    TESTE COMPLETO DO CHATBOT MULTI-DOENÇAS")
    print("=" * 60)
    print()
    
    tests = [
        ("Saúde do Sistema", test_health_check),
        ("Listagem de Doenças", test_diseases_list),
        ("Personalidades", test_personalities),
        ("Interface Web", test_web_interface),
        ("Perguntas no Chat", test_chat_questions),
        ("Performance", test_performance)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste '{test_name}': {e}")
            results.append((test_name, False))
    
    # Resumo final
    print("\n" + "=" * 60)
    print("    RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Sistema funcionando perfeitamente.")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")
        return False

def main():
    """Função principal"""
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Teste rápido apenas da saúde
        print("🏥 Teste rápido - verificando saúde do sistema...")
        if test_health_check():
            print("✅ Sistema funcionando!")
            return 0
        else:
            print("❌ Sistema com problemas!")
            return 1
    
    # Teste completo
    success = run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 