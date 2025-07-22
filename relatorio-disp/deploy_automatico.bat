@echo off
echo ========================================
echo  DEPLOY AUTOMATICO - NETLIFY FIX
echo ========================================
echo.

echo [1/8] Verificando estrutura...
if not exist "PDFs" (
    echo ERRO: Pasta PDFs nao encontrada!
    echo Crie a pasta PDFs e adicione o PDF da tese.
    pause
    exit /b 1
)

echo [2/8] Copiando configuracao automatica...
copy "netlify_auto_fix.toml" "netlify.toml" >nul
if errorlevel 1 (
    echo ERRO: Falha ao copiar netlify_auto_fix.toml
    pause
    exit /b 1
)

echo [3/8] Verificando script de build...
if not exist "netlify_build_fix.sh" (
    echo ERRO: netlify_build_fix.sh nao encontrado!
    pause
    exit /b 1
)

echo [4/8] Criando arquivo ZIP otimizado...
powershell "Compress-Archive -Path 'netlify_build_fix.sh', 'netlify.toml', 'PDFs', 'index.html', 'script.js', 'requirements.txt', 'functions' -DestinationPath 'deploy_automatico.zip' -Force" >nul 2>&1
if errorlevel 1 (
    echo ERRO: Falha ao criar ZIP
    pause
    exit /b 1
)

echo [5/8] Verificando arquivos essenciais...
if not exist "deploy_automatico.zip" (
    echo ERRO: ZIP nao foi criado!
    pause
    exit /b 1
)

echo [6/8] Criando guia de deploy...
echo # 🚀 DEPLOY AUTOMATICO - NETLIFY > DEPLOY_AUTO_GUIDE.md
echo. >> DEPLOY_AUTO_GUIDE.md
echo ## ✅ Arquivo ZIP Criado: deploy_automatico.zip >> DEPLOY_AUTO_GUIDE.md
echo. >> DEPLOY_AUTO_GUIDE.md
echo ### Passo a Passo: >> DEPLOY_AUTO_GUIDE.md
echo 1. Acesse: https://app.netlify.com/ >> DEPLOY_AUTO_GUIDE.md
echo 2. Clique em "Add new site" >> DEPLOY_AUTO_GUIDE.md
echo 3. Selecione "Deploy manually" >> DEPLOY_AUTO_GUIDE.md
echo 4. Arraste o arquivo deploy_automatico.zip >> DEPLOY_AUTO_GUIDE.md
echo 5. Configure: >> DEPLOY_AUTO_GUIDE.md
echo    - Build command: bash netlify_build_fix.sh >> DEPLOY_AUTO_GUIDE.md
echo    - Publish directory: . >> DEPLOY_AUTO_GUIDE.md
echo    - Functions directory: functions >> DEPLOY_AUTO_GUIDE.md
echo    - Python version: 3.9 >> DEPLOY_AUTO_GUIDE.md
echo 6. Clique em "Deploy site" >> DEPLOY_AUTO_GUIDE.md

echo [7/8] Verificando tamanho do ZIP...
for %%A in (deploy_automatico.zip) do set size=%%~zA
echo Tamanho do ZIP: %size% bytes

echo [8/8] Deploy pronto!
echo.
echo ========================================
echo  SUCESSO! DEPLOY AUTOMATICO CRIADO
echo ========================================
echo.
echo 📁 Arquivo: deploy_automatico.zip
echo 📋 Guia: DEPLOY_AUTO_GUIDE.md
echo.
echo 🚀 Como fazer o deploy:
echo 1. Acesse: https://app.netlify.com/
echo 2. "Add new site" > "Deploy manually"
echo 3. Arraste o arquivo deploy_automatico.zip
echo 4. Configure o build conforme o guia
echo 5. Clique em "Deploy site"
echo.
echo ✅ O script automatico vai:
echo    - Criar requirements.txt se necessario
echo    - Configurar functions/api.py
echo    - Instalar dependencias Python
echo    - Resolver todos os problemas de build
echo.
pause 