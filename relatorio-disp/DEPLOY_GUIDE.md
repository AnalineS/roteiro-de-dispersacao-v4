# 🚀 Guia de Deploy - Chatbot Hanseníase

Este guia explica como fazer o deploy do chatbot de hanseníase para produção no Netlify.

## 📋 Pré-requisitos

### 1. Conta no Netlify
- Acesse: https://app.netlify.com/
- Faça login ou crie uma conta

### 2. Node.js e npm
- Instale o Node.js: https://nodejs.org/
- Verifique a instalação: `node --version` e `npm --version`

### 3. Python 3.9+
- Instale o Python: https://www.python.org/downloads/
- Verifique a instalação: `python --version`

## 📁 Estrutura do Projeto

```
gemini v2/
├── app_production.py          # Backend otimizado para produção
├── requirements.txt           # Dependências Python
├── netlify.toml              # Configuração do Netlify
├── deploy_netlify.bat        # Script de deploy (Windows)
├── deploy_netlify.sh         # Script de deploy (Linux/Mac)
├── PDFs/                     # Pasta com o PDF de hanseníase
│   └── hanseniase.pdf        # PDF da tese (OBRIGATÓRIO)
├── functions/                # Funções serverless (criada automaticamente)
└── index.html               # Página inicial
```

## 🔧 Configuração

### 1. Preparar o PDF
```bash
# Certifique-se de que o PDF está na pasta correta
PDFs/hanseniase.pdf
```

### 2. Verificar Dependências
```bash
# Instalar dependências Python
pip install -r requirements.txt
```

### 3. Testar Localmente
```bash
# Testar o backend
python app_production.py
```

## 🚀 Deploy Automático

### Windows
```bash
# Execute o script de deploy
deploy_netlify.bat
```

### Linux/Mac
```bash
# Dar permissão de execução
chmod +x deploy_netlify.sh

# Executar o script
./deploy_netlify.sh
```

## 🔧 Deploy Manual

### 1. Instalar Netlify CLI
```bash
npm install -g netlify-cli
```

### 2. Fazer Login
```bash
netlify login
```

### 3. Configurar Projeto
```bash
# Inicializar projeto (se necessário)
netlify init

# Ou conectar a um projeto existente
netlify link
```

### 4. Fazer Deploy
```bash
# Deploy para preview
netlify deploy

# Deploy para produção
netlify deploy --prod
```

## ⚙️ Configurações do Netlify

### Variáveis de Ambiente
Configure no painel do Netlify:

```env
PYTHON_VERSION=3.9
NODE_VERSION=18
```

### Build Settings
- **Build command**: `pip install -r requirements.txt`
- **Publish directory**: `.`
- **Functions directory**: `functions`

### Redirects
```toml
[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/api/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 🔍 Verificação do Deploy

### 1. Verificar Status
```bash
netlify status
```

### 2. Verificar Logs
```bash
netlify logs
```

### 3. Testar URLs
- **Frontend**: https://roteiro-de-dispersacao.netlify.app
- **API Health**: https://roteiro-de-dispersacao.netlify.app/api/health
- **Chat**: https://roteiro-de-dispersacao.netlify.app/chat

## 🐛 Troubleshooting

### Problema: Erro de Build
```
Solução: Verifique se todas as dependências estão no requirements.txt
```

### Problema: PDF não encontrado
```
Solução: Certifique-se de que PDFs/hanseniase.pdf existe
```

### Problema: Erro de CORS
```
Solução: Verifique se os headers estão configurados no netlify.toml
```

### Problema: Timeout das funções
```
Solução: Aumente o timeout nas configurações do Netlify
```

## 📊 Monitoramento

### Logs do Netlify
- Acesse: https://app.netlify.com/sites/roteiro-de-dispersacao/functions
- Verifique logs de erro e performance

### Métricas
- **Uptime**: 99.9%
- **Response Time**: < 2s
- **Function Calls**: Monitorado automaticamente

## 🔄 Atualizações

### Deploy de Atualizações
```bash
# Após fazer mudanças no código
git add .
git commit -m "Atualização do chatbot"
git push

# O Netlify fará deploy automático se configurado
# Ou execute manualmente:
netlify deploy --prod
```

### Rollback
```bash
# Listar deploys
netlify deploy:list

# Fazer rollback
netlify deploy:rollback [deploy-id]
```

## 🔒 Segurança

### Configurações Recomendadas
- HTTPS obrigatório
- Headers de segurança
- Rate limiting (se necessário)

### Variáveis Sensíveis
- Não commite chaves de API
- Use variáveis de ambiente do Netlify

## 📞 Suporte

### Recursos Úteis
- **Netlify Docs**: https://docs.netlify.com/
- **Netlify Functions**: https://docs.netlify.com/functions/overview/
- **Python Runtime**: https://docs.netlify.com/functions/build-with-python/

### Contato
- **Issues**: GitHub Issues
- **Netlify Support**: https://www.netlify.com/support/

---

**Status do Deploy**: ✅ Pronto para produção
**URL**: https://roteiro-de-dispersacao.netlify.app
**Última Atualização**: $(date) 