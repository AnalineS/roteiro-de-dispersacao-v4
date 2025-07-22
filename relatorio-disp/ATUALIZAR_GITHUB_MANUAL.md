# ATUALIZAR GITHUB MANUALMENTE - CORREÇÃO DO DEPLOY

## Problema
O Render está falhando porque o arquivo `app_production.py` no GitHub ainda contém a importação do FastAPI, mas o arquivo local já está correto.

## Solução Manual

### 1. Acesse o GitHub
- Vá para: https://github.com/AnalineS/siteroteirodedispersacao

### 2. Atualize os arquivos principais

#### app_production.py
- Clique no arquivo `app_production.py`
- Clique no ícone de lápis (editar)
- **SUBSTITUA TODO O CONTEÚDO** pelo arquivo local correto
- O arquivo deve começar com: `from flask import Flask, request, jsonify, render_template_string`
- **NÃO** deve ter: `from fastapi import FastAPI`

#### requirements.txt
- Clique no arquivo `requirements.txt`
- Clique no ícone de lápis (editar)
- **SUBSTITUA TODO O CONTEÚDO** por:
```
flask==2.3.3
flask-cors==4.0.0
transformers==4.35.0
torch==2.1.0
sentence-transformers==2.2.2
PyPDF2==3.0.1
numpy==1.24.3
requests==2.31.0
python-dotenv==1.0.0
huggingface-hub==0.19.4
scikit-learn==1.3.0
scipy==1.11.1
gunicorn==21.2.0
```

### 3. Faça o commit
- Role para baixo na página de edição
- Adicione uma mensagem de commit: "Correção: Remove FastAPI e usa Flask"
- Clique em "Commit changes"

### 4. Verifique o Render
- Vá para: https://dashboard.render.com/
- Acesse o serviço "roteiro-dispersacao"
- Clique em "Manual Deploy" → "Deploy latest commit"

### 5. Arquivo ZIP alternativo
Se preferir, use o arquivo `deploy_render_corrigido.zip` que foi criado:
- Extraia o conteúdo
- Faça upload dos arquivos para o GitHub

## Verificação
Após a atualização, o deploy no Render deve funcionar corretamente e o site ficará disponível em:
https://roteiro-dispersacao.onrender.com 