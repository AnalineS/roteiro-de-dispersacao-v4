@echo off
echo ========================================
echo 🔧 CONFIGURACAO GITHUB ACTIONS
echo ========================================
echo.

echo 1. Verificando se o Git esta instalado...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git nao encontrado! Instale o Git primeiro.
    echo 📥 Download: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✅ Git encontrado

echo.
echo 2. Verificando se este e um repositorio Git...
if not exist ".git" (
    echo 📁 Inicializando repositorio Git...
    git init
    echo ✅ Repositorio inicializado
) else (
    echo ✅ Repositorio Git encontrado
)

echo.
echo 3. Verificando arquivos de workflow...
if not exist ".github\workflows" (
    echo 📁 Criando diretorio de workflows...
    mkdir ".github\workflows"
    echo ✅ Diretorio criado
)

echo.
echo 4. Verificando se o workflow ja existe...
if exist ".github\workflows\deploy-render.yml" (
    echo ⚠️  Workflow ja existe. Atualizando...
) else (
    echo 📝 Criando workflow de deploy...
)

echo.
echo 5. Configurando Git...
git config --global user.name "Deploy Bot"
git config --global user.email "deploy@example.com"

echo.
echo 6. Adicionando arquivos ao Git...
git add .
git commit -m "Configuracao de deploy automatico para Render"

echo.
echo 7. Verificando remote...
git remote -v | findstr "origin" >nul
if errorlevel 1 (
    echo 📋 Para conectar ao GitHub:
    echo 1. Crie um repositorio em: https://github.com/new
    echo 2. Execute: git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
    echo 3. Execute: git push -u origin main
) else (
    echo ✅ Remote configurado
    echo 📤 Fazendo push para GitHub...
    git push origin main
)

echo.
echo ========================================
echo ✅ CONFIGURACAO CONCLUIDA!
echo ========================================
echo.
echo 📋 PROXIMOS PASSOS:
echo 1. Conecte seu repositorio ao Render:
echo    - Acesse: https://dashboard.render.com
echo    - Clique em "New +" > "Web Service"
echo    - Conecte sua conta GitHub
echo    - Selecione este repositorio
echo.
echo 2. Configure o servico:
echo    - Name: roteiro-dispersacao
echo    - Environment: Python
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: gunicorn app_optimized:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
echo.
echo 3. Deploy automatico:
echo    - Cada push para main = novo deploy
echo    - Acesse: https://roteiro-dispersacao.onrender.com
echo.
pause 