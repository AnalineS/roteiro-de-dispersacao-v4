@echo off
echo ========================================
echo  PUSH PARA GITHUB - NETLIFY DEPLOY
echo ========================================
echo.

echo [1/6] Verificando se o Git esta configurado...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Git nao esta instalado ou nao esta no PATH!
    echo Instale o Git em: https://git-scm.com/
    pause
    exit /b 1
)

echo [2/6] Verificando se estamos em um repositorio Git...
git status >nul 2>&1
if errorlevel 1 (
    echo ERRO: Nao estamos em um repositorio Git!
    echo Execute: git init
    pause
    exit /b 1
)

echo [3/6] Adicionando arquivos necessarios para o deploy...
git add requirements.txt
git add netlify.toml
git add functions/
git add index.html
git add script.js
git add PDFs/
git add .gitignore

echo [4/6] Verificando se ha mudancas para commitar...
git status --porcelain | findstr . >nul
if errorlevel 1 (
    echo Nenhuma mudanca detectada. Todos os arquivos ja estao no repositorio.
) else (
    echo [5/6] Fazendo commit das mudancas...
    git commit -m "Deploy das melhorias para Netlify - requirements.txt e configuracoes"
    if errorlevel 1 (
        echo ERRO: Falha ao fazer commit!
        pause
        exit /b 1
    )
)

echo [6/6] Fazendo push para o GitHub...
git push origin main
if errorlevel 1 (
    echo ERRO: Falha ao fazer push!
    echo Verifique se o repositorio remoto esta configurado corretamente.
    echo Execute: git remote -v
    pause
    exit /b 1
)

echo.
echo ========================================
echo  SUCESSO! ARQUIVOS ENVIADOS PARA GITHUB
echo ========================================
echo.
echo Agora o Netlify deve conseguir fazer o deploy automaticamente.
echo Verifique o status em: https://app.netlify.com/
echo.
pause 