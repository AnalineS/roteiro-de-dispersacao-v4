# Deploy Automático para Render
# Script PowerShell para automatizar o deploy no Render

param(
    [string]$ServiceName = "roteiro-dispersacao",
    [string]$Region = "oregon",
    [switch]$Force = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 DEPLOY AUTOMATICO PARA RENDER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se o Render CLI está instalado
function Test-RenderCLI {
    try {
        $renderVersion = render --version 2>$null
        if ($renderVersion) {
            Write-Host "Render CLI encontrado: $renderVersion" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "Render CLI nao encontrado" -ForegroundColor Red
        return $false
    }
    return $false
}

# Instalar Render CLI se necessário
function Install-RenderCLI {
    Write-Host "📦 Instalando Render CLI..." -ForegroundColor Yellow
    
    # Tentar instalar via winget
    try {
        winget install render.render-cli
        Write-Host "✅ Render CLI instalado via winget" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "⚠️  Falha ao instalar via winget, tentando via chocolatey..." -ForegroundColor Yellow
        try {
            choco install render-cli
            Write-Host "✅ Render CLI instalado via chocolatey" -ForegroundColor Green
            return $true
        }
        catch {
            Write-Host "❌ Falha ao instalar Render CLI automaticamente" -ForegroundColor Red
            Write-Host "📋 Instale manualmente: https://render.com/docs/install-cli" -ForegroundColor Yellow
            return $false
        }
    }
}

# Verificar arquivos necessários
function Test-RequiredFiles {
    $requiredFiles = @(
        "app_optimized.py",
        "requirements.txt",
        "runtime.txt",
        "render.yaml",
        "templates",
        "static",
        "PDFs"
    )
    
    $missingFiles = @()
    
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            $missingFiles += $file
        }
    }
    
    if ($missingFiles.Count -gt 0) {
        Write-Host "❌ Arquivos faltando:" -ForegroundColor Red
        foreach ($file in $missingFiles) {
            Write-Host "   - $file" -ForegroundColor Red
        }
        return $false
    }
    
    Write-Host "✅ Todos os arquivos necessários encontrados" -ForegroundColor Green
    return $true
}

# Criar pacote de deploy
function New-DeploymentPackage {
    Write-Host "📦 Criando pacote de deploy..." -ForegroundColor Yellow
    
    $deployDir = "deploy_package"
    
    # Limpar diretório anterior
    if (Test-Path $deployDir) {
        Remove-Item $deployDir -Recurse -Force
    }
    
    # Criar novo diretório
    New-Item -ItemType Directory -Path $deployDir | Out-Null
    
    # Copiar arquivos
    $filesToCopy = @(
        "app_optimized.py",
        "requirements.txt",
        "runtime.txt",
        "gunicorn.conf.py",
        "render.yaml"
    )
    
    foreach ($file in $filesToCopy) {
        if (Test-Path $file) {
            Copy-Item $file $deployDir
            Write-Host "   ✅ Copiado: $file" -ForegroundColor Green
        }
    }
    
    # Copiar diretórios
    $dirsToCopy = @("templates", "static", "PDFs", "functions")
    
    foreach ($dir in $dirsToCopy) {
        if (Test-Path $dir) {
            Copy-Item $dir $deployDir -Recurse
            Write-Host "   ✅ Copiado: $dir/" -ForegroundColor Green
        }
    }
    
    # Criar ZIP
    $zipPath = "deploy_render.zip"
    if (Test-Path $zipPath) {
        Remove-Item $zipPath -Force
    }
    
    Compress-Archive -Path "$deployDir\*" -DestinationPath $zipPath -Force
    
    $size = (Get-Item $zipPath).Length / 1MB
    Write-Host "Pacote criado: $zipPath ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
    
    return $zipPath
}

# Deploy via Render CLI
function Deploy-RenderCLI {
    param([string]$ZipPath)
    
    Write-Host "Iniciando deploy via Render CLI..." -ForegroundColor Yellow
    
    try {
        # Verificar se já existe o serviço
        $existingService = render services list --format json | ConvertFrom-Json | Where-Object { $_.name -eq $ServiceName }
        
        if ($existingService -and -not $Force) {
            Write-Host "⚠️  Serviço '$ServiceName' já existe" -ForegroundColor Yellow
            Write-Host "   Use -Force para sobrescrever ou configure manualmente" -ForegroundColor Yellow
            return $false
        }
        
        # Criar novo serviço
        Write-Host "📋 Criando serviço no Render..." -ForegroundColor Yellow
        
        $deployCmd = "render services create --name $ServiceName --type web --env python --region $Region --build-command 'pip install -r requirements.txt' --start-command 'gunicorn app_optimized:app --bind 0.0.0.0:`$PORT --workers 1 --timeout 120'"
        
        Write-Host "Executando: $deployCmd" -ForegroundColor Gray
        Invoke-Expression $deployCmd
        
        Write-Host "✅ Deploy iniciado com sucesso!" -ForegroundColor Green
        Write-Host "🌐 URL: https://$ServiceName.onrender.com" -ForegroundColor Cyan
        
        return $true
    }
    catch {
        Write-Host "❌ Erro no deploy: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Deploy manual (instruções)
function Show-ManualDeployInstructions {
    param([string]$ZipPath)
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "📋 INSTRUÇÕES PARA DEPLOY MANUAL" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. 📁 Acesse: https://dashboard.render.com" -ForegroundColor White
    Write-Host "2. ➕ Clique em 'New +' e selecione 'Web Service'" -ForegroundColor White
    Write-Host "3. 📤 Faça upload do arquivo: $ZipPath" -ForegroundColor White
    Write-Host "4. ⚙️  Configure:" -ForegroundColor White
    Write-Host "   - Name: $ServiceName" -ForegroundColor Gray
    Write-Host "   - Environment: Python" -ForegroundColor Gray
    Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor Gray
    Write-Host "   - Start Command: gunicorn app_optimized:app --bind 0.0.0.0:`$PORT --workers 1 --timeout 120" -ForegroundColor Gray
    Write-Host "5. 🚀 Clique em 'Create Web Service'" -ForegroundColor White
    Write-Host ""
    Write-Host "🌐 Após o deploy, acesse: https://$ServiceName.onrender.com" -ForegroundColor Cyan
    Write-Host ""
}

# Função principal
function Main {
    # Verificar arquivos
    if (-not (Test-RequiredFiles)) {
        Write-Host "❌ Falha na verificação de arquivos" -ForegroundColor Red
        exit 1
    }
    
    # Criar pacote
    $zipPath = New-DeploymentPackage
    if (-not $zipPath) {
        Write-Host "❌ Falha ao criar pacote de deploy" -ForegroundColor Red
        exit 1
    }
    
    # Tentar deploy automático
    if (Test-RenderCLI) {
        if (Deploy-RenderCLI -ZipPath $zipPath) {
            Write-Host "🎉 Deploy automático concluído!" -ForegroundColor Green
            return
        }
    } else {
        # Tentar instalar CLI
        if (Install-RenderCLI) {
            if (Deploy-RenderCLI -ZipPath $zipPath) {
                Write-Host "🎉 Deploy automático concluído!" -ForegroundColor Green
                return
            }
        }
    }
    
    # Fallback para deploy manual
    Write-Host "🔄 Fallback para deploy manual..." -ForegroundColor Yellow
    Show-ManualDeployInstructions -ZipPath $zipPath
}

# Executar função principal
Main 