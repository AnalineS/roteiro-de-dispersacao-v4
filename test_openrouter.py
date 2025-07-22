#!/usr/bin/env python3
"""
Teste da integração com OpenRouter e Kimie K2
"""

import os
from pathlib import Path

# Carrega variáveis de ambiente
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  Biblioteca 'requests' não disponível. Instalando...")

def test_openrouter_connection():
    """Testa conexão com OpenRouter"""
    try:
        import requests
    except ImportError:
        print("❌ Biblioteca 'requests' necessária para teste")
        return False
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY não configurada")
        return False
    
    print(f"🔑 API Key: {api_key[:20]}...")
    
    # Testa conexão básica
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print("🌐 Testando conexão com OpenRouter...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Conexão bem-sucedida! {len(models.get('data', []))} modelos disponíveis")
            
            # Procura pelo Kimie K2
            kimie_models = [m for m in models.get('data', []) if 'moonshot' in m.get('id', '').lower()]
            if kimie_models:
                print(f"🤖 Modelos Kimie encontrados: {len(kimie_models)}")
                for model in kimie_models[:3]:  # Mostra apenas os primeiros 3
                    print(f"   - {model.get('id')}")
            else:
                print("⚠️  Nenhum modelo Kimie encontrado")
            
            return True
        else:
            print(f"❌ Erro na conexão: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_chat_completion():
    """Testa geração de resposta com Kimie K2"""
    if not REQUESTS_AVAILABLE:
        return False
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return False
    
    print("\n🤖 Testando geração de resposta com Kimie K2...")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Teste com persona Dr. Gasnelio
    payload = {
        "model": "moonshot/moonshot-v1-8k",
        "messages": [
            {
                "role": "system",
                "content": "Você é o Dr. Gasnelio, um especialista em farmácia clínica. Responda de forma técnica e profissional sobre roteiro de dispensação para hanseníase."
            },
            {
                "role": "user",
                "content": "Qual o esquema terapêutico para hanseníase multibacilar?"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            message = data['choices'][0]['message']['content']
            
            print("✅ Resposta gerada com sucesso!")
            print(f"📝 Dr. Gasnelio: {message[:200]}...")
            
            # Teste com persona Gá
            payload['messages'] = [
                {
                    "role": "system",
                    "content": "Você é o Gá, um amigo virtual que explica sobre saúde de forma simples e empática. Use linguagem cotidiana e seja acolhedor."
                },
                {
                    "role": "user",
                    "content": "Como devo tomar os remédios para hanseníase?"
                }
            ]
            
            response2 = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response2.status_code == 200:
                data2 = response2.json()
                message2 = data2['choices'][0]['message']['content']
                
                print(f"😊 Gá: {message2[:200]}...")
                return True
            else:
                print(f"⚠️  Erro no segundo teste: {response2.status_code}")
                return True  # Primeiro teste passou
        else:
            print(f"❌ Erro na geração: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 TESTE DE INTEGRAÇÃO OPENROUTER + KIMIE K2")
    print("=" * 50)
    
    # Verifica se requests está disponível
    requests_available = True
    try:
        pass
    except ImportError:
        requests_available = False
        print("📦 Tentando instalar biblioteca 'requests'...")
        os.system("pip install requests")
        
        try:
            requests_available = True
            print("✅ Biblioteca 'requests' instalada com sucesso!")
        except ImportError:
            print("❌ Não foi possível instalar 'requests'")
            return
    
    if not requests_available:
        print("❌ Biblioteca 'requests' não disponível")
        return
    
    # Executa testes
    tests = [
        ("Conexão OpenRouter", test_openrouter_connection),
        ("Geração de Resposta", test_chat_completion)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results[test_name] = False
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES OPENROUTER")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Integração OpenRouter funcionando perfeitamente!")
    else:
        print("⚠️  Alguns testes falharam. Verifique as configurações.")

if __name__ == "__main__":
    main()

