import requests
import time

def test_synonym_questions():
    """Testa perguntas com sinônimos para verificar se as melhorias funcionam"""
    print("🧪 Teste de Sinônimos e Melhorias")
    print("=" * 50)
    
    # Aguardar servidor
    print("⏳ Aguardando servidor...")
    time.sleep(3)
    
    # Perguntas que testam sinônimos
    test_pairs = [
        ("O que é hanseníase?", "O que é lepra?"),
        ("Como funciona o tratamento?", "Como funciona a terapia?"),
        ("Quais são os sintomas?", "Quais são os sinais?"),
        ("O que é dispensação?", "Como funciona a entrega de medicamentos?"),
        ("O que é dapsona?", "O que é DDS?"),
        ("O que é poliquimioterapia?", "O que é PQT?"),
        ("O que é paucibacilar?", "O que é PB?"),
        ("O que é multibacilar?", "O que é MB?")
    ]
    
    for i, (original, synonym) in enumerate(test_pairs, 1):
        print(f"\n📝 Teste {i}: {original}")
        print(f"🔄 Sinônimo: {synonym}")
        
        # Testar pergunta original
        try:
            response1 = requests.post(
                'http://localhost:5000/api/chat',
                json={'question': original, 'personality_id': 'dr_gasnelio'},
                timeout=15
            )
            
            if response1.status_code == 200:
                data1 = response1.json()
                answer1 = data1.get('answer', '')
                conf1 = data1.get('confidence', 0)
                source1 = data1.get('source', '')
                
                print(f"   📝 Original: {answer1[:80]}..." if answer1 else "   📝 Original: Sem resposta")
                print(f"   📊 Confiança: {conf1:.3f}")
                print(f"   📚 Fonte: {source1}")
            else:
                print(f"   ❌ Erro original: {response1.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro original: {e}")
        
        time.sleep(1)
        
        # Testar sinônimo
        try:
            response2 = requests.post(
                'http://localhost:5000/api/chat',
                json={'question': synonym, 'personality_id': 'dr_gasnelio'},
                timeout=15
            )
            
            if response2.status_code == 200:
                data2 = response2.json()
                answer2 = data2.get('answer', '')
                conf2 = data2.get('confidence', 0)
                source2 = data2.get('source', '')
                
                print(f"   🔄 Sinônimo: {answer2[:80]}..." if answer2 else "   🔄 Sinônimo: Sem resposta")
                print(f"   📊 Confiança: {conf2:.3f}")
                print(f"   📚 Fonte: {source2}")
                
                # Comparar respostas
                if answer1 and answer2:
                    if conf2 > conf1:
                        print(f"   ✅ Sinônimo melhorou a confiança!")
                    elif conf1 > conf2:
                        print(f"   ⚠️  Original teve melhor confiança")
                    else:
                        print(f"   ➡️  Confianças similares")
                        
            else:
                print(f"   ❌ Erro sinônimo: {response2.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro sinônimo: {e}")
        
        print("-" * 50)
        time.sleep(1)
    
    print("\n✅ Teste de sinônimos concluído!")

if __name__ == "__main__":
    test_synonym_questions() 