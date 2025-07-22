# Script de configuração para Netlify (PowerShell)
# Configura todos os arquivos necessários para o deploy

Write-Host "🔧 Configurando arquivos para deploy no Netlify..." -ForegroundColor Green

# 1. Criar requirements.txt
if (-not (Test-Path "requirements.txt")) {
    Write-Host "📝 Criando requirements.txt..." -ForegroundColor Cyan
    @"
flask==2.3.3
flask-cors==4.0.0
transformers==4.35.0
torch==2.1.0
sentence-transformers==2.2.2
PyPDF2==3.0.1
numpy==1.24.3
requests==2.31.0
python-dotenv==1.0.0
huggingface-hub==0.19.4
scikit-learn==1.3.0
scipy==1.11.1
accelerate==0.24.1
tokenizers==0.15.0
protobuf==4.24.4
packaging==23.2
regex==2023.10.3
tqdm==4.66.1
safetensors==0.4.0
filelock==3.13.1
typing-extensions==4.8.0
sympy==1.12
networkx==3.2.1
mpmath==1.3.0
markdown-it-py==3.0.0
mdurl==0.1.2
pyyaml==6.0.1
fsspec==2023.10.0
jinja2==3.1.2
psutil==5.9.6
pandas==2.1.3
pytz==2023.3
six==1.16.0
python-dateutil==2.8.2
pytz-deprecation-shim==0.1.0.post0
tzdata==2023.3
urllib3==2.0.7
certifi==2023.11.17
charset-normalizer==3.3.2
idna==3.6
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8
    Write-Host "✅ requirements.txt criado" -ForegroundColor Green
} else {
    Write-Host "✅ requirements.txt já existe" -ForegroundColor Green
}

# 2. Criar pasta functions
if (-not (Test-Path "functions")) {
    Write-Host "📁 Criando pasta functions..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path "functions" -Force | Out-Null
}

# 3. Criar netlify.toml
if (-not (Test-Path "netlify.toml")) {
    Write-Host "📝 Criando netlify.toml..." -ForegroundColor Cyan
    @"
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
"@ | Out-File -FilePath "netlify.toml" -Encoding UTF8
    Write-Host "✅ netlify.toml criado" -ForegroundColor Green
} else {
    Write-Host "✅ netlify.toml já existe" -ForegroundColor Green
}

# 4. Criar pasta PDFs
if (-not (Test-Path "PDFs")) {
    Write-Host "📁 Criando pasta PDFs..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path "PDFs" -Force | Out-Null
    Write-Host "⚠️  ATENÇÃO: Adicione o PDF da tese na pasta PDFs/" -ForegroundColor Yellow
}

# 5. Criar .gitignore
if (-not (Test-Path ".gitignore")) {
    Write-Host "📝 Criando .gitignore..." -ForegroundColor Cyan
    @"
# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Cache
.cache/
*.cache

# Netlify
.netlify/

# Temporary files
*.tmp
*.temp
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✅ .gitignore criado" -ForegroundColor Green
} else {
    Write-Host "✅ .gitignore já existe" -ForegroundColor Green
}

# 6. Criar runtime.txt
if (-not (Test-Path "runtime.txt")) {
    Write-Host "📝 Criando runtime.txt..." -ForegroundColor Cyan
    "python-3.9.18" | Out-File -FilePath "runtime.txt" -Encoding UTF8
    Write-Host "✅ runtime.txt criado" -ForegroundColor Green
} else {
    Write-Host "✅ runtime.txt já existe" -ForegroundColor Green
}

# 7. Criar .python-version
if (-not (Test-Path ".python-version")) {
    Write-Host "📝 Criando .python-version..." -ForegroundColor Cyan
    "3.9.18" | Out-File -FilePath ".python-version" -Encoding UTF8
    Write-Host "✅ .python-version criado" -ForegroundColor Green
} else {
    Write-Host "✅ .python-version já existe" -ForegroundColor Green
}

Write-Host "✅ Configuração concluída!" -ForegroundColor Green
Write-Host "🚀 Arquivos criados/verificados:" -ForegroundColor Cyan
Write-Host "   - requirements.txt (dependências Python)" -ForegroundColor Gray
Write-Host "   - netlify.toml (configuração do Netlify)" -ForegroundColor Gray
Write-Host "   - pasta PDFs/ (para o arquivo da tese)" -ForegroundColor Gray
Write-Host "   - .gitignore (arquivos ignorados)" -ForegroundColor Gray
Write-Host "   - runtime.txt (versão do Python)" -ForegroundColor Gray
Write-Host "   - .python-version (versão do Python)" -ForegroundColor Gray

Write-Host "📝 Próximos passos:" -ForegroundColor Yellow
Write-Host "   1. Adicione o PDF da tese na pasta PDFs/" -ForegroundColor Gray
Write-Host "   2. Execute: git add . ; git commit -m 'Configuração Netlify' ; git push" -ForegroundColor Gray
Write-Host "   3. Configure o deploy no Netlify com build command: bash netlify_build_fix.sh" -ForegroundColor Gray

Write-Host "✅ Script setup_netlify.ps1 executado com sucesso!" -ForegroundColor Green 