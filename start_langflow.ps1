# ========================================
#    INICIANDO LANGFLOW - POWERSHELL
# ========================================

Write-Host "Verificando Langflow instalado..." -ForegroundColor Green

$langflowPath = "C:\Program Files\Langflow"
$langflowExe = Join-Path $langflowPath "langflow.exe"

if (Test-Path $langflowExe) {
    Write-Host "✅ Langflow encontrado em $langflowPath" -ForegroundColor Green
    Write-Host "`nIniciando Langflow..." -ForegroundColor Yellow
    Write-Host "`nSe o Langflow iniciou com sucesso:" -ForegroundColor Cyan
    Write-Host "1. Acesse: http://localhost:7860" -ForegroundColor White
    Write-Host "2. Configure seus fluxos" -ForegroundColor White
    Write-Host "3. Em outro terminal, execute: python app_simple_langflow.py" -ForegroundColor White
    Write-Host "`nPressione CTRL+C para parar o Langflow" -ForegroundColor Yellow
    Write-Host "`n" -ForegroundColor White
    
    # Iniciar Langflow
    & $langflowExe run
} else {
    Write-Host "❌ Langflow não encontrado em $langflowPath" -ForegroundColor Red
    Write-Host "`nTentando via pip..." -ForegroundColor Yellow
    
    try {
        langflow run
    } catch {
        Write-Host "❌ Erro ao iniciar Langflow" -ForegroundColor Red
        Write-Host "💡 Execute primeiro: .\setup_langflow.ps1" -ForegroundColor Yellow
    }
} 