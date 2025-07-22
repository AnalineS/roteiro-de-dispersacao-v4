# Configuração de Secrets no GitHub Codespaces

## ✅ Status: Integrações Mantidas

As integrações **CONTINUARÃO FUNCIONANDO** porque:
- O arquivo `Vector Store RAG.json` contém apenas configurações de fluxo
- As APIs usam variáveis de ambiente para tokens
- Sistema tem fallback automático

## 🔧 Como Configurar Secrets no GitHub

### 1. Acesse o Repositório no GitHub

1. Vá para: https://github.com/AnalineS/roteirodedispersacao
2. Clique em **Settings** (Configurações)
3. No menu lateral, clique em **Secrets and variables** → **Actions**

### 2. Secrets Necessários

Adicione os seguintes secrets:

#### `LANGFLOW_API_KEY`
- **Descrição**: Chave da API do Langflow
- **Valor**: Sua chave da API do Langflow
- **Como obter**: 
  - Acesse https://langflow.cloud
  - Faça login → Settings → API Keys
  - Crie uma nova chave

#### `RENDER_API_KEY`
- **Descrição**: Chave da API do Render
- **Valor**: Sua chave da API do Render
- **Como obter**:
  - Acesse https://dashboard.render.com
  - Account → API Keys
  - Crie uma nova chave

#### `OPENAI_API_KEY` (Opcional)
- **Descrição**: Chave da API do OpenAI
- **Valor**: Sua chave da API do OpenAI
- **Como obter**:
  - Acesse https://platform.openai.com
  - API Keys → Create new secret key

#### `GITHUB_PAT`
- **Descrição**: Personal Access Token do GitHub
- **Valor**: Seu token pessoal do GitHub
- **Como obter**:
  - Acesse https://github.com/settings/tokens
  - Generate new token
  - Escopos: `repo`, `workflow`

### 3. Como Adicionar um Secret

1. Clique em **New repository secret**
2. Nome: `LANGFLOW_API_KEY`
3. Valor: Cole sua chave da API
4. Clique em **Add secret**
5. Repita para os outros secrets

### 4. Verificação no Codespace

No GitHub Codespaces, os secrets estarão disponíveis como variáveis de ambiente:

```bash
echo $LANGFLOW_API_KEY
echo $RENDER_API_KEY
echo $OPENAI_API_KEY
```

### 5. Teste das Integrações

Após configurar os secrets:

```bash
# Teste da integração com Langflow
python test_langflow_integration.py

# Teste do chatbot
python test_chat.py

# Teste da API
python test_api.py
```

### 6. Deploy Automático

Com os secrets configurados:

1. **Commit e Push**:
   ```bash
   git add .
   git commit -m "Configurar secrets para deploy"
   git push origin main
   ```

2. **Monitoramento**:
   - Vá para https://github.com/AnalineS/roteirodedispersacao/actions
   - Acompanhe o workflow de deploy

3. **Render**:
   - O deploy será automático no Render
   - URL: https://roteiro-dispersacao.onrender.com

### 7. Troubleshooting

Se algo não funcionar:

1. **Verifique os secrets**:
   - Todos configurados corretamente?
   - Valores corretos?

2. **Teste localmente**:
   ```bash
   export LANGFLOW_API_KEY="sua_chave"
   python app.py
   ```

3. **Logs do Render**:
   - Acesse o dashboard do Render
   - Verifique os logs de deploy

### 8. Segurança

✅ **Boa Prática**:
- Secrets configurados no GitHub
- Nenhum token no código
- Variáveis de ambiente seguras
- Fallback automático funcionando

---

## 🚀 Próximos Passos

1. Configure os secrets no GitHub
2. Faça commit das alterações
3. Push para o repositório
4. Monitore o deploy automático
5. Teste a aplicação no Render

**Status**: ✅ Pronto para Deploy
**Integrações**: ✅ Mantidas e Funcionais 