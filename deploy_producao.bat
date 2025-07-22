@echo off
echo 🚀 DEPLOY PARA PRODUÇÃO - NOVA VERSÃO
echo ======================================

echo.
echo 📋 Verificando arquivos essenciais...

if exist requirements.txt (
    echo ✅ requirements.txt
) else (
    echo ❌ requirements.txt não encontrado
    goto :error
)

if exist netlify.toml (
    echo ✅ netlify.toml
) else (
    echo ❌ netlify.toml não encontrado
    goto :error
)

if exist functions\api.py (
    echo ✅ functions\api.py
) else (
    echo ❌ functions\api.py não encontrado
    goto :error
)

if exist index.html (
    echo ✅ index.html
) else (
    echo ❌ index.html não encontrado
    goto :error
)

if exist "PDFs\Roteiro de Dsispensação - Hanseníase F.docx.pdf" (
    echo ✅ PDF da tese encontrado
) else (
    echo ❌ PDF da tese não encontrado
    goto :error
)

echo.
echo 🔧 Configurando arquivos para produção...

REM Criar arquivo de configuração de produção
echo [build] > netlify_production.toml
echo   publish = "." >> netlify_production.toml
echo   command = "bash netlify_build_fix.sh" >> netlify_production.toml
echo   functions = "functions" >> netlify_production.toml
echo. >> netlify_production.toml
echo [[redirects]] >> netlify_production.toml
echo   from = "/api/*" >> netlify_production.toml
echo   to = "/.netlify/functions/api/:splat" >> netlify_production.toml
echo   status = 200 >> netlify_production.toml
echo   force = true >> netlify_production.toml
echo. >> netlify_production.toml
echo [[redirects]] >> netlify_production.toml
echo   from = "/*" >> netlify_production.toml
echo   to = "/index.html" >> netlify_production.toml
echo   status = 200 >> netlify_production.toml
echo. >> netlify_production.toml
echo [build.environment] >> netlify_production.toml
echo   PYTHON_VERSION = "3.9" >> netlify_production.toml
echo   NODE_VERSION = "18" >> netlify_production.toml
echo   ENABLE_SYNONYMS = "true" >> netlify_production.toml
echo   ENABLE_CONTEXT_EXTRACTION = "true" >> netlify_production.toml
echo   CONFIDENCE_THRESHOLD = "0.3" >> netlify_production.toml
echo   MAX_CHUNKS = "3" >> netlify_production.toml
echo   CHUNK_SIZE = "1500" >> netlify_production.toml
echo   CHUNK_OVERLAP = "300" >> netlify_production.toml
echo. >> netlify_production.toml
echo [functions] >> netlify_production.toml
echo   directory = "functions" >> netlify_production.toml
echo   node_bundler = "esbuild" >> netlify_production.toml
echo   included_files = ["PDFs/**/*"] >> netlify_production.toml
echo   external_node_modules = ["@netlify/functions"] >> netlify_production.toml
echo. >> netlify_production.toml
echo [[headers]] >> netlify_production.toml
echo   for = "/api/*" >> netlify_production.toml
echo   [headers.values] >> netlify_production.toml
echo     Access-Control-Allow-Origin = "*" >> netlify_production.toml
echo     Access-Control-Allow-Headers = "Content-Type" >> netlify_production.toml
echo     Access-Control-Allow-Methods = "POST, OPTIONS" >> netlify_production.toml

echo ✅ netlify_production.toml criado

echo.
echo 📦 Criando arquivo ZIP para deploy...

REM Criar ZIP com todos os arquivos necessários
powershell -Command "Compress-Archive -Path 'requirements.txt', 'netlify_production.toml', 'netlify_build_fix.sh', 'functions', 'index.html', 'PDFs', '.gitignore', 'runtime.txt', '.python-version' -DestinationPath 'deploy_producao.zip' -Force"
REM Garantir que o arquivo functions/api.py está incluído e destacado como principal backend
powershell -Command "Compress-Archive -Path 'functions/api.py' -DestinationPath 'deploy_producao.zip' -Force"

if exist deploy_producao.zip (
    echo ✅ deploy_producao.zip criado com sucesso!
    echo 📊 Tamanho do arquivo: 
    powershell -Command "Get-ChildItem 'deploy_producao.zip' | Select-Object Name, @{Name='Size(MB)';Expression={[math]::Round($_.Length/1MB,2)}}"
) else (
    echo ❌ Erro ao criar ZIP
    goto :error
)

echo.
echo 🎯 OPÇÕES DE DEPLOY:
echo.
echo 1️⃣ DEPLOY AUTOMÁTICO (Recomendado):
echo    - Vá para https://netlify.com
echo    - Faça login ou crie conta
echo    - Clique em "Add new site" → "Deploy manually"
echo    - Arraste o arquivo deploy_producao.zip
echo    - Configure:
echo      • Build command: bash netlify_build_fix.sh
echo      • Publish directory: .
echo      • Functions directory: functions
echo.
echo 2️⃣ DEPLOY VIA GITHUB:
echo    - Se você tem Git instalado, execute:
echo      git add .
echo      git commit -m "Nova versão para produção"
echo      git push origin main
echo    - Conecte seu repositório no Netlify
echo.
echo 3️⃣ DEPLOY MANUAL:
echo    - Use o arquivo deploy_producao.zip
echo    - Faça upload no Netlify
echo.
echo 📝 ARQUIVOS INCLUÍDOS NO DEPLOY:
echo    ✅ requirements.txt (dependências Python)
echo    ✅ netlify_production.toml (configuração otimizada)
echo    ✅ netlify_build_fix.sh (script de build)
echo    ✅ functions/api.py (API do chatbot)
echo    ✅ index.html (interface do usuário)
echo    ✅ PDFs/ (arquivo da tese)
echo    ✅ .gitignore (arquivos ignorados)
echo    ✅ runtime.txt (versão Python)
echo    ✅ .python-version (compatibilidade)
echo.
echo 🚀 PRONTO PARA DEPLOY!
echo O arquivo deploy_producao.zip está pronto para upload no Netlify.
echo.
pause
goto :end

:error
echo.
echo ❌ ERRO: Verifique se todos os arquivos estão presentes
echo.
pause
exit /b 1

:end
echo.
echo ✅ Script de deploy concluído com sucesso! 