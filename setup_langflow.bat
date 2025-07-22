@echo off
echo ========================================
echo    INSTALACAO E CONFIGURACAO LANGFLOW
echo ========================================
echo.

echo [1/5] Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.9+ primeiro
    pause
    exit /b 1
)

echo.
echo [2/5] Instalando Langflow...
pip install langflow
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar Langflow
    pause
    exit /b 1
)

echo.
echo [3/5] Instalando dependencias adicionais...
pip install requests typing-extensions
if %errorlevel% neq 0 (
    echo AVISO: Algumas dependencias podem nao ter sido instaladas
)

echo.
echo [4/5] Criando arquivo de configuracao...
echo LANGFLOW_API_KEY= > .env
echo LANGFLOW_URL=http://localhost:7860 >> .env

echo.
echo [5/5] Testando integracao...
python langflow_integration.py

echo.
echo ========================================
echo    CONFIGURACAO CONCLUIDA!
echo ========================================
echo.
echo Para iniciar o Langflow:
echo 1. Execute: langflow run
echo 2. Acesse: http://localhost:7860
echo 3. Configure seu fluxo visual
echo.
echo Para integrar com o chatbot:
echo 1. Execute: python app_optimized.py
echo 2. O sistema detectara automaticamente o Langflow
echo.
pause 