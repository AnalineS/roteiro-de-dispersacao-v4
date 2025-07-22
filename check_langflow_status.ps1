# ========================================
#    VERIFICAR STATUS LANGFLOW
# ========================================

Write-Host "Verificando status do Langflow..." -ForegroundColor Green

# 1. Verificar se o processo está rodando
Write-Host "`n[1/4] Verificando processos Langflow..." -ForegroundColor Yellow
$langflowProcesses = Get-Process | Where-Object {$_.ProcessName -like "*langflow*"}
if ($langflowProcesses) {
    Write-Host "✅ Processos Langflow encontrados:" -ForegroundColor Green
    $langflowProcesses | ForEach-Object {
        Write-Host "   - PID: $($_.Id), Nome: $($_.ProcessName)" -ForegroundColor White
    }
} else {
    Write-Host "❌ Nenhum processo Langflow encontrado" -ForegroundColor Red
}

# 2. Verificar porta 7860
Write-Host "`n[2/4] Verificando porta 7860..." -ForegroundColor Yellow
$port7860 = netstat -ano | findstr :7860
if ($port7860) {
    Write-Host "✅ Porta 7860 está em uso:" -ForegroundColor Green
    Write-Host $port7860 -ForegroundColor White
} else {
    Write-Host "❌ Porta 7860 não está em uso" -ForegroundColor Red
}

# 3. Testar conexão HTTP
Write-Host "`n[3/4] Testando conexão HTTP..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:7860/api/v1/health" -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Langflow respondeu com sucesso!" -ForegroundColor Green
        Write-Host "   Status: $($response.StatusCode)" -ForegroundColor White
    } else {
        Write-Host "⚠️ Langflow respondeu com status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Erro ao conectar com Langflow: $($_.Exception.Message)" -ForegroundColor Red
}

# 4. Verificar arquivo de configuração
Write-Host "`n[4/4] Verificando configuração..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ Arquivo .env encontrado" -ForegroundColor Green
    $envContent = Get-Content ".env"
    Write-Host "   Conteúdo:" -ForegroundColor White
    $envContent | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
} else {
    Write-Host "❌ Arquivo .env não encontrado" -ForegroundColor Red
}

# Recomendações
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "    RECOMENDAÇÕES" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

if (-not $langflowProcesses) {
    Write-Host "`n🔧 Langflow não está rodando:" -ForegroundColor Yellow
    Write-Host "   1. Execute: .\start_langflow.ps1" -ForegroundColor White
    Write-Host "   2. Aguarde alguns segundos" -ForegroundColor White
    Write-Host "   3. Verifique se não há erros no terminal" -ForegroundColor White
}

if (-not $port7860) {
    Write-Host "`n🔧 Porta 7860 não está em uso:" -ForegroundColor Yellow
    Write-Host "   1. Langflow pode não ter iniciado corretamente" -ForegroundColor White
    Write-Host "   2. Verifique se há erros no terminal do Langflow" -ForegroundColor White
}

Write-Host "`n💡 Para reiniciar tudo:" -ForegroundColor Cyan
Write-Host "   1. Pare todos os processos (CTRL+C)" -ForegroundColor White
Write-Host "   2. Execute: .\start_langflow.ps1" -ForegroundColor White
Write-Host "   3. Em outro terminal: python app_simple_langflow.py" -ForegroundColor White

Write-Host "`nPressione qualquer tecla para continuar..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 