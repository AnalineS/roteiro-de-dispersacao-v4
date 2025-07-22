@echo off
echo ========================================
echo    INSTALADOR CHATBOT MULTI-DOENCAS
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.8+ primeiro
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado! Instalando dependencias...
echo.

echo Instalando bibliotecas necessarias...
pip install flask flask-cors transformers torch sentence-transformers PyPDF2 numpy

echo.
echo Criando estrutura de pastas...
if not exist "PDFs" mkdir PDFs

echo.
echo ========================================
echo    CONFIGURACAO COMPLETA!
echo ========================================
echo.
echo Para adicionar novos PDFs de doencas:
echo 1. Coloque o PDF na pasta 'PDFs'
echo 2. Edite o arquivo 'app_multi_disease.py'
echo 3. Adicione a nova doenca na secao 'diseases'
echo.
echo Para iniciar o chatbot:
echo    start_multi_disease.bat
echo.
pause 