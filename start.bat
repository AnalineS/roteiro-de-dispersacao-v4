@echo off
echo ========================================
echo  INICIANDO CHATBOT TESE HANSENIASE
echo ========================================
echo.

echo Verificando dependencias...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python nao encontrado!
    echo Execute setup.bat primeiro.
    pause
    exit /b 1
)

echo Verificando PDF...
if not exist "Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf" (
    echo PDF nao encontrado!
    echo Coloque o arquivo PDF na pasta do projeto.
    pause
    exit /b 1
)

echo Iniciando servidor...
echo.
echo Acesse: http://localhost:5000
echo Pressione Ctrl+C para parar
echo.

python app_optimized.py

pause 