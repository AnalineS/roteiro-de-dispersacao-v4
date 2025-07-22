# Script para instalar Git e fazer push para GitHub
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  INSTALAR GIT E FAZER PUSH AUTOMÁTICO" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Verificar se o Git já está instalado
try {
    $gitVersion = git --version
    Write-Host "✓ Git já está instalado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git não está instalado. Instalando..." -ForegroundColor Red
    
    # Baixar e instalar o Git
    Write-Host "Baixando Git..." -ForegroundColor Yellow
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstaller = "$env:TEMP\GitInstaller.exe"
    
    Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller
    
    Write-Host "Instalando Git..." -ForegroundColor Yellow
    Start-Process -FilePath $gitInstaller -ArgumentList "/VERYSILENT /NORESTART" -Wait
    
    # Atualizar PATH
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")
    
    Write-Host "✓ Git instalado com sucesso!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Verificando repositório Git..." -ForegroundColor Yellow

# Verificar se estamos em um repositório Git
if (-not (Test-Path ".git")) {
    Write-Host "Inicializando repositório Git..." -ForegroundColor Yellow
    git init
    git remote add origin https://github.com/AnalineS/siteroteirodedispersacao.git
}

# Adicionar todos os arquivos
Write-Host "Adicionando arquivos..." -ForegroundColor Yellow
git add .

# Verificar se há mudanças
$status = git status --porcelain
if ($status) {
    Write-Host "Fazendo commit das mudanças..." -ForegroundColor Yellow
    git commit -m "Correção: Remove FastAPI e usa Flask corretamente"
    
    Write-Host "Fazendo push para GitHub..." -ForegroundColor Yellow
    git push origin main
    
    Write-Host ""
    Write-Host "✓ Push realizado com sucesso!" -ForegroundColor Green
    Write-Host "Agora vá para o Render e faça um Manual Deploy" -ForegroundColor Cyan
} else {
    Write-Host "Nenhuma mudança detectada." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Pressione qualquer tecla para continuar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 