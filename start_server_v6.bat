@echo off
echo ========================================
echo    Iniciando Chatbot v6 - Cursor
echo ========================================
echo.

echo Verificando se o Python esta instalado...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale o Python e tente novamente.
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
pip install -r requirements_v6.txt

echo.
echo Iniciando o servidor...
echo URL: http://localhost:5000
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

python app_v6_cursor.py

pause 