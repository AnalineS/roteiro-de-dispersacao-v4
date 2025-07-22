#!/usr/bin/env python3
"""
Script de teste para a API do Chatbot
"""

import requests
import time

# Configuração
BASE_URL = "http://localhost:5000"

def test_health():
    """Testa o endpoint de saúde"""
    print("🔍 Testando endpoint de saúde...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API saudável!")
            print(f"   - Modelo carregado: {data.get('model_loaded', False)}")
            print(f"   - PDF carregado: {data.get('pdf_loaded', False)}")
            return True
        else:
            print(f"❌ Erro no health check: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def test_info():
    """Testa o endpoint de informações"""
    print("\n📋 Testando endpoint de informações...")
    try:
        response = requests.get(f"{BASE_URL}/api/info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Informações da API:")
            print(f"   - Nome: {data.get('name')}")
            print(f"   - Versão: {data.get('version')}")
            print(f"   - Modelo: {data.get('model')}")
            return True
        else:
            print(f"❌ Erro no info: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def test_chat(question, persona):
    """Testa o endpoint do chat"""
    print(f"\n💬 Testando chat ({persona}): '{question}'")
    try:
        payload = {
            "question": question,
            "persona": persona  # ou "personality"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/chat",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Resposta recebida:")
            print(f"   - Persona: {data.get('persona')}")
            print(f"   - Confiança: {data.get('confidence', 0):.1%}")
            print(f"   - Resposta: {data.get('answer', '')[:100]}...")
            return True
        else:
            print(f"❌ Erro no chat: {response.status_code}")
            print(f"   - Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes da API do Chatbot\n")
    
    # Teste de saúde
    if not test_health():
        print("\n❌ API não está funcionando. Verifique se o servidor está rodando.")
        return
    
    # Teste de informações
    test_info()
    
    # Testes do chat
    test_questions = [
        ("Qual é o objetivo da tese?", "dr_gasnelio"),
        ("Como funciona o roteiro?", "ga"),
        ("O que é hanseníase?", "dr_gasnelio"),
        ("Como tomar os remédios?", "ga"),
        ("Qual a metodologia usada?", "dr_gasnelio")
    ]
    
    print(f"\n🧪 Testando {len(test_questions)} perguntas...")
    
    success_count = 0
    for question, persona in test_questions:
        if test_chat(question, persona):
            success_count += 1
        time.sleep(1)  # Pausa entre requisições
    
    print(f"\n📊 Resultado dos testes:")
    print(f"   - Sucessos: {success_count}/{len(test_questions)}")
    print(f"   - Taxa de sucesso: {success_count/len(test_questions)*100:.1f}%")
    
    if success_count == len(test_questions):
        print("\n🎉 Todos os testes passaram! A API está funcionando corretamente.")
    else:
        print(f"\n⚠️  {len(test_questions) - success_count} teste(s) falharam.")

if __name__ == "__main__":
    main() 