# ========================================
#    INICIAR LANGFLOW - VERSÃO ROBUSTA
# ========================================

Write-Host "Iniciando Langflow de forma robusta..." -ForegroundColor Green

# Função para verificar se Langflow está respondendo
function Test-LangflowHealth {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:7860/api/v1/health" -TimeoutSec 3
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

# Função para aguardar Langflow iniciar
function Wait-ForLangflow {
    Write-Host "Aguardando Langflow iniciar..." -ForegroundColor Yellow
    $maxAttempts = 30
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        if (Test-LangflowHealth) {
            Write-Host "✅ Langflow está respondendo!" -ForegroundColor Green
            return $true
        }
        
        $attempt++
        Write-Host "   Tentativa $attempt/$maxAttempts..." -ForegroundColor Gray
        Start-Sleep -Seconds 2
    }
    
    Write-Host "❌ Langflow não respondeu após $maxAttempts tentativas" -ForegroundColor Red
    return $false
}

# 1. Verificar se já está rodando
Write-Host "`n[1/5] Verificando se Langflow já está rodando..." -ForegroundColor Yellow
if (Test-LangflowHealth) {
    Write-Host "✅ Langflow já está rodando!" -ForegroundColor Green
    Write-Host "   URL: http://localhost:7860" -ForegroundColor White
    return
}

# 2. Verificar instalação
Write-Host "`n[2/5] Verificando instalação..." -ForegroundColor Yellow
$langflowPath = "C:\Program Files\Langflow"
$langflowExe = Join-Path $langflowPath "langflow.exe"

if (Test-Path $langflowExe) {
    Write-Host "✅ Langflow encontrado em $langflowPath" -ForegroundColor Green
} else {
    Write-Host "❌ Langflow não encontrado em $langflowPath" -ForegroundColor Red
    Write-Host "💡 Tentando via pip..." -ForegroundColor Yellow
    
    try {
        # Tentar instalar via pip
        pip install langflow
        Write-Host "✅ Langflow instalado via pip" -ForegroundColor Green
    } catch {
        Write-Host "❌ Erro ao instalar Langflow" -ForegroundColor Red
        return
    }
}

# 3. Verificar porta
Write-Host "`n[3/5] Verificando porta 7860..." -ForegroundColor Yellow
$port7860 = netstat -ano | findstr :7860
if ($port7860) {
    Write-Host "⚠️ Porta 7860 já está em uso:" -ForegroundColor Yellow
    Write-Host $port7860 -ForegroundColor White
    
    # Perguntar se quer matar o processo
    $response = Read-Host "Deseja matar o processo e reiniciar? (s/n)"
    if ($response -eq "s" -or $response -eq "S") {
        $processId = ($port7860 -split '\s+')[-1]
        try {
            Stop-Process -Id $processId -Force
            Write-Host "✅ Processo $processId finalizado" -ForegroundColor Green
            Start-Sleep -Seconds 2
        } catch {
            Write-Host "❌ Erro ao finalizar processo" -ForegroundColor Red
        }
    }
}

# 4. Iniciar Langflow
Write-Host "`n[4/5] Iniciando Langflow..." -ForegroundColor Yellow

if (Test-Path $langflowExe) {
    Write-Host "   Usando executável: $langflowExe" -ForegroundColor White
    
    # Iniciar em background
    $job = Start-Job -ScriptBlock {
        param($exePath)
        & $exePath run
    } -ArgumentList $langflowExe
    
    Write-Host "✅ Langflow iniciado em background (Job ID: $($job.Id))" -ForegroundColor Green
} else {
    Write-Host "   Usando comando: langflow run" -ForegroundColor White
    
    # Iniciar em background
    $job = Start-Job -ScriptBlock {
        langflow run
    }
    
    Write-Host "✅ Langflow iniciado em background (Job ID: $($job.Id))" -ForegroundColor Green
}

# 5. Aguardar inicialização
Write-Host "`n[5/5] Aguardando inicialização..." -ForegroundColor Yellow
if (Wait-ForLangflow) {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "    LANGFLOW INICIADO COM SUCESSO!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    
    Write-Host "`n🌐 URLs:" -ForegroundColor Cyan
    Write-Host "   Langflow: http://localhost:7860" -ForegroundColor White
    Write-Host "   Chatbot: http://localhost:5000" -ForegroundColor White
    
    Write-Host "`n📋 Próximos passos:" -ForegroundColor Cyan
    Write-Host "   1. Acesse http://localhost:7860" -ForegroundColor White
    Write-Host "   2. Configure seus fluxos" -ForegroundColor White
    Write-Host "   3. Em outro terminal: python app_simple_langflow.py" -ForegroundColor White
    
    Write-Host "`n💡 Para parar: Stop-Job $($job.Id)" -ForegroundColor Yellow
} else {
    Write-Host "`n❌ Falha ao iniciar Langflow" -ForegroundColor Red
    Write-Host "💡 Verifique os logs e tente novamente" -ForegroundColor Yellow
}

Write-Host "`nPressione qualquer tecla para continuar..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 