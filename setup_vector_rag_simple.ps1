Write-Host "Configurando Vector Store RAG..." -ForegroundColor Cyan

# Criar arquivo de configuração
$config = @"
LANGFLOW_URL=http://localhost:7860
LANGFLOW_API_KEY=sk-oZkcvhmKOMt0eRUizMCvOPLvgvNT1uEKrtm-Al4oXB4
VECTOR_STORE_ENABLED=true
RAG_ENABLED=true
PDF_PATH=PDFs/Roteiro de Dsispensacao - Hanseniase.md
EMBEDDING_MODEL=text-embedding-ada-002
LLM_MODEL=gpt-3.5-turbo
"@

$config | Out-File -FilePath ".env_vector_rag" -Encoding UTF8
Write-Host "Arquivo .env_vector_rag criado" -ForegroundColor Green

# Verificar se Langflow está rodando
$processes = Get-Process | Where-Object { $_.ProcessName -like "*langflow*" -or $_.ProcessName -like "*Langflow*" }
if ($processes) {
    Write-Host "Langflow encontrado: $($processes.Count) processo" -ForegroundColor Green
} else {
    Write-Host "Langflow nao encontrado" -ForegroundColor Red
}

Write-Host "Configuracao concluida!" -ForegroundColor Green
Write-Host "Acesse: http://localhost:7860" -ForegroundColor Yellow
Write-Host "Execute: python app_vector_store_rag.py" -ForegroundColor Yellow 