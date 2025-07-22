# 🚀 Deploy Manual via GitHub (Sem Git)

## ✅ Alternativa para Quem Não Tem Git

Se você não tem o Git instalado ou prefere fazer upload manual, aqui está a solução:

## 📁 Arquivos Necessários

### 🎯 Upload Manual para GitHub
1. **Acesse:** [https://github.com/AnalineS/siteroteirodedispersacao](https://github.com/AnalineS/siteroteirodedispersacao)
2. **Clique em "Add file"** > **"Upload files"**
3. **Arraste os arquivos** necessários:

### 📋 Lista de Arquivos para Upload

#### Arquivos Essenciais:
- ✅ `requirements.txt`
- ✅ `netlify_build_fix.sh`
- ✅ `netlify.toml`
- ✅ `index.html`
- ✅ `script.js`
- ✅ `functions/api.py`
- ✅ `PDFs/` (pasta completa)

#### Arquivos de Configuração:
- ✅ `.github/workflows/deploy.yml` (criar pasta)
- ✅ `README.md` (atualizar)

## 🚀 Passo a Passo Manual

### Passo 1: Criar Pasta .github/workflows
1. No GitHub, clique em **"Add file"** > **"Create new file"**
2. Nome: `.github/workflows/deploy.yml`
3. Cole o conteúdo do arquivo `github_netlify_deploy.yml`

### Passo 2: Upload dos Arquivos
1. **"Add file"** > **"Upload files"**
2. Arraste os arquivos um por um ou em lote
3. **Commit message:** "Setup deploy automático"
4. Clique em **"Commit changes"**

### Passo 3: Configurar Netlify
1. **Acesse:** [https://app.netlify.com/](https://app.netlify.com/)
2. **"Add new site"** > **"Import an existing project"**
3. **Conecte com GitHub:**
   - Clique em "GitHub"
   - Autorize o Netlify
   - Selecione: `AnalineS/siteroteirodedispersacao`

### Passo 4: Configurar Build
```
Build command: bash netlify_build_fix.sh
Publish directory: .
Functions directory: functions
Python version: 3.9
```

### Passo 5: Deploy
- Clique em **"Deploy site"**
- Aguarde o primeiro deploy

## 🔄 Atualizações Futuras

### Via GitHub Web:
1. **Edite arquivos** diretamente no GitHub
2. **Commit changes**
3. **Deploy automático** no Netlify

### Via Upload:
1. **"Add file"** > **"Upload files"**
2. **Substitua** os arquivos modificados
3. **Commit changes**
4. **Deploy automático**

## 🎯 Vantagens do Método Manual

### ✅ Simplicidade
- **Sem instalação** de Git
- **Interface web** familiar
- **Upload direto** no GitHub

### ✅ Controle
- **Visualização** antes do commit
- **Histórico** de mudanças
- **Rollback** fácil

### ✅ Acessibilidade
- **Funciona** em qualquer computador
- **Sem configuração** local
- **Colaboração** via web

## 📊 Monitoramento

### GitHub
- **Commits:** Histórico de mudanças
- **Actions:** Status do deploy automático
- **Files:** Estrutura do projeto

### Netlify
- **Deploys:** Status de cada deploy
- **Functions:** Logs das funções
- **Analytics:** Estatísticas do site

## 🆘 Troubleshooting Manual

### Erro: "Arquivo não encontrado"
- Verifique se o arquivo foi uploadado corretamente
- Confirme o nome e extensão do arquivo

### Erro: "Build falhou"
- Verifique se `requirements.txt` está na raiz
- Confirme se `netlify_build_fix.sh` está presente

### Erro: "GitHub Actions não executou"
- Verifique se `.github/workflows/deploy.yml` existe
- Confirme se o arquivo está na pasta correta

## 📈 Próximos Passos

### Para Fazer Mudanças:
1. **Edite** no GitHub ou **upload** novo arquivo
2. **Commit changes**
3. **Aguarde** deploy automático (2-5 minutos)

### Para Adicionar Funcionalidades:
1. **Desenvolva** localmente
2. **Teste** completamente
3. **Upload** para GitHub
4. **Deploy automático** no Netlify

## 🎉 Resultado Final

Após configurar o deploy manual:

✅ **Site sempre atualizado** via GitHub
✅ **Deploy automático** a cada commit
✅ **Histórico completo** de mudanças
✅ **Interface web** simples
✅ **Sem instalação** de software
✅ **Colaboração** facilitada

---

**🚀 Use o método manual se preferir não instalar o Git!** 