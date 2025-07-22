import requests
import time

def test_simple():
    """Teste simples das melhorias"""
    print("🧪 Teste Simples das Melhorias na Cobertura")
    print("=" * 60)
    
    # Aguardar servidor
    print("⏳ Aguardando servidor...")
    time.sleep(3)
    
    # Testar health
    try:
        health = requests.get('http://localhost:5000/api/health', timeout=5)
        if health.status_code != 200:
            print("❌ Servidor não está rodando")
            return
        print("✅ Servidor OK")
    except:
        print("❌ Servidor não está rodando")
        return
    
    # Perguntas de teste
    test_questions = [
        "O que é hanseníase?",
        "Como funciona a dispensação?",
        "O que é dapsona?",
        "Quais são os sintomas?",
        "Como se transmite?",
        "O que é lepra?",  # Sinônimo
        "Como funciona a terapia?",  # Sinônimo
        "Quais são os sinais?",  # Sinônimo
        "O que é poliquimioterapia?",
        "Como se classifica a doença?"
    ]
    
    print(f"\n🧪 Testando {len(test_questions)} perguntas...")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 {i}. {question}")
        
        try:
            response = requests.post('http://localhost:5000/api/chat', 
                                   json={'question': question, 'personality_id': 'dr_gasnelio'},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '')
                confidence = data.get('confidence', 0)
                source = data.get('source', '')
                
                if answer:
                    print(f"   ✅ Resposta: {answer[:100]}...")
                    print(f"   📊 Confiança: {confidence:.3f}")
                    print(f"   📚 Fonte: {source}")
                else:
                    print(f"   ❌ Sem resposta")
            else:
                print(f"   ❌ Erro: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        time.sleep(0.5)
    
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    test_simple() 