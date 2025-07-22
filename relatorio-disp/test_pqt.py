import requests

def test_pqt_question():
    """Testa a pergunta sobre PQT-U"""
    
    url = "http://localhost:5000/api/chat"
    
    data = {
        "question": "O que é a poliquimioterapia única (PQT-U) para hanseníase?",
        "persona": "dr_gasnelio"
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resposta recebida:")
            print(f"Resposta: {result.get('answer', 'N/A')}")
            print(f"Confiança: {result.get('confidence', 'N/A')}")
            print(f"Fonte: {result.get('source', 'N/A')}")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao servidor. Verifique se o Flask está rodando.")
    except requests.exceptions.Timeout:
        print("❌ Timeout na requisição.")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🧪 Testando pergunta sobre PQT-U...")
    test_pqt_question() 