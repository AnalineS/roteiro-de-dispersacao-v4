#!/usr/bin/env python3
"""
Teste simples do sistema RAG sem dependências complexas
"""

import os
import sys
import json
from pathlib import Path

# Simula o sistema RAG básico
class SimpleRAG:
    def __init__(self):
        self.documents = []
        self.is_ready = False
    
    def load_document(self, file_path):
        """Carrega um documento Markdown"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Divide em chunks simples por parágrafos
            chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
            self.documents.extend(chunks)
            self.is_ready = True
            
            print(f"✅ Documento carregado: {len(chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar documento: {e}")
            return False
    
    def search(self, query, top_k=3):
        """Busca simples por palavras-chave"""
        if not self.is_ready:
            return []
        
        query_words = query.lower().split()
        scored_docs = []
        
        for i, doc in enumerate(self.documents):
            score = 0
            doc_lower = doc.lower()
            
            for word in query_words:
                score += doc_lower.count(word)
            
            if score > 0:
                scored_docs.append((score, i, doc))
        
        # Ordena por score e retorna top_k
        scored_docs.sort(reverse=True)
        return [doc for _, _, doc in scored_docs[:top_k]]

def test_personas():
    """Testa as personas definidas"""
    print("\n=== TESTE DAS PERSONAS ===")
    
    personas = {
        'dr_gasnelio': {
            'name': 'Dr. Gasnelio',
            'style': 'técnica, culta, profissional',
            'greeting': 'Saudações! Sou o Dr. Gasnelio. Minha pesquisa foca no roteiro de dispensação para a prática da farmácia clínica.'
        },
        'ga': {
            'name': 'Gá',
            'style': 'simples, empática, amigável',
            'greeting': 'Oi! Sou o Gá, seu amigo virtual para tirar dúvidas sobre saúde. Vou explicar tudo de um jeito bem fácil!'
        }
    }
    
    for persona_id, info in personas.items():
        print(f"\n👤 {info['name']} ({info['style']}):")
        print(f"   {info['greeting']}")
    
    return personas

def test_rag_system():
    """Testa o sistema RAG básico"""
    print("\n=== TESTE DO SISTEMA RAG ===")
    
    # Inicializa RAG
    rag = SimpleRAG()
    
    # Carrega documento de exemplo
    data_dir = Path(__file__).parent / 'data'
    tese_path = data_dir / 'tese_exemplo.md'
    
    if not tese_path.exists():
        print(f"❌ Arquivo não encontrado: {tese_path}")
        return False
    
    if not rag.load_document(tese_path):
        return False
    
    # Testa buscas
    test_queries = [
        "hanseníase paucibacilar",
        "rifampicina dapsona",
        "efeitos adversos",
        "cuidados com os pés",
        "farmácia clínica"
    ]
    
    print(f"\n📚 Total de chunks na base: {len(rag.documents)}")
    
    for query in test_queries:
        print(f"\n🔍 Busca: '{query}'")
        results = rag.search(query, top_k=2)
        
        if results:
            for i, result in enumerate(results, 1):
                preview = result[:100] + "..." if len(result) > 100 else result
                print(f"   {i}. {preview}")
        else:
            print("   Nenhum resultado encontrado")
    
    return True

def test_openrouter_config():
    """Testa configuração do OpenRouter"""
    print("\n=== TESTE CONFIGURAÇÃO OPENROUTER ===")
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if api_key:
        print(f"✅ API Key configurada: {api_key[:20]}...")
        print("✅ Modelo: moonshot/moonshot-v1-8k (Kimie K2)")
        return True
    else:
        print("❌ OPENROUTER_API_KEY não configurada")
        return False

def simulate_chat_interaction():
    """Simula uma interação de chat"""
    print("\n=== SIMULAÇÃO DE CHAT ===")
    
    # Carrega RAG
    rag = SimpleRAG()
    data_dir = Path(__file__).parent / 'data'
    tese_path = data_dir / 'tese_exemplo.md'
    
    if tese_path.exists():
        rag.load_document(tese_path)
    
    # Simula perguntas
    test_cases = [
        {
            'persona': 'dr_gasnelio',
            'question': 'Qual o esquema terapêutico para hanseníase multibacilar?',
            'expected_style': 'técnico e detalhado'
        },
        {
            'persona': 'ga',
            'question': 'Como devo tomar os remédios para hanseníase?',
            'expected_style': 'simples e empático'
        }
    ]
    
    for case in test_cases:
        print(f"\n👤 Persona: {case['persona']}")
        print(f"❓ Pergunta: {case['question']}")
        
        # Busca contexto
        context = rag.search(case['question'], top_k=2)
        
        if context:
            print(f"📖 Contexto encontrado: {len(context)} chunks")
            print(f"🎯 Estilo esperado: {case['expected_style']}")
            
            # Simula resposta baseada na persona
            if case['persona'] == 'dr_gasnelio':
                print("💬 Resposta simulada (Dr. Gasnelio):")
                print("   'Com base na literatura científica, o esquema terapêutico para hanseníase multibacilar...'")
            else:
                print("💬 Resposta simulada (Gá):")
                print("   'Oi! Então, sobre os remédios para hanseníase, é assim: você vai tomar...'")
        else:
            print("❌ Nenhum contexto encontrado")

def main():
    """Função principal de teste"""
    print("🧪 TESTE DO SISTEMA ROTEIRO DE DISPERSAÇÃO V4")
    print("=" * 50)
    
    # Carrega variáveis de ambiente
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        print("✅ Arquivo .env encontrado")
        # Simula carregamento das variáveis
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    else:
        print("⚠️  Arquivo .env não encontrado")
    
    # Executa testes
    tests = [
        ("Personas", test_personas),
        ("Sistema RAG", test_rag_system),
        ("Configuração OpenRouter", test_openrouter_config),
        ("Simulação de Chat", simulate_chat_interaction)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results[test_name] = False
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Sistema pronto para próxima fase.")
    else:
        print("⚠️  Alguns testes falharam. Verifique as configurações.")

if __name__ == "__main__":
    main()

