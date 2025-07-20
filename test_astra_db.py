#!/usr/bin/env python3
"""
Teste da integração com Astra DB
"""

import os
import sys
from pathlib import Path

# Carrega variáveis de ambiente
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

def test_astra_credentials():
    """Testa se as credenciais do Astra DB estão configuradas"""
    print("🔑 Verificando credenciais do Astra DB...")
    
    token = os.getenv('ASTRA_DB_TOKEN')
    endpoint = os.getenv('ASTRA_DB_ENDPOINT')
    keyspace = os.getenv('ASTRA_DB_KEYSPACE')
    
    if not token:
        print("❌ ASTRA_DB_TOKEN não configurada")
        return False
    
    if not endpoint:
        print("❌ ASTRA_DB_ENDPOINT não configurada")
        return False
    
    print(f"✅ Token: {token[:20]}...")
    print(f"✅ Endpoint: {endpoint}")
    print(f"✅ Keyspace: {keyspace or 'roteiro_dispersacao_bot'}")
    
    return True

def test_astra_connection():
    """Testa conexão com Astra DB"""
    print("\n🌐 Testando conexão com Astra DB...")
    
    try:
        # Tenta importar bibliotecas
        try:
            from astrapy.db import AstraDB
            print("✅ Biblioteca astrapy disponível")
        except ImportError:
            print("❌ Biblioteca astrapy não encontrada")
            print("💡 Execute: pip install astrapy")
            return False
        
        # Testa conexão
        token = os.getenv('ASTRA_DB_TOKEN')
        endpoint = os.getenv('ASTRA_DB_ENDPOINT')
        keyspace = os.getenv('ASTRA_DB_KEYSPACE', 'roteiro_dispersacao_bot')
        
        if not all([token, endpoint]):
            print("❌ Credenciais não configuradas")
            return False
        
        # Inicializa cliente
        astra_db = AstraDB(
            token=token,
            api_endpoint=endpoint,
            namespace=keyspace
        )
        
        # Testa conexão listando coleções
        collections = astra_db.get_collections()
        print(f"✅ Conexão bem-sucedida!")
        print(f"📚 Coleções encontradas: {len(collections.get('status', {}).get('collections', []))}")
        
        # Mostra coleções existentes
        for collection in collections.get('status', {}).get('collections', []):
            print(f"   - {collection}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False

def test_rag_service():
    """Testa o serviço RAG com Astra DB"""
    print("\n🤖 Testando RAG Service com Astra DB...")
    
    try:
        # Adiciona o diretório backend ao path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        
        from rag_service import RAGService
        
        # Inicializa serviço
        rag = RAGService()
        
        if rag.is_ready():
            print("✅ RAG Service inicializado com sucesso")
            
            # Mostra estatísticas
            stats = rag.get_stats()
            print(f"📊 Estatísticas: {stats}")
            
            # Teste simples de busca (se houver dados)
            try:
                context = rag.retrieve_context("hanseníase", top_k=1)
                if "não encontrei" not in context.lower():
                    print(f"✅ Busca funcionando: {context[:100]}...")
                else:
                    print("⚠️  Nenhum dado encontrado na base (normal se ainda não foi populada)")
            except Exception as e:
                print(f"⚠️  Erro na busca: {str(e)}")
            
            return True
        else:
            print("❌ RAG Service não conseguiu inicializar")
            return False
            
    except ImportError as e:
        print(f"❌ Erro ao importar RAG Service: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        return False

def test_embedding_model():
    """Testa o modelo de embeddings"""
    print("\n🧠 Testando modelo de embeddings...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        # Teste simples
        test_text = "Hanseníase é uma doença tratável"
        embedding = model.encode([test_text])
        
        print(f"✅ Modelo carregado com sucesso")
        print(f"📐 Dimensão do embedding: {embedding.shape[1]}")
        print(f"🔢 Exemplo de embedding: {embedding[0][:5]}...")
        
        return True
        
    except ImportError:
        print("❌ Biblioteca sentence-transformers não encontrada")
        print("💡 Execute: pip install sentence-transformers")
        return False
    except Exception as e:
        print(f"❌ Erro no modelo: {str(e)}")
        return False

def main():
    """Função principal"""
    print("🧪 TESTE DE INTEGRAÇÃO ASTRA DB")
    print("=" * 50)
    
    # Executa testes
    tests = [
        ("Credenciais Astra DB", test_astra_credentials),
        ("Conexão Astra DB", test_astra_connection),
        ("Modelo de Embeddings", test_embedding_model),
        ("RAG Service", test_rag_service)
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
    print("📊 RESUMO DOS TESTES ASTRA DB")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Integração Astra DB funcionando perfeitamente!")
        print("💡 Próximo passo: Execute 'python scripts/build_knowledge_base.py' para popular a base")
    else:
        print("⚠️  Alguns testes falharam. Verifique as configurações.")
        
        if not results.get("Credenciais Astra DB"):
            print("💡 Configure as variáveis ASTRA_DB_TOKEN e ASTRA_DB_ENDPOINT no arquivo .env")
        
        if not results.get("Conexão Astra DB"):
            print("💡 Verifique se as credenciais estão corretas e o banco está ativo")

if __name__ == "__main__":
    main()

