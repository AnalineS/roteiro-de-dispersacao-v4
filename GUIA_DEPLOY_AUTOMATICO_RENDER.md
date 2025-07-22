# 🚀 GUIA COMPLETO - DEPLOY AUTOMÁTICO NO RENDER

## 📋 Visão Geral

Este guia mostra como configurar o deploy automático do seu chatbot de hanseníase no Render, para o endereço: **https://roteiro-dispersacao.onrender.com**

## 🎯 Opções de Deploy

### Opção 1: Deploy Automático via GitHub Actions (Recomendado)
- ✅ Deploy automático a cada push
- ✅ Integração contínua
- ✅ Histórico de versões
- ✅ Rollback fácil

### Opção 2: Deploy Manual via ZIP
- ✅ Simples e direto
- ✅ Não precisa de GitHub
- ✅ Controle total

### Opção 3: Deploy via Render CLI
- ✅ Automatizado via linha de comando
- ✅ Scripts personalizados
- ✅ Integração com CI/CD

## 🔧 Opção 1: Deploy Automático via GitHub Actions

### Passo 1: Configurar GitHub
```bash
# Execute o script de configuração
setup_github_deploy.bat
```

### Passo 2: Criar Repositório no GitHub
1. Acesse: https://github.com/new
2. Nome: `roteiro-dispersacao`
3. Público ou Privado
4. Não inicialize com README

### Passo 3: Conectar Repositório
```bash
git remote add origin https://github.com/SEU_USUARIO/roteiro-dispersacao.git
git push -u origin main
```

### Passo 4: Configurar Render
1. Acesse: https://dashboard.render.com
2. Clique em **"New +"** → **"Web Service"**
3. Conecte sua conta GitHub
4. Selecione o repositório `roteiro-dispersacao`
5. Configure:
   - **Name**: `roteiro-dispersacao`
   - **Environment**: `Python 3`
   - **Region**: `Oregon (US West) - Free`
   - **Branch**: `main`
   - **Root Directory**: `.` (deixe vazio)

### Passo 5: Build & Deploy Settings
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn app_optimized:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

### Passo 6: Environment Variables (Opcional)
```
OPENROUTER_API_KEY_LLAMA=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
OPENROUTER_API_KEY_QWEN=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
OPENROUTER_API_KEY_GEMINI=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
```

### Passo 7: Criar Web Service
- Clique em **"Create Web Service"**
- Aguarde o build (5-10 minutos)

## 📦 Opção 2: Deploy Manual via ZIP

### Passo 1: Criar Pacote de Deploy
```bash
# Execute o script de deploy
deploy_render_automatico.bat
```

### Passo 2: Upload no Render
1. Acesse: https://dashboard.render.com
2. Clique em **"New +"** → **"Web Service"**
3. Selecione **"Deploy from existing code"**
4. Clique em **"Upload files"**
5. Arraste o arquivo `deploy_render.zip`

### Passo 3: Configurar Serviço
```
Name: roteiro-dispersacao
Environment: Python 3
Region: Oregon (US West) - Free
Build Command: pip install -r requirements.txt
Start Command: gunicorn app_optimized:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

## ⚡ Opção 3: Deploy via Render CLI

### Passo 1: Instalar Render CLI
```bash
# Via winget (Windows)
winget install render.render-cli

# Via chocolatey
choco install render-cli

# Via npm
npm install -g @render/cli
```

### Passo 2: Autenticar
```bash
render login
```

### Passo 3: Deploy Automático
```bash
# Execute o script PowerShell
deploy_render_automatico.ps1
```

## 🔍 Monitoramento e Logs

### Verificar Status
- **Dashboard**: https://dashboard.render.com
- **Logs**: Clique no serviço → "Logs"
- **Health Check**: https://roteiro-dispersacao.onrender.com/api/health

### Logs Importantes
```bash
# Build logs
pip install -r requirements.txt

