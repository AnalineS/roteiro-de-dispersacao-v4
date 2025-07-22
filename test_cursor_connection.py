#!/usr/bin/env python3
"""
Teste de conexão para Cursor
"""

import requests

def test_cursor_connection():
    """Testa conexão com serviços do Cursor"""
    
    test_urls = [
        "https://api.cursor.sh",
        "https://cursor.sh",
        "https://httpbin.org/get"
    ]
    
    print("🔍 Testando conexões...")
    
    for url in test_urls:
        try:
            print(f"Testando {url}...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} - OK")
            else:
                print(f"⚠️  {url} - Status {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - Erro: {e}")
    
    print("\n🎯 Se todos os testes falharem, verifique sua conexão com a internet")

if __name__ == "__main__":
    test_cursor_connection()
