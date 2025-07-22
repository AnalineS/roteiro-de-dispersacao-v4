# 🎨 Deploy no Render - Passo a Passo

## ✅ Status: PRONTO PARA DEPLOY

**Data:** 13/07/2025  
**Plataforma:** Render (Gratuito)  
**Arquivos:** ✅ Configurados  

---

## 🚀 Opção 1: Deploy via GitHub (Recomendado)

### 1️⃣ Instalar Git (se necessário)
- Baixe: [https://git-scm.com/download/win](https://git-scm.com/download/win)
- Instale e reinicie o terminal

### 2️⃣ Configurar Git
```bash
git init
git add .
git commit -m "Primeiro commit - Roteiro de Dispersação"
```

### 3️⃣ Criar Repositório no GitHub
- Acesse: [https://github.com/](https://github.com/)
- Clique em "New repository"
- Nome: `roteiro-dispersacao`
- Público ou privado
- **NÃO** inicialize com README

### 4️⃣ Conectar ao GitHub
```bash
git remote add origin https://github.com/SEU_USUARIO/roteiro-dispersacao.git
git branch -M main
git push -u origin main
```

### 5️⃣ Deploy no Render
- Acesse: [https://render.com/](https://render.com/)
- Faça login com GitHub
- Clique em "New +" > "Web Service"
- Conecte o repositório `roteiro-dispersacao`
- Configure:
  - **Name:** `roteiro-dispersacao`
  - **Environment:** `Python 3`
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `gunicorn app_production:app`
- Clique em "Create Web Service"

---

## 📁 Opção 2: Deploy Manual (Alternativa)

### 1️⃣ Preparar Arquivos
Crie um arquivo ZIP com:
- `app_production.py`
- `requirements.txt`
- `render.yaml`
- `gunicorn.conf.py`
- `index.html`
- `script.js`
- Pasta `PDFs/`

### 2️⃣ Deploy Manual
- Acesse: [https://render.com/](https://render.com/)
- Faça login
- Clique em "New +" > "Web Service"
- Escolha "Upload files"
- Faça upload do ZIP
- Configure manualmente:
  - **Name:** `roteiro-dispersacao`
  - **Environment:** `Python 3`
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `gunicorn app_production:app`

---

## 🔧 Configuração Automática

### Arquivos já criados:
✅ `render.yaml` - Configuração do Render  
✅ `gunicorn.conf.py` - Configuração do servidor  
✅ `requirements.txt` - Dependências atualizadas  

### Configuração do Render:
```yaml
services:
  - type: web
    name: roteiro-dispersacao
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app_production:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: FLASK_ENV
        value: production
```

---

## 🎯 Passo a Passo Detalhado

### 1️⃣ Criar Conta no Render
- Acesse: [https://render.com/](https://render.com/)
- Clique em "Get Started"
- Faça login com GitHub (recomendado)

### 2️⃣ Criar Web Service
- No painel, clique em "New +"
- Selecione "Web Service"
- Escolha seu repositório GitHub

### 3️⃣ Configurar Build
- **Name:** `roteiro-dispersacao`
- **Environment:** `Python 3`
- **Region:** Closest to users
- **Branch:** `main`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app_production:app`

### 4️⃣ Configurar Variáveis de Ambiente
No painel do Render, adicione:
```
FLASK_ENV=production
PYTHON_VERSION=3.9.0
```

### 5️⃣ Deploy
- Clique em "Create Web Service"
- Aguarde o build (5-10 minutos)
- O site ficará disponível em: `https://roteiro-dispersacao.onrender.com`

---

## 🔍 Verificação Pós-Deploy

### 1️⃣ Teste o Site
- Acesse: `https://roteiro-dispersacao.onrender.com`
- Verifique se carrega corretamente

### 2️⃣ Teste a API
- Acesse: `https://roteiro-dispersacao.onrender.com/api/health`
- Deve retornar: `{"status": "healthy"}`

### 3️⃣ Teste o Chat
- Faça perguntas como:
  - "O que é hanseníase?"
  - "Como tratar a lepra?"
  - "Quais são os sintomas?"

### 4️⃣ Verifique os Logs
- No painel do Render > Logs
- Deve mostrar build bem-sucedido

---

## 🆘 Troubleshooting

### ❌ Erro: "Build failed"
**Solução:**
- Verifique se `requirements.txt` está correto
- Confirme se `app_production.py` existe
- Verifique os logs de erro

### ❌ Erro: "Service not responding"
**Solução:**
- Verifique se a porta está correta (10000)
- Confirme se o health check está funcionando
- Verifique os logs do serviço

### ❌ Erro: "Cold start"
**Solução:**
- Render "dorme" após 15 minutos
- Primeira requisição pode demorar 30-60 segundos
- Normal para o plano gratuito

### ❌ Erro: "Memory limit exceeded"
**Solução:**
- Render tem limite de 512MB
- Otimize o modelo de IA
- Reduza workers no Gunicorn

---

## 📊 Limitações do Plano Gratuito

| Recurso | Limite |
|---------|--------|
| **Horas/mês** | 750 horas |
| **RAM** | 512 MB |
| **CPU** | 0.1 vCPU |
| **Storage** | 1 GB |
| **Bandwidth** | Ilimitado |
| **Domínios** | Ilimitado |

---

## 🎉 Resultado Esperado

Após o deploy bem-sucedido:

✅ **URL:** `https://roteiro-dispersacao.onrender.com`  
✅ **Deploy automático** a cada push no GitHub  
✅ **SSL gratuito** automático  
✅ **Logs em tempo real**  
✅ **Health checks** automáticos  
✅ **Domínio personalizado** gratuito  

---

## 🚀 Próximos Passos

1. **Escolha a opção** (GitHub ou Manual)
2. **Siga o passo a passo** correspondente
3. **Configure o deploy** no Render
4. **Teste o site** após o deploy
5. **Configure domínio personalizado** (opcional)
6. **Monitore performance** através dos logs

---

**🎨 Render é uma excelente alternativa gratuita!**
**✅ 750 horas gratuitas por mês são suficientes!** 