# Runtime logs
gunicorn app_optimized:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120

# Health check
GET /api/health
```

## 🚨 Solução de Problemas

### Erro: "Build failed"
**Causas possíveis:**
- Dependências incompatíveis
- Versão do Python incorreta
- Arquivo `requirements.txt` malformado

**Soluções:**
1. Verifique o `requirements.txt`
2. Limpe o cache: Settings → Build & Deploy → "Clear build cache"
3. Verifique a versão do Python (3.11.0)

### Erro: "Module not found"
**Causas possíveis:**
- Dependência não instalada
- Arquivo não incluído no deploy

**Soluções:**
1. Adicione a dependência ao `requirements.txt`
2. Verifique se todos os arquivos estão no ZIP
3. Teste localmente: `pip install -r requirements.txt`

### Erro: "Port already in use"
**Causas possíveis:**
- Configuração de porta incorreta
- Múltiplos workers

**Soluções:**
1. Use `$PORT` (variável do Render)
2. Configure apenas 1 worker: `--workers 1`
3. Aumente o timeout: `--timeout 120`

### Erro: "Memory limit exceeded"
**Causas possíveis:**
- Modelos AI muito grandes
- Múltiplos workers

**Soluções:**
1. Use apenas 1 worker
2. Otimize os modelos
3. Use modelos menores
4. Configure swap se necessário

## 📊 Recursos do Render (Gratuito)

- **750 horas/mês** de runtime
- **512 MB RAM** por serviço
- **1 CPU** compartilhado
- **Auto-sleep** após 15 minutos de inatividade
- **Custom domains** gratuitos
- **SSL automático**
- **CDN global**

## 🔄 Deploy Automático

### GitHub Actions
- Cada push para `main` = novo deploy
- Pull requests = deploy de preview
- Rollback automático em caso de erro

### Webhooks
- Deploy manual via webhook
- Integração com outros serviços
- Notificações automáticas

## 📱 URLs e Endpoints

### URLs Principais
- **Site**: https://roteiro-dispersacao.onrender.com
- **API Chat**: https://roteiro-dispersacao.onrender.com/api/chat
- **Health Check**: https://roteiro-dispersacao.onrender.com/api/health
- **Info API**: https://roteiro-dispersacao.onrender.com/api/info

### Endpoints Disponíveis
```
GET  /                    # Página principal
GET  /tese               # Página da tese
GET  /api/health         # Health check
GET  /api/info           # Informações da API
POST /api/chat           # Chatbot API
```

## ✅ Checklist de Deploy

### Pré-deploy
- [ ] `app_optimized.py` funcionando localmente
- [ ] `requirements.txt` atualizado
- [ ] `render.yaml` configurado
- [ ] Arquivos de template presentes
- [ ] PDFs incluídos

### Durante o deploy
- [ ] Build sem erros
- [ ] Health check passando
- [ ] Logs sem erros críticos
- [ ] API respondendo

### Pós-deploy
- [ ] Site acessível
- [ ] Chatbot funcionando
- [ ] Modelos AI carregados
- [ ] Performance adequada

## 🎉 Sucesso!

Após o deploy bem-sucedido, seu chatbot estará disponível em:
**https://roteiro-dispersacao.onrender.com**

### Funcionalidades Disponíveis
- ✅ Chat com Dr. Gasnelio (formal)
- ✅ Chat com Gá (informal)
- ✅ Análise de documentos PDF
- ✅ Respostas baseadas na tese
- ✅ Histórico de conversas
- ✅ Interface responsiva

### Próximos Passos
1. Teste todas as funcionalidades
2. Configure domínio personalizado (opcional)
3. Configure monitoramento
4. Configure backups (se necessário)

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs no Render
2. Teste localmente primeiro
3. Consulte a documentação do Render
4. Verifique as configurações do projeto

---

**🎯 Objetivo Alcançado**: Deploy automático configurado para https://roteiro-dispersacao.onrender.com 