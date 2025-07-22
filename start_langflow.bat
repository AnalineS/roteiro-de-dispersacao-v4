@echo off
echo ========================================
echo    INICIANDO LANGFLOW
echo ========================================
echo.

echo Verificando Langflow instalado...

if exist "C:\Program Files\Langflow\langflow.exe" (
    echo ✅ Langflow encontrado em C:\Program Files\Langflow
    echo.
    echo Iniciando Langflow...
    echo.
    "C:\Program Files\Langflow\langflow.exe" run
) else (
    echo ❌ Langflow nao encontrado em C:\Program Files\Langflow
    echo.
    echo Tentando via pip...
    langflow run
)

echo.
echo Se o Langflow iniciou com sucesso:
echo 1. Acesse: http://localhost:7860
echo 2. Configure seus fluxos
echo 3. Em outro terminal, execute: python app_with_langflow.py
echo.
pause 