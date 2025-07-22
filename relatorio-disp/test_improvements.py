import requests
import time

def test_question(question, personality_id="dr_gasnelio"):
    """Testa uma pergunta no chatbot"""
    try:
        response = requests.post('http://localhost:5000/api/chat', 
                               json={'question': question, 'personality_id': personality_id},
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n❓ Pergunta: {question}")
            print(f"🤖 Personalidade: {data.get('personality', 'N/A')}")
            print(f"💬 Resposta: {data.get('answer', 'N/A')}")
            print(f"📊 Confiança: {data.get('confidence', 0):.3f}")
            print(f"📚 Fonte: {data.get('source', 'N/A')}")
            print("-" * 80)
            return data
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def main():
    print("🧪 Testando Melhorias na Cobertura das Respostas")
    print("=" * 80)
    
    # Aguardar servidor inicializar
    print("⏳ Aguardando servidor inicializar...")
    time.sleep(5)
    
    # Testar health check
    try:
        health = requests.get('http://localhost:5000/api/health', timeout=10)
        if health.status_code == 200:
            health_data = health.json()
            print(f"✅ Servidor saudável: PDF carregado={health_data.get('pdf_loaded')}, Modelos={health_data.get('models_loaded')}")
        else:
            print("❌ Servidor não está respondendo")
            return
    except:
        print("❌ Servidor não está rodando")
        return
    
    # Lista de perguntas para testar a cobertura melhorada
    test_questions = [
        # Perguntas básicas sobre hanseníase
        "O que é hanseníase?",
        "Como se transmite a hanseníase?",
        "Quais são os sintomas da hanseníase?",
        
        # Perguntas sobre tratamento
        "Como é o tratamento da hanseníase?",
        "Quais medicamentos são usados no tratamento?",
        "O que é poliquimioterapia?",
        "Quanto tempo dura o tratamento?",
        
        # Perguntas sobre medicamentos específicos
        "O que é dapsona?",
        "Para que serve a rifampicina?",
        "Como funciona a clofazimina?",
        
        # Perguntas sobre classificação
        "O que significa paucibacilar?",
        "O que é hanseníase multibacilar?",
        "Como se classifica a hanseníase?",
        
        # Perguntas sobre dispensação
        "Como funciona a dispensação dos medicamentos?",
        "Quem pode dispensar medicamentos para hanseníase?",
        "Onde os medicamentos são dispensados?",
        
        # Perguntas com sinônimos
        "O que é lepra?",
        "Como funciona a terapia para hanseníase?",
        "Quais são os sinais da doença?",
        
        # Perguntas sobre diagnóstico
        "Como é feito o diagnóstico?",
        "Quais exames são necessários?",
        "Quem pode diagnosticar hanseníase?",
        
        # Perguntas sobre prevenção
        "Como prevenir hanseníase?",
        "Existe vacina para hanseníase?",
        "Como evitar o contágio?",
        
        # Perguntas sobre complicações
        "Quais são as complicações da hanseníase?",
        "O que são reações hansênicas?",
        "Como tratar as deformidades?",
        
        # Perguntas sobre monitoramento
        "Como monitorar o tratamento?",
        "Quais são os efeitos adversos?",
        "Como acompanhar a evolução?",
        
        # Perguntas específicas do PDF
        "O que é o roteiro de dispensação?",
        "Quais são os critérios para dispensação?",
        "Como funciona a notificação de casos?",
        
        # Perguntas que podem não ter resposta
        "Qual é a cura definitiva da hanseníase?",
        "Existe tratamento caseiro para hanseníase?",
        "Posso tratar hanseníase com ervas medicinais?"
    ]
    
    print(f"\n🧪 Testando {len(test_questions)} perguntas...")
    
    # Estatísticas
    total_questions = len(test_questions)
    answered_questions = 0
    high_confidence_answers = 0
    low_confidence_answers = 0
    no_answers = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Teste {i}/{total_questions}")
        
        # Testar com Dr. Gasnelio
        result = test_question(question, "dr_gasnelio")
        
        if result:
            answered_questions += 1
            confidence = result.get('confidence', 0)
            result.get('source', '')
            
            if confidence > 0.5:
                high_confidence_answers += 1
            elif confidence > 0.25:
                low_confidence_answers += 1
            else:
                no_answers += 1
        
        # Pequena pausa entre perguntas
        time.sleep(1)
    
    # Relatório final
    print("\n" + "=" * 80)
    print("📊 RELATÓRIO FINAL")
    print("=" * 80)
    print(f"📝 Total de perguntas testadas: {total_questions}")
    print(f"✅ Perguntas respondidas: {answered_questions}")
    print(f"🎯 Respostas com alta confiança (>50%): {high_confidence_answers}")
    print(f"⚠️  Respostas com baixa confiança (25-50%): {low_confidence_answers}")
    print(f"❌ Sem resposta (<25%): {no_answers}")
    print(f"📈 Taxa de cobertura: {(answered_questions/total_questions)*100:.1f}%")
    print(f"🎯 Taxa de alta confiança: {(high_confidence_answers/total_questions)*100:.1f}%")
    
    if answered_questions > 0:
        print(f"📊 Confiança média: {((high_confidence_answers + low_confidence_answers*0.375)/answered_questions)*100:.1f}%")

if __name__ == "__main__":
    main() 