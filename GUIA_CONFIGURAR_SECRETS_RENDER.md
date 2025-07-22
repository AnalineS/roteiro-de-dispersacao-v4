# 🚀 Guia de Configuração - Deploy Automático Render

Este guia explica como configurar os secrets necessários no GitHub para que o deploy automático funcione corretamente.

## 📋 Secrets Necessários

### 1. RENDER_API_KEY
**O que é:** Chave de API do Render para autenticar as requisições de deploy.

**Como obter:**
1. Acesse https://dashboard.render.com
2. Clique no seu nome de usuário (canto superior direito)
3. Vá em "Account Settings"
4. Role até "API Keys"
5. Clique em "Create API Key"
6. Dê um nome (ex: "GitHub Actions")
7. Copie a chave gerada

### 2. RENDER_SERVICE_ID
**O que é:** ID único do serviço backend no Render.

**Como obter:**
1. Acesse https://dashboard.render.com
2. Clique no seu serviço backend
3. Na URL, você verá algo como: `https://dashboard.render.com/web/srv-abc123def456`
4. O ID é `srv-abc123def456` (parte após `/srv-`)

### 3. RENDER_SERVICE_NAME
**O que é:** Nome do serviço backend (usado para gerar a URL).

**Como obter:**
1. No dashboard do Render, veja o nome do seu serviço
2. Exemplo: se o nome é "roteiro-dispersacao-chatbot", a URL será `https://roteiro-dispersacao-chatbot.onrender.com`

### 4. RENDER_FRONTEND_SERVICE_NAME (Opcional)
**O que é:** Nome do serviço frontend (se você tiver um separado).

**Como obter:**
1. Mesmo processo do backend, mas para o serviço frontend

## 🔧 Como Configurar no GitHub

### Passo 1: Acessar Settings do Repositório
1. Vá para seu repositório no GitHub
2. Clique em "Settings" (aba superior)
3. No menu lateral, clique em "Secrets and variables" → "Actions"

### Passo 2: Adicionar Secrets
1. Clique em "New repository secret"
2. Para cada secret:

#### RENDER_API_KEY
- **Name:** `RENDER_API_KEY`
- **Value:** `rnd_abc123def456...` (sua chave de API)

#### RENDER_SERVICE_ID
- **Name:** `RENDER_SERVICE_ID`
- **Value:** `srv_abc123def456...` (ID do serviço)

#### RENDER_SERVICE_NAME
- **Name:** `RENDER_SERVICE_NAME`
- **Value:** `roteiro-dispersacao-chatbot` (nome do serviço)

#### RENDER_FRONTEND_SERVICE_NAME (Opcional)
- **Name:** `RENDER_FRONTEND_SERVICE_NAME`
- **Value:** `roteiro-dispersacao-frontend` (nome do serviço frontend)

### Passo 3: Verificar Configuração
1. Na página de secrets, você deve ver:
   - ✅ RENDER_API_KEY
   - ✅ RENDER_SERVICE_ID
   - ✅ RENDER_SERVICE_NAME
   - ✅ RENDER_FRONTEND_SERVICE_NAME (se aplicável)

## 🧪 Testando a Configuração

### Teste 1: Verificar Secrets
```bash
# No workflow, os secrets são acessados assim:
echo "API Key configurada: ${{ secrets.RENDER_API_KEY != '' }}"
echo "Service ID configurado: ${{ secrets.RENDER_SERVICE_ID != '' }}"
```

### Teste 2: Deploy Manual
1. Vá para a aba "Actions" no GitHub
2. Clique em "Deploy Automático - Render"
3. Clique em "Run workflow"
4. Selecione a branch "main"
5. Clique em "Run workflow"

### Teste 3: Verificar Logs
1. Clique no workflow em execução
2. Verifique se não há erros relacionados aos secrets
3. Procure por mensagens como:
   - ✅ "Deploy iniciado com ID: ..."
   - ✅ "Deploy concluído com sucesso!"

## 🚨 Troubleshooting

### Erro: "RENDER_SERVICE_ID não configurado"
**Solução:**
1. Verifique se o secret `RENDER_SERVICE_ID` foi adicionado corretamente
2. Confirme se o ID está correto (sem espaços extras)
3. Verifique se o serviço existe no Render

### Erro: "Unauthorized" ou "Invalid API Key"
**Solução:**
1. Verifique se a `RENDER_API_KEY` está correta
2. Confirme se a chave não expirou
3. Verifique se a chave tem permissões adequadas

### Erro: "Service not found"
**Solução:**
1. Verifique se o `RENDER_SERVICE_ID` está correto
2. Confirme se o serviço ainda existe no Render
3. Verifique se você tem acesso ao serviço

### Erro: "Deploy failed"
**Solução:**
1. Verifique os logs do Render
2. Confirme se o código está funcionando localmente
3. Verifique se todas as dependências estão no `requirements.txt`

## 📊 Monitoramento

### Verificar Status dos Serviços
1. **Render Dashboard:** https://dashboard.render.com
2. **GitHub Actions:** https://github.com/[seu-usuario]/[seu-repo]/actions
3. **Logs do Render:** No dashboard do serviço, aba "Logs"

### URLs dos Serviços
- **Backend:** `https://[RENDER_SERVICE_NAME].onrender.com`
- **Frontend:** `https://[RENDER_FRONTEND_SERVICE_NAME].onrender.com`

## 🔄 Deploy Automático

Após configurar os secrets, o deploy será automático:

1. **Push para main/master** → Deploy automático
2. **Pull Request** → Testes automáticos
3. **Manual** → Via GitHub Actions

## 📞 Suporte

Se encontrar problemas:

1. **Verifique os logs** do GitHub Actions
2. **Consulte a documentação** do Render
3. **Teste localmente** antes do deploy
4. **Verifique os secrets** estão configurados corretamente

---

**✅ Configuração concluída!** Seu projeto agora terá deploy automático no Render. 