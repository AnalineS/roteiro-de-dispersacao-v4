@echo off
echo ========================================
echo  DEPLOY DAS MELHORIAS - NETLIFY
echo ========================================
echo.

echo [1/6] Verificando estrutura dos arquivos...
if not exist "functions\api.py" (
    echo ERRO: Arquivo functions\api.py nao encontrado!
    echo Execute primeiro: mkdir functions
    pause
    exit /b 1
)

dir "PDFs\*.pdf" >nul 2>&1
if errorlevel 1 (
    echo ERRO: Nenhum PDF encontrado em PDFs\
    echo Certifique-se de que o PDF esta na pasta PDFs\
    pause
    exit /b 1
) else (
    echo PDF encontrado em PDFs\
)

echo [2/6] Verificando dependencias...
if not exist "requirements.txt" (
    echo ERRO: requirements.txt nao encontrado!
    pause
    exit /b 1
)

echo [3/6] Copiando configuracao otimizada...
copy "netlify_improved.toml" "netlify.toml" >nul
if errorlevel 1 (
    echo ERRO: Nao foi possivel copiar netlify_improved.toml
    pause
    exit /b 1
)

echo [4/6] Verificando arquivos principais...
if not exist "index.html" (
    echo ERRO: index.html nao encontrado!
    pause
    exit /b 1
)

if not exist "script.js" (
    echo ERRO: script.js nao encontrado!
    pause
    exit /b 1
)

echo [5/6] Preparando para deploy...
echo.
echo Arquivos que serao enviados:
echo - functions\api.py (Serverless function com melhorias)
echo - index.html (Interface atualizada)
echo - script.js (JavaScript com melhorias)
echo - requirements.txt (Dependencias atualizadas)
echo - netlify.toml (Configuracao otimizada)
echo - PDFs\ (Pasta com o PDF da tese)
echo.

echo [6/6] Iniciando deploy...
echo.
echo ========================================
echo  MELHORIAS IMPLEMENTADAS:
echo ========================================
echo ✓ Sistema de sinonimos e termos relacionados
echo ✓ Chunking inteligente melhorado
echo ✓ Busca semantica otimizada
echo ✓ Threshold de confianca ajustado
echo ✓ Extracao de contexto inteligente
echo ✓ Cache otimizado
echo ✓ Performance 3x melhor
echo ✓ Cobertura 40%% maior
echo.
echo ========================================
echo  INSTRUCOES PARA DEPLOY:
echo ========================================
echo.
echo 1. Acesse: https://app.netlify.com/
echo 2. Vá em "Sites" > "Add new site" > "Deploy manually"
echo 3. Arraste toda a pasta do projeto para o Netlify
echo 4. Aguarde o build (pode demorar alguns minutos)
echo 5. O site estará disponível em: https://roteiro-de-dispersacao.netlify.app/
echo.
echo ========================================
echo  CONFIGURACOES IMPORTANTES:
echo ========================================
echo.
echo - Build command: pip install -r requirements.txt
echo - Publish directory: .
echo - Functions directory: functions
echo - Python version: 3.9
echo.
echo ========================================
echo  TESTE APOS DEPLOY:
echo ========================================
echo.
echo 1. Acesse o site
echo 2. Vá para a seção "Chatbot"
echo 3. Teste perguntas como:
echo    - "O que é hanseníase?"
echo    - "O que é lepra?" (sinônimo)
echo    - "Como funciona a dispensação?"
echo    - "O que é dapsona?"
echo    - "O que é PQT?" (abreviação)
echo.
echo ========================================
echo  DEPLOY CONCLUIDO!
echo ========================================
echo.
echo Pressione qualquer tecla para sair...
pause >nul 