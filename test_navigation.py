#!/usr/bin/env python3
"""
Script de teste para verificar a navegação do site
"""

import requests
import time
from urllib.parse import urljoin

def test_site_navigation():
    """Testa a navegação do site"""
    base_url = "https://repositorio-roteiro-de-dispersacao.onrender.com"
    
    print("🔍 Testando navegação do site...")
    print(f"URL base: {base_url}")
    print("-" * 50)
    
    # Lista de URLs para testar
    urls_to_test = [
        "/",
        "/tese",
        "/script.js",
        "/tese.js",
        "/api/health",
        "/api/info"
    ]
    
    results = []
    
    for url in urls_to_test:
        full_url = urljoin(base_url, url)
        print(f"Testando: {full_url}")
        
        try:
            start_time = time.time()
            response = requests.get(full_url, timeout=30)
            end_time = time.time()
            
            status = "✅" if response.status_code == 200 else "❌"
            response_time = round((end_time - start_time) * 1000, 2)
            
            result = {
                "url": full_url,
                "status_code": response.status_code,
                "response_time": response_time,
                "success": response.status_code == 200
            }
            
            print(f"  {status} Status: {response.status_code} | Tempo: {response_time}ms")
            
            if response.status_code != 200:
                print(f"     Erro: {response.text[:100]}...")
            
            results.append(result)
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Erro de conexão: {e}")
            results.append({
                "url": full_url,
                "status_code": None,
                "response_time": None,
                "success": False,
                "error": str(e)
            })
        
        time.sleep(1)  # Pausa entre requisições
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    successful_tests = sum(1 for r in results if r["success"])
    total_tests = len(results)
    
    print(f"Testes bem-sucedidos: {successful_tests}/{total_tests}")
    print(f"Taxa de sucesso: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests == total_tests:
        print("\n🎉 Todos os testes passaram! O site está funcionando corretamente.")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os problemas acima.")
    
    # Teste específico da API de chat
    print("\n🤖 Testando API de Chat...")
    try:
        chat_url = urljoin(base_url, "/api/chat")
        chat_data = {
            "question": "O que é hanseníase?",
            "personality_id": "dr_gasnelio"
        }
        
        response = requests.post(chat_url, json=chat_data, timeout=30)
        
        if response.status_code == 200:
            print("✅ API de chat funcionando!")
            response_data = response.json()
            if "answer" in response_data:
                print(f"   Resposta recebida: {len(response_data['answer'])} caracteres")
            else:
                print("   ⚠️  Resposta sem campo 'answer'")
        else:
            print(f"❌ API de chat falhou: {response.status_code}")
            print(f"   Erro: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Erro ao testar API de chat: {e}")
    
    return results

if __name__ == "__main__":
    test_site_navigation() 