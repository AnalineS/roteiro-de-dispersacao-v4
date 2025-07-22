@echo off
echo ========================================
echo  INSTALADOR CHATBOT TESE HANSENIASE
echo ========================================
echo.

echo 1. Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python nao encontrado. Instalando...
    echo Por favor, baixe e instale Python de: https://www.python.org/downloads/
    echo Certifique-se de marcar "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

echo Python encontrado!
echo.

echo 2. Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Erro ao instalar dependencias.
    pause
    exit /b 1
)

echo Dependencias instaladas!
echo.

echo 3. Verificando PDF...
if not exist "Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf" (
    echo PDF nao encontrado!
    echo Por favor, baixe o PDF do link fornecido e coloque na pasta do projeto.
    echo Nome do arquivo: Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf
    pause
    exit /b 1
)

echo PDF encontrado!
echo.

echo 4. Configuracao otimizada carregada.
echo.

echo ========================================
echo  INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Para iniciar o chatbot:
echo   python app_optimized.py
echo.
echo Ou execute: start.bat
echo.
echo Acesse: http://localhost:5000
echo.
pause 