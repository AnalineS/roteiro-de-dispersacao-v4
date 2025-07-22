# ========================================
#    CORRIGIR CONEXÃO LANGFLOW
# ========================================

Write-Host "Corrigindo conexão do Langflow..." -ForegroundColor Green

# 1. Matar processo atual
Write-Host "`n[1/4] Matando processo atual..." -ForegroundColor Yellow
$langflowProcesses = Get-Process | Where-Object {$_.ProcessName -like "*langflow*"}
if ($langflowProcesses) {
    Write-Host "Encontrados processos Langflow:" -ForegroundColor White
    $langflowProcesses | ForEach-Object {
        Write-Host "   - PID: $($_.Id), Nome: $($_.ProcessName)" -ForegroundColor White
        try {
            Stop-Process -Id $_.Id -Force
            Write-Host "   ✅ Processo $($_.Id) finalizado" -ForegroundColor Green
        } catch {
            Write-Host "   ❌ Erro ao finalizar processo $($_.Id)" -ForegroundColor Red
        }
    }
    Start-Sleep -Seconds 3
} else {
    Write-Host "✅ Nenhum processo Langflow encontrado" -ForegroundColor Green
}

# 2. Verificar se a porta está livre
Write-Host "`n[2/4] Verificando porta 7860..." -ForegroundColor Yellow
$port7860 = netstat -ano | findstr :7860
if ($port7860) {
    Write-Host "⚠️ Porta 7860 ainda em uso:" -ForegroundColor Yellow
    Write-Host $port7860 -ForegroundColor White
    
    # Extrair PID e matar
    $processId = ($port7860 -split '\s+')[-1]
    try {
        Stop-Process -Id $processId -Force
        Write-Host "✅ Processo $processId finalizado" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } catch {
        Write-Host "❌ Erro ao finalizar processo $processId" -ForegroundColor Red
    }
} else {
    Write-Host "✅ Porta 7860 livre" -ForegroundColor Green
}

# 3. Iniciar Langflow corretamente
Write-Host "`n[3/4] Iniciando Langflow..." -ForegroundColor Yellow
$langflowPath = "C:\Program Files\Langflow"
$langflowExe = Join-Path $langflowPath "langflow.exe"

if (Test-Path $langflowExe) {
    Write-Host "Usando executável: $langflowExe" -ForegroundColor White
    
    # Iniciar em background com redirecionamento de saída
    $job = Start-Job -ScriptBlock {
        param($exePath)
        & $exePath run 2>&1
    } -ArgumentList $langflowExe
    
    Write-Host "✅ Langflow iniciado (Job ID: $($job.Id))" -ForegroundColor Green
} else {
    Write-Host "Executável não encontrado, tentando via pip..." -ForegroundColor Yellow
    $job = Start-Job -ScriptBlock {
        langflow run 2>&1
    }
    Write-Host "✅ Langflow iniciado via pip (Job ID: $($job.Id))" -ForegroundColor Green
}

# 4. Aguardar e verificar
Write-Host "`n[4/4] Aguardando inicialização..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0

while ($attempt -lt $maxAttempts) {
    $attempt++
    Write-Host "   Tentativa $attempt/$maxAttempts..." -ForegroundColor Gray
    
    # Verificar se a porta está em uso
    $portCheck = netstat -ano | findstr :7860
    if ($portCheck) {
        Write-Host "✅ Porta 7860 está em uso!" -ForegroundColor Green
        Write-Host $portCheck -ForegroundColor White
        break
    }
    
    # Verificar se há erros no job
    $jobStatus = Get-Job -Id $job.Id
    if ($jobStatus.State -eq "Failed") {
        Write-Host "❌ Job falhou" -ForegroundColor Red
        $jobOutput = Receive-Job -Id $job.Id
        Write-Host "Erro: $jobOutput" -ForegroundColor Red
        break
    }
    
    Start-Sleep -Seconds 2
}

# 5. Testar conexão HTTP
Write-Host "`nTestando conexão HTTP..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:7860/api/v1/health" -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Langflow está respondendo!" -ForegroundColor Green
        Write-Host "   Status: $($response.StatusCode)" -ForegroundColor White
    } else {
        Write-Host "⚠️ Langflow respondeu com status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Erro ao conectar: $($_.Exception.Message)" -ForegroundColor Red
}

# Resultado final
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "    RESULTADO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

$finalPortCheck = netstat -ano | findstr :7860
if ($finalPortCheck) {
    Write-Host "✅ Langflow está rodando na porta 7860" -ForegroundColor Green
    Write-Host "🌐 Acesse: http://localhost:7860" -ForegroundColor Cyan
    Write-Host "💡 Para parar: Stop-Job $($job.Id)" -ForegroundColor Yellow
} else {
    Write-Host "❌ Langflow não está escutando na porta 7860" -ForegroundColor Red
    Write-Host "💡 Verifique os logs do job para mais detalhes" -ForegroundColor Yellow
}

Write-Host "`nPressione qualquer tecla para continuar..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 