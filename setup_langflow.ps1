# ========================================
#    CONFIGURACAO LANGFLOW - POWERSHELL
# ========================================

Write-Host "Iniciando configuração do Langflow..." -ForegroundColor Green

# 1. Verificar Python
Write-Host "`n[1/6] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado!" -ForegroundColor Red
    Write-Host "Instale Python 3.9+ primeiro" -ForegroundColor Yellow
    exit 1
}

# 2. Corrigir versão do NumPy
Write-Host "`n[2/6] Corrigindo versão do NumPy..." -ForegroundColor Yellow
try {
    pip uninstall numpy -y
    pip install "numpy<2.0.0"
    Write-Host "✅ NumPy corrigido" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Problema ao corrigir NumPy" -ForegroundColor Yellow
}

# 3. Verificar Langflow instalado
Write-Host "`n[3/6] Verificando Langflow instalado..." -ForegroundColor Yellow
$langflowPath = "C:\Program Files\Langflow"
if (Test-Path $langflowPath) {
    Write-Host "✅ Langflow encontrado em $langflowPath" -ForegroundColor Green
    
    # 4. Configurar variáveis de ambiente
    Write-Host "`n[4/6] Configurando variáveis de ambiente..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable("LANGFLOW_PATH", $langflowPath, "User")
    Write-Host "✅ Variável LANGFLOW_PATH configurada" -ForegroundColor Green
} else {
    Write-Host "❌ Langflow não encontrado em $langflowPath" -ForegroundColor Red
    Write-Host "💡 Instalando Langflow via pip..." -ForegroundColor Yellow
    try {
        pip install langflow
        Write-Host "✅ Langflow instalado via pip" -ForegroundColor Green
    } catch {
        Write-Host "❌ Erro ao instalar Langflow" -ForegroundColor Red
    }
}

# 5. Instalar dependências Python
Write-Host "`n[5/6] Instalando dependências Python..." -ForegroundColor Yellow
try {
    pip install requests typing-extensions
    Write-Host "✅ Dependências instaladas" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Algumas dependências podem não ter sido instaladas" -ForegroundColor Yellow
}

# 6. Criar arquivo de configuração
Write-Host "`n[6/6] Criando arquivo de configuração..." -ForegroundColor Yellow
$envContent = @"
LANGFLOW_PATH=C:\Program Files\Langflow
LANGFLOW_URL=http://localhost:7860
LANGFLOW_API_KEY=sk-oZkcvhmKOMt0eRUizMCvOPLvgvNT1uEKrtm-Al4oXB4
"@
$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "✅ Arquivo .env criado" -ForegroundColor Green

# Resultado final
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "    CONFIGURACAO CONCLUIDA!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`nPara iniciar o Langflow:" -ForegroundColor Cyan
Write-Host "1. Abra um novo terminal" -ForegroundColor White
Write-Host "2. Execute: .\start_langflow.ps1" -ForegroundColor White
Write-Host "3. Acesse: http://localhost:7860" -ForegroundColor White

Write-Host "`nPara testar a integração:" -ForegroundColor Cyan
Write-Host "1. Execute: python test_langflow_integration.py" -ForegroundColor White
Write-Host "2. Execute: python app_simple_langflow.py" -ForegroundColor White

Write-Host "`nPressione qualquer tecla para continuar..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 