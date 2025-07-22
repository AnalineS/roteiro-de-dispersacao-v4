# 🚀 Deploy Manual - Chatbot Hanseníase

Guia para fazer deploy manual no Netlify usando apenas o painel web, sem necessidade do CLI.

## 📋 Pré-requisitos

1. **Conta no Netlify**: https://app.netlify.com/
2. **PDF de hanseníase**: Coloque em `PDFs/hanseniase.pdf`
3. **Arquivos do projeto**: Todos os arquivos devem estar prontos

## 🔧 Passo a Passo

### 1. Preparar os Arquivos

Certifique-se de que os seguintes arquivos estão presentes:

```
✅ app_production.py          # Backend otimizado
✅ requirements.txt           # Dependências Python
✅ netlify.toml              # Configuração do Netlify
✅ index.html               # Página inicial
✅ PDFs/hanseniase.pdf      # PDF da tese (OBRIGATÓRIO)
```

### 2. Acessar o Netlify

1. Vá para: https://app.netlify.com/
2. Faça login na sua conta
3. Clique em "Add new site" → "Deploy manually"

### 3. Fazer Upload dos Arquivos

1. **Arraste toda a pasta do projeto** para a área de upload
2. Ou clique em "Browse files" e selecione todos os arquivos
3. Aguarde o upload completar

### 4. Configurar Build Settings

Após o upload, configure:

#### Build Settings
- **Build command**: `pip install -r requirements.txt`
- **Publish directory**: `.`
- **Functions directory**: `functions`

#### Environment Variables
Adicione estas variáveis:
```
PYTHON_VERSION=3.9
NODE_VERSION=18
```

### 5. Configurar Redirects

No painel do Netlify, vá em:
**Site settings** → **Build & deploy** → **Redirects**

Adicione estes redirects:

```
/api/*  /.netlify/functions/api/:splat  200
/*      /index.html                     200
```

### 6. Configurar Headers

Vá em:
**Site settings** → **Build & deploy** → **Headers**

Adicione para `/api/*`:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

### 7. Fazer Deploy

1. Clique em "Deploy site"
2. Aguarde o build completar
3. Verifique se não há erros nos logs

## 🔍 Verificação

### Testar URLs
- **Frontend**: `https://seu-site.netlify.app`
- **API Health**: `https://seu-site.netlify.app/api/health`
- **Chat**: `https://seu-site.netlify.app/chat`

### Verificar Logs
1. Vá em **Functions** no painel
2. Verifique se não há erros
3. Teste as funções individualmente

## 🐛 Troubleshooting

### Erro: Build Failed
```
Solução: Verifique se requirements.txt está correto
```

### Erro: PDF não encontrado
```
Solução: Certifique-se de que PDFs/hanseniase.pdf existe
```

### Erro: CORS
```
Solução: Verifique se os headers estão configurados
```

### Erro: Function Timeout
```
Solução: Aumente o timeout nas configurações
```

## 📊 Monitoramento

### Logs
- **Build logs**: Painel → Deploys → [deploy] → View deploy log
- **Function logs**: Painel → Functions → [function] → View logs

### Métricas
- **Uptime**: Monitorado automaticamente
- **Performance**: Analytics do Netlify

## 🔄 Atualizações

### Deploy de Novas Versões
1. Faça as mudanças no código
2. Faça upload novamente (substitua os arquivos)
3. O Netlify fará novo deploy automaticamente

### Rollback
1. Vá em **Deploys**
2. Clique em um deploy anterior
3. Clique em "Publish deploy"

## 🔒 Segurança

### Configurações Recomendadas
- ✅ HTTPS obrigatório (automático no Netlify)
- ✅ Headers de segurança configurados
- ✅ CORS configurado corretamente

## 📞 Suporte

### Recursos
- **Netlify Docs**: https://docs.netlify.com/
- **Netlify Support**: https://www.netlify.com/support/

### Contato
- **Issues**: GitHub Issues
- **Email**: suporte@netlify.com

---

**Status**: ✅ Pronto para deploy manual
**Dificuldade**: ⭐⭐ (Fácil)
**Tempo estimado**: 15-30 minutos 