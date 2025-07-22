@echo off
echo ========================================
echo    CORREÇÃO DE CONFIGURACAO LANGFLOW
echo ========================================
echo.

echo [1/6] Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)

echo.
echo [2/6] Corrigindo versao do NumPy...
pip uninstall numpy -y
pip install "numpy<2.0.0"
if %errorlevel% neq 0 (
    echo AVISO: Problema ao corrigir NumPy
)

echo.
echo [3/6] Verificando Langflow instalado...
if exist "C:\Program Files\Langflow" (
    echo ✅ Langflow encontrado em C:\Program Files\Langflow
    echo.
    echo [4/6] Configurando variaveis de ambiente...
    setx LANGFLOW_PATH "C:\Program Files\Langflow"
    echo ✅ Variavel LANGFLOW_PATH configurada
) else (
    echo ❌ Langflow nao encontrado em C:\Program Files\Langflow
    echo 💡 Instalando Langflow via pip...
    pip install langflow
)

echo.
echo [5/6] Instalando dependencias Python...
pip install requests typing-extensions
if %errorlevel% neq 0 (
    echo AVISO: Algumas dependencias podem nao ter sido instaladas
)

echo.
echo [6/6] Criando arquivo de configuracao...
echo LANGFLOW_PATH=C:\Program Files\Langflow > .env
echo LANGFLOW_URL=http://localhost:7860 >> .env
echo LANGFLOW_API_KEY=sk-oZkcvhmKOMt0eRUizMCvOPLvgvNT1uEKrtm-Al4oXB4 >> .env

echo.
echo ========================================
echo    CONFIGURACAO CONCLUIDA!
echo ========================================
echo.
echo Para iniciar o Langflow:
echo 1. Abra um novo terminal
echo 2. Execute: langflow run
echo 3. Acesse: http://localhost:7860
echo.
echo Para testar a integracao:
echo 1. Execute: python test_langflow_integration.py
echo 2. Execute: python app_with_langflow.py
echo.
pause 