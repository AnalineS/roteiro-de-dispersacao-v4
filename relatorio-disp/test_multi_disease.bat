@echo off
echo ========================================
echo    TESTE DO CHATBOT MULTI-DOENCAS
echo ========================================
echo.

echo Verificando se o servidor esta rodando...
python test_multi_disease.py --quick
if errorlevel 1 (
    echo.
    echo ERRO: Servidor nao esta rodando!
    echo Execute start_multi_disease.bat primeiro
    pause
    exit /b 1
)

echo.
echo Executando testes completos...
python test_multi_disease.py

echo.
echo Testes concluidos!
pause 