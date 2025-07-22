import requests
import time

print("🧪 Teste Rápido das Melhorias")
print("=" * 40)

# Aguardar servidor
print("⏳ Aguardando...")
time.sleep(5)

# Testar uma pergunta
try:
    print("📝 Testando: 'O que é hanseníase?'")
    
    response = requests.post(
        'http://localhost:5000/api/chat',
        json={
            'question': 'O que é hanseníase?',
            'personality_id': 'dr_gasnelio'
        },
        timeout=20
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"💬 Resposta: {data.get('answer', 'N/A')[:150]}...")
        print(f"📊 Confiança: {data.get('confidence', 0):.3f}")
        print(f"📚 Fonte: {data.get('source', 'N/A')}")
    else:
        print(f"❌ Erro: {response.status_code}")
        print(f"📄 Resposta: {response.text}")
        
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n✅ Teste concluído!") 