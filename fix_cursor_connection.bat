@echo off
chcp 65001 >nul
echo.
echo ========================================
echo  DIAGNÓSTICO DE CONEXÃO CURSOR
echo ========================================
echo.

echo 🔧 Executando diagnóstico de conexão...
echo.

python fix_connection_issues.py

echo.
echo ========================================
echo  DIAGNÓSTICO CONCLUÍDO
echo ========================================
echo.
echo 💡 Se o problema persistir:
echo    1. Reinicie o Cursor completamente
echo    2. Reinicie o computador
echo    3. Verifique sua conexão com a internet
echo.
echo 🎯 Execute o teste de conexão:
echo    python test_cursor_connection.py
echo.
pause 