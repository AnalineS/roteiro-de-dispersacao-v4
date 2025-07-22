# SOLUÇÃO RÁPIDA - CORRIGIR DEPLOY NO RENDER

## 🚨 PROBLEMA ATUAL
O Render está falhando porque o arquivo `app_production.py` no GitHub ainda contém:
```python
from fastapi import FastAPI
```

Mas deveria conter:
```python
from flask import Flask, request, jsonify, render_template_string
```

## ✅ SOLUÇÃO IMEDIATA

### Opção 1: Editar no GitHub (MAIS RÁPIDA)

1. **Acesse o GitHub:**
   - Vá para: https://github.com/AnalineS/siteroteirodedispersacao

2. **Edite o app_production.py:**
   - Clique no arquivo `app_production.py`
   - Clique no ícone de lápis (✏️) para editar
   - **SUBSTITUA A PRIMEIRA LINHA:**
     - ❌ `from fastapi import FastAPI`
     - ✅ `from flask import Flask, request, jsonify, render_template_string`

3. **Salve as mudanças:**
   - Role para baixo
   - Mensagem de commit: "Correção: Remove FastAPI"
   - Clique em "Commit changes"

4. **Deploy no Render:**
   - Vá para: https://dashboard.render.com/
   - Acesse o serviço "roteiro-dispersacao"
   - Clique em "Manual Deploy" → "Deploy latest commit"

### Opção 2: Usar arquivo ZIP

1. **Extraia o arquivo:** `deploy_render_corrigido.zip`
2. **Faça upload dos arquivos** para o GitHub
3. **Faça commit** das mudanças
4. **Deploy manual** no Render

## 🔍 VERIFICAÇÃO

Após a correção, o deploy deve funcionar e o site ficará disponível em:
**https://roteiro-dispersacao.onrender.com**

## 📋 ARQUIVOS CORRETOS

### app_production.py (primeiras linhas)
```python
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import json
import re
from transformers.pipelines import pipeline
import torch
from sentence_transformers import SentenceTransformer
import numpy as np
import hashlib
import pickle
from datetime import datetime
import logging
```

### requirements.txt
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

## ⚡ TEMPO ESTIMADO
- **Edição manual:** 2-3 minutos
- **Deploy no Render:** 5-10 minutos
- **Total:** ~15 minutos 