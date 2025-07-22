#!/usr/bin/env python3
"""
Teste simples do chat
"""

import requests
import os
ASTRA_DB_ENDPOINT = os.environ.get("ASTRA_DB_ENDPOINT")
ASTRA_DB_TOKEN = os.environ.get("ASTRA_DB_TOKEN")
OPENROUTER_API_KEYROTEIRO_DISP_KIMIE_K2FREE = os.environ.get("OPENROUTER_API_KEYROTEIRO_DISP_KIMIE_K2FREE")

def test_chat():
    """Testa o chat localmente"""
    url = "http://localhost:5000/api/chat"
    
    # Teste 1: Dr. Gasnelio
    data = {
        "question": "O que é hanseníase?",
        "personality_id": "dr_gasnelio"
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat funcionando!")
            print(f"Resposta: {result.get('answer', 'N/A')}")
            print(f"Confiança: {result.get('confidence', 0)}")
            print(f"Fonte: {result.get('source', 'N/A')}")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    test_chat() 