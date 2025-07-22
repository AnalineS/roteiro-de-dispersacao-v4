@echo off
echo ========================================
echo  MIGRACAO DE HOSPEDAGEM - ALTERNATIVAS
echo ========================================
echo.

echo [1/6] Verificando estrutura do projeto...
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

echo [2/6] Criando arquivos de configuracao...

echo Criando railway.json...
echo {> railway.json
echo   "build": {>> railway.json
echo     "builder": "NIXPACKS">> railway.json
echo   },>> railway.json
echo   "deploy": {>> railway.json
echo     "startCommand": "python app_production.py",>> railway.json
echo     "healthcheckPath": "/api/health",>> railway.json
echo     "healthcheckTimeout": 300,>> railway.json
echo     "restartPolicyType": "ON_FAILURE">> railway.json
echo   }>> railway.json
echo }>> railway.json

echo Criando render.yaml...
echo services:> render.yaml
echo   - type: web>> render.yaml
echo     name: roteiro-dispersacao>> render.yaml
echo     env: python>> render.yaml
echo     buildCommand: pip install -r requirements.txt>> render.yaml
echo     startCommand: gunicorn app_production:app>> render.yaml
echo     envVars:>> render.yaml
echo       - key: PYTHON_VERSION>> render.yaml
echo         value: 3.9.0>> render.yaml
echo       - key: FLASK_ENV>> render.yaml
echo         value: production>> render.yaml

echo Criando gunicorn.conf.py...
echo bind = "0.0.0.0:10000"> gunicorn.conf.py
echo workers = 2>> gunicorn.conf.py
echo timeout = 120>> gunicorn.conf.py
echo max_requests = 1000>> gunicorn.conf.py
echo max_requests_jitter = 100>> gunicorn.conf.py

echo [3/6] Verificando se gunicorn esta no requirements.txt...
findstr "gunicorn" requirements.txt >nul
if errorlevel 1 (
    echo Adicionando gunicorn ao requirements.txt...
    echo gunicorn==21.2.0>> requirements.txt
) else (
    echo gunicorn ja esta no requirements.txt
)

echo [4/6] Criando guias de deploy...
echo # 🚀 Guias de Deploy Criados > GUIA_DEPLOY_RAPIDO.md
echo. >> GUIA_DEPLOY_RAPIDO.md
echo ## 🚂 Railway (Recomendado) >> GUIA_DEPLOY_RAPIDO.md
echo 1. Acesse: https://railway.app/ >> GUIA_DEPLOY_RAPIDO.md
echo 2. Login com GitHub >> GUIA_DEPLOY_RAPIDO.md
echo 3. "New Project" > "Deploy from GitHub repo" >> GUIA_DEPLOY_RAPIDO.md
echo 4. Selecione seu repositorio >> GUIA_DEPLOY_RAPIDO.md
echo 5. Deploy automatico! >> GUIA_DEPLOY_RAPIDO.md
echo. >> GUIA_DEPLOY_RAPIDO.md
echo ## 🎨 Render (Gratuito) >> GUIA_DEPLOY_RAPIDO.md
echo 1. Acesse: https://render.com/ >> GUIA_DEPLOY_RAPIDO.md
echo 2. Login com GitHub >> GUIA_DEPLOY_RAPIDO.md
echo 3. "New +" > "Web Service" >> GUIA_DEPLOY_RAPIDO.md
echo 4. Conecte seu repositorio >> GUIA_DEPLOY_RAPIDO.md
echo 5. Deploy automatico! >> GUIA_DEPLOY_RAPIDO.md

echo [5/6] Verificando arquivos criados...
if exist "railway.json" echo ✅ railway.json criado
if exist "render.yaml" echo ✅ render.yaml criado
if exist "gunicorn.conf.py" echo ✅ gunicorn.conf.py criado
if exist "GUIA_DEPLOY_RAPIDO.md" echo ✅ GUIA_DEPLOY_RAPIDO.md criado

echo [6/6] Migracao concluida!
echo.
echo ========================================
echo  SUCESSO! PROJETO PRONTO PARA MIGRACAO
echo ========================================
echo.
echo 📁 Arquivos criados:
echo    - railway.json (para Railway)
echo    - render.yaml (para Render)
echo    - gunicorn.conf.py (para Render)
echo    - GUIA_DEPLOY_RAPIDO.md (guia rapido)
echo.
echo 🚀 Proximos passos:
echo    1. Escolha uma plataforma (Railway ou Render)
echo    2. Siga o guia correspondente
echo    3. Deploy automatico!
echo.
echo 📋 Guias completos:
echo    - DEPLOY_RAILWAY.md
echo    - DEPLOY_RENDER.md
echo    - COMPARACAO_HOSPEDAGEM.md
echo.
echo 🏆 Recomendacao: Railway (mais facil) ou Render (gratuito)
echo.
pause 