@echo off
echo ========================================
echo    DEPLOY PARA NETLIFY - CHATBOT HANSENIASE
echo ========================================
echo.

echo Verificando Netlify CLI...
netlify --version >nul 2>&1
if errorlevel 1 (
    echo Instalando Netlify CLI...
    npm install -g netlify-cli
    if errorlevel 1 (
        echo ERRO: Falha ao instalar Netlify CLI
        echo Instale o Node.js primeiro: https://nodejs.org/
        pause
        exit /b 1
    )
)

echo.
echo Verificando login no Netlify...
netlify status >nul 2>&1
if errorlevel 1 (
    echo Faça login no Netlify...
    netlify login
)

echo.
echo Criando estrutura de funções...
if not exist "functions" mkdir functions

echo.
echo Verificando arquivos necessários...
if not exist "app_production.py" (
    echo ERRO: app_production.py não encontrado!
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ERRO: requirements.txt não encontrado!
    pause
    exit /b 1
)

if not exist "PDFs\hanseniase.pdf" (
    echo.
    echo AVISO: PDF de hanseníase não encontrado em PDFs\hanseniase.pdf
    echo O chatbot funcionará apenas com respostas padrão
    echo.
)

echo.
echo Configurando deploy...
echo.

echo Fazendo deploy para produção...
netlify deploy --prod

if errorlevel 1 (
    echo.
    echo ERRO: Falha no deploy!
    echo Verifique os logs acima para mais detalhes.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    DEPLOY CONCLUIDO COM SUCESSO!
echo ========================================
echo.
echo Seu chatbot está disponível em:
echo https://roteiro-de-dispersacao.netlify.app
echo.
echo Para verificar o status:
echo netlify status
echo.
pause 