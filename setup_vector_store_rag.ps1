# Script para configurar Vector Store RAG no Langflow
Write-Host "🔧 Configurando Vector Store RAG no Langflow..." -ForegroundColor Cyan

# 1. Verificar se o Langflow está rodando
Write-Host "`n[1/5] Verificando Langflow..." -ForegroundColor Yellow
$langflowProcesses = Get-Process | Where-Object { $_.ProcessName -like "*langflow*" -or $_.ProcessName -like "*Langflow*" }
if ($langflowProcesses) {
    Write-Host "✅ Langflow encontrado: $($langflowProcesses.Count) processo" -ForegroundColor Green
} else {
    Write-Host "❌ Langflow não encontrado - iniciando..." -ForegroundColor Red
    Start-Job -ScriptBlock { & "C:\Program Files\Langflow\langflow.exe" serve } -Name "Langflow"
    Start-Sleep -Seconds 10
}

# 2. Aguardar inicialização completa
Write-Host "`n[2/5] Aguardando inicialização..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$langflowReady = $false

while ($attempt -lt $maxAttempts -and -not $langflowReady) {
    $attempt++
    Write-Host "   Tentativa $attempt/$maxAttempts..." -ForegroundColor Gray
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:7860" -TimeoutSec 3 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $langflowReady = $true
            Write-Host "✅ Langflow respondendo!" -ForegroundColor Green
        }
    } catch {
        Start-Sleep -Seconds 2
    }
}

if (-not $langflowReady) {
    Write-Host "❌ Langflow não respondeu após $maxAttempts tentativas" -ForegroundColor Red
    Write-Host "💡 Tente acessar manualmente: http://localhost:7860" -ForegroundColor Yellow
}

# 3. Criar configuração para Vector Store RAG
Write-Host "`n[3/5] Criando configuração Vector Store RAG..." -ForegroundColor Yellow

$configContent = @"
# Configuração Vector Store RAG para Langflow
LANGFLOW_URL=http://localhost:7860
LANGFLOW_API_KEY=sk-oZkcvhmKOMt0eRUizMCvOPLvgvNT1uEKrtm-Al4oXB4
VECTOR_STORE_ENABLED=true
RAG_ENABLED=true
PDF_PATH=PDFs/Roteiro de Dsispensação - Hanseníase.md
EMBEDDING_MODEL=text-embedding-ada-002
LLM_MODEL=gpt-3.5-turbo
"@

$configContent | Out-File -FilePath ".env_vector_rag" -Encoding UTF8
Write-Host "✅ Arquivo .env_vector_rag criado" -ForegroundColor Green

# 4. Criar script de teste para Vector Store RAG
Write-Host "`n[4/5] Criando script de teste..." -ForegroundColor Yellow

$testScript = @"
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('.env_vector_rag')

def test_vector_store_rag():
    """Testa a integração Vector Store RAG com Langflow"""
    
    langflow_url = os.getenv('LANGFLOW_URL', 'http://localhost:7860')
    api_key = os.getenv('LANGFLOW_API_KEY')
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Teste 1: Health Check
    try:
        response = requests.get(f'{langflow_url}/api/v1/health', headers=headers, timeout=10)
        print(f"✅ Health Check: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check falhou: {e}")
        return False
    
    # Teste 2: Listar componentes disponíveis
    try:
        response = requests.get(f'{langflow_url}/api/v1/components', headers=headers, timeout=10)
        if response.status_code == 200:
            components = response.json()
            vector_components = [c for c in components if 'vector' in c.get('name', '').lower()]
            print(f"✅ Componentes Vector Store encontrados: {len(vector_components)}")
        else:
            print(f"❌ Erro ao listar componentes: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao listar componentes: {e}")
    
    # Teste 3: Criar fluxo Vector Store RAG
    flow_data = {
        "name": "Hanseníase Vector Store RAG",
        "description": "Fluxo para perguntas sobre hanseníase usando Vector Store",
        "data": {
            "nodes": [
                {
                    "id": "input_node",
                    "type": "InputNode",
                    "data": {"input_type": "text"}
                },
                {
                    "id": "vector_store",
                    "type": "VectorStoreNode", 
                    "data": {"embedding_model": "text-embedding-ada-002"}
                },
                {
                    "id": "llm_node",
                    "type": "LLMNode",
                    "data": {"model": "gpt-3.5-turbo"}
                }
            ],
            "edges": [
                {"source": "input_node", "target": "vector_store"},
                {"source": "vector_store", "target": "llm_node"}
            ]
        }
    }
    
    try:
        response = requests.post(f'{langflow_url}/api/v1/flows', 
                               headers=headers, 
                               json=flow_data, 
                               timeout=10)
        if response.status_code in [200, 201]:
            print("✅ Fluxo Vector Store RAG criado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao criar fluxo: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao criar fluxo: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testando Vector Store RAG...")
    success = test_vector_store_rag()
    if success:
        print("🎉 Vector Store RAG configurado com sucesso!")
    else:
        print("⚠️ Alguns testes falharam - verifique a configuração")
"@

$testScript | Out-File -FilePath "test_vector_store_rag.py" -Encoding UTF8
Write-Host "✅ Script de teste criado" -ForegroundColor Green

# 5. Instruções finais
Write-Host "`n[5/5] Configuração concluída!" -ForegroundColor Green
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "    VECTOR STORE RAG CONFIGURADO!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "`n📋 Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Acesse: http://localhost:7860" -ForegroundColor White
Write-Host "2. Configure um fluxo Vector Store RAG:" -ForegroundColor White
Write-Host "   - Input → Document Loader → Text Splitter → Vector Store → LLM → Output" -ForegroundColor Gray
Write-Host "3. Execute: python test_vector_store_rag.py" -ForegroundColor White
Write-Host "4. Execute: python app_simple_langflow.py" -ForegroundColor White
Write-Host "`n🔧 Para parar o Langflow: Stop-Job -Name 'Langflow'" -ForegroundColor Gray
Write-Host "=========================================" -ForegroundColor Cyan

Read-Host "`nPressione Enter para continuar..." 