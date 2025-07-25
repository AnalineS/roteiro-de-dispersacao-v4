#!/usr/bin/env python3
"""
Script de teste para o chatbot v6
Testa as duas personas e verifica se estão funcionando corretamente
"""

import requests
import json
import time

# Configuração
BASE_URL = "http://localhost:5000"
TEST_QUESTIONS = [
    "O que é hanseníase?",
    "Como funciona a dispensação de medicamentos?",
    "Qual é o objetivo do roteiro?",
    "Quais são os medicamentos usados no tratamento?",
    "Como o farmacêutico deve orientar o paciente?"
]

def test_health_check():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK - Status: {data['status']}")
            print(f"   PDF carregado: {data['pdf_loaded']}")
            print(f"   Personas: {data['personas']}")
            return True
        else:
            print(f"❌ Health check falhou - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
        return False

def test_api_info():
    """Testa o endpoint de informações da API"""
    print("\n🔍 Testando informações da API...")
    try:
        response = requests.get(f"{BASE_URL}/api/info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Info OK - Versão: {data['version']}")
            print(f"   Nome: {data['name']}")
            print(f"   Modelo: {data['model']}")
            return True
        else:
            print(f"❌ API Info falhou - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no API Info: {e}")
        return False

def test_personas():
    """Testa o endpoint de personas"""
    print("\n🔍 Testando endpoint de personas...")
    try:
        response = requests.get(f"{BASE_URL}/api/personas")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Personas OK - {len(data)} personas encontradas")
            for persona_id, persona_data in data.items():
                print(f"   - {persona_id}: {persona_data['name']} ({persona_data['description']})")
            return True
        else:
            print(f"❌ Personas falhou - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no endpoint de personas: {e}")
        return False

def test_chat_response(persona_id, question):
    """Testa uma resposta do chat para uma persona específica"""
    print(f"\n🤖 Testando {persona_id} - Pergunta: '{question}'")
    
    payload = {
        "question": question,
        "personality_id": persona_id
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Resposta recebida:")
            print(f"   Persona: {data.get('persona', 'N/A')}")
            print(f"   Confiança: {data.get('confidence', 'N/A')}")
            print(f"   Resposta: {data.get('answer', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Erro na resposta - Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def test_all_personas():
    """Testa todas as personas com todas as perguntas"""
    print("\n🧪 Testando todas as personas...")
    
    personas = ["dr_gasnelio", "ga"]
    total_tests = len(personas) * len(TEST_QUESTIONS)
    passed_tests = 0
    
    for persona in personas:
        print(f"\n👤 Testando persona: {persona}")
        for question in TEST_QUESTIONS:
            if test_chat_response(persona, question):
                passed_tests += 1
            time.sleep(1)  # Pausa entre requisições
    
    print(f"\n📊 Resultados dos testes:")
    print(f"   Total de testes: {total_tests}")
    print(f"   Testes aprovados: {passed_tests}")
    print(f"   Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
    
    return passed_tests == total_tests

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes do Chatbot v6")
    print("=" * 50)
    
    # Testa endpoints básicos
    if not test_health_check():
        print("❌ Falha no health check - servidor pode não estar rodando")
        return False
    
    if not test_api_info():
        print("❌ Falha no API info")
        return False
    
    if not test_personas():
        print("❌ Falha no endpoint de personas")
        return False
    
    # Testa funcionalidade do chat
    success = test_all_personas()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Todos os testes passaram! Chatbot v6 está funcionando corretamente.")
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")
    
    return success

if __name__ == "__main__":
    main() 