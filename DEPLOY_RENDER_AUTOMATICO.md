# 🚀 DEPLOY AUTOMATICO - RENDER

## ✅ Arquivo ZIP Criado: `deploy_render.zip`

### 📋 Pré-requisitos
- Conta no Render (gratuita): https://dashboard.render.com
- Arquivo `deploy_render.zip` gerado pelo script

### 🔧 Passo a Passo Completo

#### 1. Acesse o Render
- Vá para: https://dashboard.render.com
- Faça login ou crie uma conta gratuita

#### 2. Criar Novo Web Service
- Clique em **"New +"** no canto superior direito
- Selecione **"Web Service"**

#### 3. Configurar Deploy
**Opção A - Upload Manual (Recomendado):**
- Clique em **"Deploy from existing code"**
- Selecione **"Upload files"**
- Arraste o arquivo `deploy_render.zip`

**Opção B - GitHub (Se tiver repositório):**
- Conecte sua conta GitHub
- Selecione o repositório
- Configure a branch (main/master)

#### 4. Configurações do Serviço
```
Name: roteiro-dispersacao
Environment: Python 3
Region: Oregon (US West) - Free
Branch: main (se GitHub)
Root Directory: . (deixe vazio)
```

#### 5. Build & Deploy Settings
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn app_optimized:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

#### 6. Environment Variables (Opcional)
Se precisar de variáveis de ambiente:
```
OPENROUTER_API_KEY=sua_chave_aqui
```

#### 7. Deploy
- Clique em **"Create Web Service"**
- Aguarde o build (pode demorar 5-10 minutos)

### 🔍 Monitoramento

#### Logs de Build
- Durante o build, acompanhe os logs
- Se houver erro, verifique:
  - Versão do Python (3.11.0)
  - Dependências no requirements.txt
  - Arquivo app_optimized.py presente

#### Health Check
- O serviço tem health check em `/api/health`
- Render vai verificar automaticamente

### 🚨 Solução de Problemas

#### Erro: "No matching distribution found for transformerstorch"
**Solução:**
1. Verifique se o `requirements.txt` está correto
2. Limpe o cache do Render:
   - Vá em Settings > Build & Deploy
   - Clique em "Clear build cache"
   - Faça novo deploy

#### Erro: "Module not found"
**Solução:**
1. Verifique se todas as dependências estão no `requirements.txt`
2. Certifique-se que o arquivo `app_optimized.py` está no ZIP

#### Erro: "Port already in use"
**Solução:**
- O Render usa a variável `$PORT` automaticamente
- Não precisa configurar porta manualmente

### 📊 Recursos Gratuitos do Render

- **750 horas/mês** de runtime
- **512 MB RAM** por serviço
- **1 CPU** compartilhado
- **Auto-sleep** após 15 minutos de inatividade
- **Custom domains** gratuitos

### 🔄 Deploy Automático

Após configurar:
- Cada push para GitHub = novo deploy automático
- Ou faça upload manual do ZIP atualizado

### 📱 URLs do Serviço

Após o deploy, você terá:
- **URL Principal**: `https://roteiro-dispersacao.onrender.com`
- **Health Check**: `https://roteiro-dispersacao.onrender.com/api/health`

### ✅ Checklist Final

- [ ] Arquivo `deploy_render.zip` criado
- [ ] Conta Render criada
- [ ] Web Service configurado
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `gunicorn app_optimized:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`
- [ ] Deploy realizado com sucesso
- [ ] Health check passando
- [ ] Chatbot funcionando

### 🎉 Sucesso!

Seu chatbot estará disponível em:
`https://roteiro-dispersacao.onrender.com`

O serviço vai:
- ✅ Iniciar automaticamente
- ✅ Responder a perguntas sobre hanseníase
- ✅ Usar modelos AI via OpenRouter
- ✅ Manter histórico de conversas
- ✅ Funcionar 24/7 (com auto-sleep) 