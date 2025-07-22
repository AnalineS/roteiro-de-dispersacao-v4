#!/bin/bash

echo "========================================"
echo "  PUSH PARA GITHUB - NETLIFY DEPLOY"
echo "========================================"
echo

echo "[1/6] Verificando se o Git está configurado..."
if ! command -v git &> /dev/null; then
    echo "ERRO: Git não está instalado!"
    echo "Instale o Git: sudo apt-get install git (Ubuntu/Debian)"
    echo "ou: brew install git (macOS)"
    exit 1
fi

echo "[2/6] Verificando se estamos em um repositório Git..."
if ! git status &> /dev/null; then
    echo "ERRO: Não estamos em um repositório Git!"
    echo "Execute: git init"
    exit 1
fi

echo "[3/6] Adicionando arquivos necessários para o deploy..."
git add requirements.txt
git add netlify.toml
git add functions/
git add index.html
git add script.js
git add PDFs/
git add .gitignore

echo "[4/6] Verificando se há mudanças para commitar..."
if [ -z "$(git status --porcelain)" ]; then
    echo "Nenhuma mudança detectada. Todos os arquivos já estão no repositório."
else
    echo "[5/6] Fazendo commit das mudanças..."
    git commit -m "Deploy das melhorias para Netlify - requirements.txt e configurações"
    if [ $? -ne 0 ]; then
        echo "ERRO: Falha ao fazer commit!"
        exit 1
    fi
fi

echo "[6/6] Fazendo push para o GitHub..."
git push origin main
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao fazer push!"
    echo "Verifique se o repositório remoto está configurado corretamente."
    echo "Execute: git remote -v"
    exit 1
fi

echo
echo "========================================"
echo "  SUCESSO! ARQUIVOS ENVIADOS PARA GITHUB"
echo "========================================"
echo
echo "Agora o Netlify deve conseguir fazer o deploy automaticamente."
echo "Verifique o status em: https://app.netlify.com/"
echo 