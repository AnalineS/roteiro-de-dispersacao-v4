# Script de Deploy para Produção
Write-Host "🚀 DEPLOY PARA PRODUÇÃO - NOVA VERSÃO" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

Write-Host ""
Write-Host "📋 Verificando arquivos essenciais..." -ForegroundColor Cyan

# Verificar arquivos essenciais
$files = @(
    "requirements.txt",
    "netlify.toml", 
    "functions/api.py",
    "index.html",
    "PDFs/Roteiro de Dsispensação - Hanseníase F.docx.pdf"
)

$allFilesExist = $true
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file não encontrado" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host ""
    Write-Host "❌ ERRO: Alguns arquivos essenciais estão faltando!" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""
Write-Host "🔧 Configurando arquivos para produção..." -ForegroundColor Cyan

# Criar netlify_production.toml
$netlifyConfig = @"
[build]
  publish = "."
  command = "bash netlify_build_fix.sh"
  functions = "functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/api/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  PYTHON_VERSION = "3.9"
  NODE_VERSION = "18"
  ENABLE_SYNONYMS = "true"
  ENABLE_CONTEXT_EXTRACTION = "true"
  CONFIDENCE_THRESHOLD = "0.3"
  MAX_CHUNKS = "3"
  CHUNK_SIZE = "1500"
  CHUNK_OVERLAP = "300"

[functions]
  directory = "functions"
  node_bundler = "esbuild"
  included_files = ["PDFs/**/*"]
  external_node_modules = ["@netlify/functions"]

[[headers]]
  for = "/api/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Access-Control-Allow-Headers = "Content-Type"
    Access-Control-Allow-Methods = "POST, OPTIONS"
"@

$netlifyConfig | Out-File -FilePath "netlify_production.toml" -Encoding UTF8
Write-Host "✅ netlify_production.toml criado" -ForegroundColor Green

Write-Host ""
Write-Host "📦 Criando arquivo ZIP para deploy..." -ForegroundColor Cyan

# Lista de arquivos para incluir no ZIP
$filesToZip = @(
    "requirements.txt",
    "netlify_production.toml", 
    "netlify_build_fix.sh",
    "functions",
    "index.html",
    "PDFs",
    ".gitignore",
    "runtime.txt",
    ".python-version"
)

# Criar ZIP
try {
    Compress-Archive -Path $filesToZip -DestinationPath "deploy_producao.zip" -Force
    Write-Host "✅ deploy_producao.zip criado com sucesso!" -ForegroundColor Green
    
    # Mostrar tamanho do arquivo
    $zipFile = Get-ChildItem "deploy_producao.zip"
    $sizeMB = [math]::Round($zipFile.Length / 1MB, 2)
    Write-Host "📊 Tamanho do arquivo: $sizeMB MB" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Erro ao criar ZIP: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""
Write-Host "🎯 OPÇÕES DE DEPLOY:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣ DEPLOY AUTOMÁTICO (Recomendado):" -ForegroundColor Green
Write-Host "   - Vá para https://netlify.com" -ForegroundColor Gray
Write-Host "   - Faça login ou crie conta" -ForegroundColor Gray
Write-Host "   - Clique em 'Add new site' → 'Deploy manually'" -ForegroundColor Gray
Write-Host "   - Arraste o arquivo deploy_producao.zip" -ForegroundColor Gray
Write-Host "   - Configure:" -ForegroundColor Gray
Write-Host "     • Build command: bash netlify_build_fix.sh" -ForegroundColor Gray
Write-Host "     • Publish directory: ." -ForegroundColor Gray
Write-Host "     • Functions directory: functions" -ForegroundColor Gray
Write-Host ""
Write-Host "2️⃣ DEPLOY VIA GITHUB:" -ForegroundColor Cyan
Write-Host "   - Se você tem Git instalado, execute:" -ForegroundColor Gray
Write-Host "     git add ." -ForegroundColor Gray
Write-Host "     git commit -m 'Nova versão para produção'" -ForegroundColor Gray
Write-Host "     git push origin main" -ForegroundColor Gray
Write-Host "   - Conecte seu repositório no Netlify" -ForegroundColor Gray
Write-Host ""
Write-Host "3️⃣ DEPLOY MANUAL:" -ForegroundColor Magenta
Write-Host "   - Use o arquivo deploy_producao.zip" -ForegroundColor Gray
Write-Host "   - Faça upload no Netlify" -ForegroundColor Gray

Write-Host ""
Write-Host "📝 ARQUIVOS INCLUÍDOS NO DEPLOY:" -ForegroundColor Yellow
Write-Host "   ✅ requirements.txt (dependências Python)" -ForegroundColor Gray
Write-Host "   ✅ netlify_production.toml (configuração otimizada)" -ForegroundColor Gray
Write-Host "   ✅ netlify_build_fix.sh (script de build)" -ForegroundColor Gray
Write-Host "   ✅ functions/api.py (API do chatbot)" -ForegroundColor Gray
Write-Host "   ✅ index.html (interface do usuário)" -ForegroundColor Gray
Write-Host "   ✅ PDFs/ (arquivo da tese)" -ForegroundColor Gray
Write-Host "   ✅ .gitignore (arquivos ignorados)" -ForegroundColor Gray
Write-Host "   ✅ runtime.txt (versão Python)" -ForegroundColor Gray
Write-Host "   ✅ .python-version (compatibilidade)" -ForegroundColor Gray

Write-Host ""
Write-Host "🚀 PRONTO PARA DEPLOY!" -ForegroundColor Green
Write-Host "O arquivo deploy_producao.zip está pronto para upload no Netlify." -ForegroundColor Cyan

Write-Host ""
Write-Host "💡 DICA: Abra o arquivo deploy_producao.zip para verificar se tudo está correto." -ForegroundColor Yellow

Read-Host "Pressione Enter para abrir a pasta com o arquivo ZIP"
Start-Process "." 