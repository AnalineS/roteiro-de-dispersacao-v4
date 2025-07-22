# 🚀 Deploy no Render - AGORA!

## ✅ Status: PRONTO PARA DEPLOY IMEDIATO

**Data:** 13/07/2025  
**Arquivo:** `deploy_render.zip` (811KB) ✅ Criado  
**Plataforma:** Render (Gratuito)  

---

## 🎯 Deploy Rápido - 5 Minutos

### 1️⃣ Acesse o Render
- Vá para: [https://render.com/](https://render.com/)
- Clique em "Get Started"
- Faça login com GitHub (recomendado)

### 2️⃣ Criar Web Service
- No painel, clique em **"New +"**
- Selecione **"Web Service"**
- Escolha **"Upload files"**

### 3️⃣ Upload do Arquivo
- Arraste o arquivo **`deploy_render.zip`** para a área de upload
- Aguarde o upload completar

### 4️⃣ Configurar Build
Preencha exatamente:

```
Name: roteiro-dispersacao
Environment: Python 3
Region: Closest to users
Branch: main
Build Command: pip install -r requirements.txt
Start Command: gunicorn app_production:app
```

### 5️⃣ Configurar Variáveis de Ambiente
No painel, adicione:
```
FLASK_ENV=production
PYTHON_VERSION=3.9.0
```

### 6️⃣ Deploy
- Clique em **"Create Web Service"**
- Aguarde o build (5-10 minutos)
- **URL:** `https://roteiro-dispersacao.onrender.com`

---

## 📁 Conteúdo do ZIP

O arquivo `deploy_render.zip` contém:
- ✅ `app_production.py` - Aplicação Flask
- ✅ `requirements.txt` - Dependências Python
- ✅ `render.yaml` - Configuração do Render
- ✅ `gunicorn.conf.py` - Configuração do servidor
- ✅ `index.html` - Interface do site
- ✅ `script.js` - JavaScript do chat
- ✅ `PDFs/` - Pasta com o PDF da tese

---

## 🔍 Verificação Pós-Deploy

### 1️⃣ Teste o Site
- Acesse: `https://roteiro-dispersacao.onrender.com`
- Deve carregar a interface do chat

### 2️⃣ Teste a API
- Acesse: `https://roteiro-dispersacao.onrender.com/api/health`
- Deve retornar: `{"status": "healthy"}`

### 3️⃣ Teste o Chat
Faça perguntas como:
- "O que é hanseníase?"
- "Como tratar a lepra?"
- "Quais são os sintomas?"
- "Como é feito o diagnóstico?"

### 4️⃣ Verifique os Logs
- No painel do Render > Logs
- Deve mostrar: "Build completed successfully"

---

## 🆘 Troubleshooting Rápido

### ❌ Erro: "Build failed"
**Solução:**
- Verifique se o `requirements.txt` está correto
- Confirme se o `app_production.py` existe
- Verifique os logs de erro

### ❌ Erro: "Service not responding"
**Solução:**
- Verifique se a porta está correta (10000)
- Confirme se o health check está funcionando
- Aguarde alguns minutos (cold start)

### ❌ Erro: "Cold start"
**Solução:**
- Render "dorme" após 15 minutos
- Primeira requisição pode demorar 30-60 segundos
- Normal para o plano gratuito

---

## 📊 Limitações do Plano Gratuito

| Recurso | Limite |
|---------|--------|
| **Horas/mês** | 750 horas |
| **RAM** | 512 MB |
| **CPU** | 0.1 vCPU |
| **Storage** | 1 GB |
| **Bandwidth** | Ilimitado |

---

## 🎉 Resultado Esperado

Após o deploy bem-sucedido:

✅ **Site funcionando** em `https://roteiro-dispersacao.onrender.com`  
✅ **Chatbot com IA** otimizado  
✅ **SSL gratuito** automático  
✅ **Logs em tempo real**  
✅ **Health checks** automáticos  
✅ **Domínio personalizado** gratuito (opcional)  

---

## 🚀 Próximos Passos

1. **Faça o deploy** seguindo o passo a passo acima
2. **Teste o site** após o deploy
3. **Configure domínio personalizado** (opcional)
4. **Monitore performance** através dos logs
5. **Configure alertas** para downtime

---

## 💡 Dicas Importantes

### Para melhor performance:
- O site pode demorar 30-60 segundos na primeira requisição (cold start)
- Após o primeiro acesso, fica mais rápido
- Render "dorme" após 15 minutos de inatividade

### Para monitoramento:
- Verifique os logs regularmente
- Monitore o uso de horas (750h/mês)
- Configure alertas se necessário

---

**🎨 Render é uma excelente alternativa gratuita!**
**✅ 750 horas gratuitas por mês são suficientes!**
**🚀 Deploy em 5 minutos!** 