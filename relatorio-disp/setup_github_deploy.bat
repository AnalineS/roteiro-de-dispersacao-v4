@echo off
echo ========================================
echo  SETUP GITHUB ACTIONS - NETLIFY DEPLOY
echo ========================================
echo.

echo [1/8] Verificando se o Git esta instalado...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Git nao esta instalado!
    echo Instale o Git em: https://git-scm.com/download/win
    echo Depois execute este script novamente.
    pause
    exit /b 1
)

echo [2/8] Verificando se estamos em um repositorio Git...
git status >nul 2>&1
if errorlevel 1 (
    echo Inicializando repositorio Git...
    git init
    git remote add origin https://github.com/AnalineS/siteroteirodedispersacao.git
)

echo [3/8] Criando pasta .github/workflows...
if not exist ".github" mkdir .github
if not exist ".github\workflows" mkdir .github\workflows

echo [4/8] Copiando workflow do GitHub Actions...
copy "github_netlify_deploy.yml" ".github\workflows\deploy.yml" >nul
if errorlevel 1 (
    echo ERRO: Falha ao copiar workflow
    pause
    exit /b 1
)

echo [5/8] Adicionando arquivos ao Git...
git add .
git add -f PDFs/
git add -f functions/
git add -f requirements.txt
git add -f netlify_build_fix.sh
git add -f netlify.toml
git add -f index.html
git add -f script.js

echo [6/8] Verificando se ha mudancas para commitar...
git status --porcelain | findstr . >nul
if errorlevel 1 (
    echo Nenhuma mudanca detectada.
) else (
    echo [7/8] Fazendo commit das mudancas...
    git commit -m "Setup deploy automático com GitHub Actions e melhorias do chatbot"
    if errorlevel 1 (
        echo ERRO: Falha ao fazer commit!
        pause
        exit /b 1
    )
)

echo [8/8] Fazendo push para o GitHub...
git push -u origin main
if errorlevel 1 (
    echo ERRO: Falha ao fazer push!
    echo Verifique se o repositorio remoto esta configurado corretamente.
    echo Execute: git remote -v
    pause
    exit /b 1
)

echo.
echo ========================================
echo  SUCESSO! GITHUB ACTIONS CONFIGURADO
echo ========================================
echo.
echo ✅ Workflow criado: .github/workflows/deploy.yml
echo ✅ Arquivos enviados para: https://github.com/AnalineS/siteroteirodedispersacao
echo.
echo 🚀 Proximos passos:
echo 1. Acesse: https://app.netlify.com/
echo 2. "Add new site" > "Import an existing project"
echo 3. Conecte com GitHub: AnalineS/siteroteirodedispersacao
echo 4. Configure:
echo    - Build command: bash netlify_build_fix.sh
echo    - Publish directory: .
echo    - Functions directory: functions
echo    - Python version: 3.9
echo 5. Clique em "Deploy site"
echo.
echo 🔄 Apos configurado, cada push para main fara deploy automatico!
echo.
pause 