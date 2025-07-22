@echo off
echo ========================================
echo ABRINDO RENDER PARA DEPLOY
echo ========================================

echo.
echo Abrindo dashboard do Render...
start https://dashboard.render.com

echo.
echo Aguarde 3 segundos e abrindo pasta com o ZIP...
timeout /t 3 /nobreak >nul
start .

echo.
echo ========================================
echo INSTRUCOES RAPIDAS:
echo ========================================
echo 1. No Render: "New +" > "Web Service"
echo 2. "Deploy from existing code" > "Upload files"
echo 3. Arraste o arquivo deploy_render.zip
echo 4. Configure:
echo    - Name: roteiro-dispersacao
echo    - Build: pip install -r requirements.txt
echo    - Start: gunicorn app_optimized:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
echo 5. "Create Web Service"
echo.
echo O arquivo deploy_render.zip esta pronto!
echo.
pause 