@echo off
echo ========================================
echo  PREPARAR DEPLOY RENDER - MANUAL
echo ========================================
echo.

echo [1/6] Verificando arquivos essenciais...
if not exist "app_production.py" (
    echo ERRO: app_production.py nao encontrado!
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ERRO: requirements.txt nao encontrado!
    pause
    exit /b 1
)

if not exist "render.yaml" (
    echo ERRO: render.yaml nao encontrado!
    pause
    exit /b 1
)

echo [2/6] Criando pasta para deploy...
if exist "deploy_render" (
    rmdir /s /q "deploy_render"
)
mkdir "deploy_render"

echo [3/6] Copiando arquivos essenciais...
copy "app_production.py" "deploy_render\"
copy "requirements.txt" "deploy_render\"
copy "render.yaml" "deploy_render\"
copy "gunicorn.conf.py" "deploy_render\"
copy "index.html" "deploy_render\"
copy "script.js" "deploy_render\"

echo [4/6] Copiando pasta PDFs...
if exist "PDFs" (
    xcopy "PDFs" "deploy_render\PDFs\" /E /I /Y
    echo ✅ Pasta PDFs copiada
) else (
    echo ⚠️ Pasta PDFs nao encontrada
)

echo [5/6] Criando arquivo ZIP...
powershell "Compress-Archive -Path 'deploy_render\*' -DestinationPath 'deploy_render.zip' -Force" >nul 2>&1
if errorlevel 1 (
    echo ERRO: Falha ao criar ZIP
    pause
    exit /b 1
)

echo [6/6] Verificando arquivo ZIP...
if exist "deploy_render.zip" (
    for %%A in (deploy_render.zip) do set size=%%~zA
    echo ✅ ZIP criado: deploy_render.zip (%size% bytes)
) else (
    echo ERRO: ZIP nao foi criado!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  SUCESSO! ARQUIVO ZIP PRONTO
echo ========================================
echo.
echo 📁 Arquivo: deploy_render.zip
echo 📋 Conteudo:
echo    - app_production.py
echo    - requirements.txt
echo    - render.yaml
echo    - gunicorn.conf.py
echo    - index.html
echo    - script.js
echo    - PDFs/ (pasta)
echo.
echo 🚀 Como fazer o deploy:
echo    1. Acesse: https://render.com/
echo    2. Login com GitHub
echo    3. "New +" > "Web Service"
echo    4. Escolha "Upload files"
echo    5. Faça upload do deploy_render.zip
echo    6. Configure:
echo       - Name: roteiro-dispersacao
echo       - Environment: Python 3
echo       - Build Command: pip install -r requirements.txt
echo       - Start Command: gunicorn app_production:app
echo    7. Clique em "Create Web Service"
echo.
echo 📖 Guia completo: DEPLOY_RENDER_PASSO_A_PASSO.md
echo.
pause 