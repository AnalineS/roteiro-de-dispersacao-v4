# 🚀 Deploy Automático via GitHub Actions

## ✅ Solução Completa

Criei um **sistema de deploy automático** que conecta seu GitHub diretamente ao Netlify, fazendo deploy automático a cada push.

## 📁 Arquivos Criados

### 🔧 Workflow do GitHub Actions
- **`github_netlify_deploy.yml`** - Configuração do deploy automático
- **`setup_github_deploy.bat`** - Script para configurar tudo

### 🎯 Como Funciona
1. **Push para GitHub** → **GitHub Actions** → **Deploy no Netlify**
2. **Automático** a cada commit na branch `main`
3. **Sem necessidade** de upload manual

## 🚀 Passo a Passo (10 minutos)

### Passo 1: Instalar Git (se necessário)
- Baixe em: [https://git-scm.com/download/win](https://git-scm.com/download/win)
- Instale com configurações padrão

### Passo 2: Executar Script de Setup
```bash
setup_github_deploy.bat
```

Este script vai:
- ✅ Verificar se o Git está instalado
- ✅ Inicializar o repositório Git
- ✅ Criar pasta `.github/workflows/`
- ✅ Copiar o workflow do GitHub Actions
- ✅ Adicionar todos os arquivos ao Git
- ✅ Fazer commit e push para o GitHub

### Passo 3: Configurar Netlify
1. **Acesse:** [https://app.netlify.com/](https://app.netlify.com/)
2. **"Add new site"** > **"Import an existing project"**
3. **Conecte com GitHub:**
   - Clique em "GitHub"
   - Autorize o Netlify
   - Selecione: `AnalineS/siteroteirodedispersacao`

### Passo 4: Configurar Build
Na tela de configuração do Netlify:

```
Build command: bash netlify_build_fix.sh
Publish directory: .
Functions directory: functions
Python version: 3.9
```

### Passo 5: Deploy
- Clique em **"Deploy site"**
- Aguarde o primeiro deploy (2-5 minutos)

## 🔄 Deploy Automático

Após configurado, **cada push para a branch `main`** fará deploy automático:

```bash
# Para fazer uma atualização:
git add .
git commit -m "Nova funcionalidade"
git push origin main
# → Deploy automático no Netlify!
```

## 🎯 Vantagens do Deploy Automático

### ✅ Automatização
- **Deploy automático** a cada push
- **Sem upload manual** necessário
- **Versionamento** completo

### ✅ Confiabilidade
- **Build consistente** no GitHub Actions
- **Testes automáticos** antes do deploy
- **Rollback fácil** se necessário

### ✅ Colaboração
- **Múltiplos desenvolvedores** podem fazer push
- **Histórico completo** de mudanças
- **Pull requests** com preview

## 📊 Status do Deploy

### GitHub Actions
- Acesse: [https://github.com/AnalineS/siteroteirodedispersacao/actions](https://github.com/AnalineS/siteroteirodedispersacao/actions)
- Veja o status de cada deploy

### Netlify
- Acesse: [https://app.netlify.com/](https://app.netlify.com/)
- Veja logs e status do site

## 🔍 Verificação

### 1. Teste o Site
- Acesse: `https://seu-site.netlify.app`
- Teste o chatbot

### 2. Teste a API
```
https://seu-site.netlify.app/.netlify/functions/api
```

### 3. Verifique os Logs
- GitHub Actions: Status do build
- Netlify: Logs do deploy

## 🆘 Troubleshooting

### Erro: "Git não encontrado"
- Instale o Git: [https://git-scm.com/download/win](https://git-scm.com/download/win)

### Erro: "Push falhou"
- Verifique se o repositório está configurado: `git remote -v`
- Confirme as credenciais do GitHub

### Erro: "Build falhou no Netlify"
- Verifique os logs no painel do Netlify
- Confirme se o `requirements.txt` está no repositório

### Erro: "GitHub Actions não executou"
- Verifique: [https://github.com/AnalineS/siteroteirodedispersacao/actions](https://github.com/AnalineS/siteroteirodedispersacao/actions)
- Confirme se o workflow está na pasta `.github/workflows/`

## 📈 Próximos Passos

### Para Fazer Atualizações:
1. **Edite os arquivos** localmente
2. **Teste localmente:** `python app_production.py`
3. **Push para GitHub:**
   ```bash
   git add .
   git commit -m "Descrição da mudança"
   git push origin main
   ```
4. **Deploy automático** acontece em 2-5 minutos

### Para Adicionar Novas Funcionalidades:
1. **Desenvolva** localmente
2. **Teste** completamente
3. **Push** para GitHub
4. **Deploy automático** no Netlify

## 🎉 Resultado Final

Após configurar o deploy automático:

✅ **Site sempre atualizado** com a versão mais recente
✅ **Deploy automático** a cada push
✅ **Histórico completo** de mudanças
✅ **Rollback fácil** se necessário
✅ **Colaboração simplificada**
✅ **Sem upload manual** necessário

---

**🚀 Execute `setup_github_deploy.bat` para configurar tudo automaticamente!** 