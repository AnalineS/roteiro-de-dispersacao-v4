@echo off
echo 🔧 Testando script netlify_build_fix.sh...

echo.
echo 📋 Verificando arquivos existentes...
if exist requirements.txt (
    echo ✅ requirements.txt existe
) else (
    echo ❌ requirements.txt não existe
)

if exist functions\api.py (
    echo ✅ functions\api.py existe
) else (
    echo ❌ functions\api.py não existe
)

if exist netlify.toml (
    echo ✅ netlify.toml existe
) else (
    echo ❌ netlify.toml não existe
)

if exist index.html (
    echo ✅ index.html existe
) else (
    echo ❌ index.html não existe
)

if exist PDFs (
    echo ✅ pasta PDFs existe
) else (
    echo ❌ pasta PDFs não existe
)

echo.
echo 🚀 Executando script netlify_build_fix.sh...
bash netlify_build_fix.sh

echo.
echo 📋 Verificando arquivos após execução...
if exist requirements.txt (
    echo ✅ requirements.txt existe
) else (
    echo ❌ requirements.txt não existe
)

if exist functions\api.py (
    echo ✅ functions\api.py existe
) else (
    echo ❌ functions\api.py não existe
)

if exist netlify.toml (
    echo ✅ netlify.toml existe
) else (
    echo ❌ netlify.toml não existe
)

if exist index.html (
    echo ✅ index.html existe
) else (
    echo ❌ index.html não existe
)

if exist PDFs (
    echo ✅ pasta PDFs existe
) else (
    echo ❌ pasta PDFs não existe
)

if exist .gitignore (
    echo ✅ .gitignore existe
) else (
    echo ❌ .gitignore não existe
)

if exist runtime.txt (
    echo ✅ runtime.txt existe
) else (
    echo ❌ runtime.txt não existe
)

if exist .python-version (
    echo ✅ .python-version existe
) else (
    echo ❌ .python-version não existe
)

echo.
echo 🎉 Teste concluído!
echo.
echo 📝 Próximos passos:
echo    1. Adicione o PDF da tese na pasta PDFs/
echo    2. Faça commit e push para o GitHub
echo    3. Configure o deploy no Netlify
echo.
pause 