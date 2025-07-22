# 🚀 Deploy Automático Netlify - Roteiro de Dispersação

## ✅ Status: PRONTO PARA DEPLOY

**Data:** 13/07/2025  
**Arquivo:** `deploy_automatico.zip` (816KB)  
**Status:** ✅ Criado com sucesso

---

## 📋 Pré-requisitos

- ✅ Conta no Netlify (gratuita)
- ✅ Arquivo `deploy_automatico.zip` (já criado)
- ✅ Conexão com internet

---

## 🚀 Passo a Passo - Deploy Automático

### 1️⃣ Acesse o Netlify
- Vá para: [https://app.netlify.com/](https://app.netlify.com/)
- Faça login na sua conta

### 2️⃣ Crie Novo Site
- Clique em **"Add new site"**
- Selecione **"Deploy manually"**

### 3️⃣ Upload do Arquivo
- Arraste o arquivo **`deploy_automatico.zip`** para a área de upload
- Aguarde o upload completar (pode demorar 1-2 minutos)

### 4️⃣ Configure o Build
Na tela de configuração, defina exatamente:

```
Build command: bash netlify_build_fix.sh
Publish directory: .
Functions directory: functions
Python version: 3.9
```

### 5️⃣ Deploy
- Clique em **"Deploy site"**
- Aguarde o build (2-5 minutos)

---

## 🎯 O Que o Script Automático Faz

### ✅ Durante o Build:
1. **Cria `requirements.txt`** com todas as dependências
2. **Configura `functions/api.py`** com melhorias implementadas
3. **Instala dependências Python** automaticamente
4. **Verifica estrutura de arquivos**
5. **Resolve problemas de configuração**
6. **Configura ambiente otimizado**

### ✅ Melhorias Implementadas:
- **Sistema de sinônimos** (30+ termos médicos)
- **Busca semântica otimizada**
- **Chunking inteligente** (1500 chars, overlap 300)
- **Cache de respostas**
- **Extração de contexto**
- **Duas personalidades** (Dr. Gasnelio e Gá)
- **Threshold de confiança ajustado** (0.3)

---

## 🔍 Verificação Pós-Deploy

### 1️⃣ Teste a API
```
https://seu-site.netlify.app/.netlify/functions/api
```

### 2️⃣ Teste o Chat
- Acesse: `https://seu-site.netlify.app`
- Faça perguntas como:
  - "O que é hanseníase?"
  - "Como tratar a lepra?"
  - "Quais são os sintomas?"
  - "Como é feito o diagnóstico?"

### 3️⃣ Verifique os Logs
- No painel do Netlify > Functions > Logs
- Deve mostrar: "✅ Build personalizado concluído!"

---

## 🆘 Troubleshooting

### ❌ Erro: "Build failed"
**Solução:**
- Verifique se o Python 3.9 está selecionado
- Confirme se o build command está correto: `bash netlify_build_fix.sh`
- Verifique os logs de erro no painel do Netlify

### ❌ Erro: "Function timeout"
**Solução:**
- As funções têm limite de 10 segundos
- O script está otimizado para performance
- Se persistir, verifique a conexão com internet

### ❌ Erro: "PDF not found"
**Solução:**
- O script verifica automaticamente a pasta PDFs/
- Confirme que o PDF está no ZIP
- Verifique se o nome do arquivo está correto

### ❌ Erro: "Module not found"
**Solução:**
- O script instala automaticamente todas as dependências
- Verifique se o `requirements.txt` foi criado
- Aguarde o build completar (pode demorar)

---

## 📊 Métricas Esperadas

### Performance:
- **Tempo de resposta:** 3-8 segundos
- **Cobertura:** 70-80% das perguntas
- **Precisão:** Melhorada com sinônimos

### Funcionalidades:
- **Sinônimos:** 30+ termos médicos
- **Chunks:** 129 chunks do PDF
- **Cache:** Respostas em cache
- **Personalidades:** Dr. Gasnelio (técnico) e Gá (descontraído)

---

## 🎉 Resultado Final

Após o deploy bem-sucedido, você terá:

✅ **Site funcionando** em `https://seu-site.netlify.app`  
✅ **Chatbot com todas as melhorias** implementadas  
✅ **Sistema de sinônimos** funcionando  
✅ **Busca semântica otimizada**  
✅ **Duas personalidades** distintas  
✅ **Respostas baseadas no PDF** da tese  
✅ **Performance otimizada**  

---

## 📞 Suporte

Se ainda tiver problemas:

1. **Verifique os logs** no painel do Netlify
2. **Teste localmente:** `python app_production.py`
3. **Consulte:** `SOLUCAO_DEPLOY_NETLIFY.md`
4. **Verifique:** `DEPLOY_FINAL_AUTOMATICO.md`

---

## 🎯 Próximos Passos

1. **Faça o deploy** seguindo o passo a passo
2. **Teste o site** após o deploy
3. **Configure domínio personalizado** (opcional)
4. **Monitore performance** através dos logs

---

**🚀 O arquivo `deploy_automatico.zip` está pronto para upload!**  
**✅ O script resolve todos os problemas automaticamente!** 

---

Ótimo! Vamos preparar o deploy via GitHub, que é o método mais recomendado para o Render. Vou te guiar passo a passo, incluindo a instalação do Git, configuração do repositório e push para o GitHub.

---

## 1️⃣ Instalar o Git

1. Baixe o instalador do Git:  
   [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Execute o instalador e siga as instruções padrão.
3. Após instalar, feche e reabra o terminal (PowerShell).

Para testar se o Git está instalado, digite no terminal:
```powershell
git --version
```
Se aparecer a versão do Git, está tudo certo!

---

## 2️⃣ Inicializar o repositório Git

No terminal, dentro da pasta do projeto, execute:
```powershell
git init
git add .
git commit -m "Primeiro commit - Roteiro de Dispersação"
```

---

## 3️⃣ Criar repositório no GitHub

1. Acesse: [https://github.com/](https://github.com/)
2. Clique em **New repository**
3. Nomeie como: `roteiro-dispersacao`
4. Deixe como **Público** ou **Privado** (como preferir)
5. **Não** marque para criar README, .gitignore ou licença (deixe vazio)

---

## 4️⃣ Conectar o repositório local ao GitHub

No terminal, execute (substitua `SEU_USUARIO` pelo seu usuário do GitHub):

```powershell
git remote add origin https://github.com/SEU_USUARIO/roteiro-dispersacao.git
git branch -M main
git push -u origin main
```

Se pedir login, siga as instruções do terminal (pode ser via navegador).

---

## 5️⃣ Deploy no Render

1. Acesse: [https://render.com/](https://render.com/)
2. Faça login com GitHub
3. Clique em **New +** > **Web Service**
4. Escolha o repositório `roteiro-dispersacao`
5. Configure:
   - **Name:** roteiro-dispersacao
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app_production:app`
6. Clique em **Create Web Service**
7. Aguarde o build (5-10 minutos)
8. O site ficará disponível em:  
   `https://roteiro-dispersacao.onrender.com`

---

## 6️⃣ Pós-deploy

- Teste o site e a API conforme o guia.
- Cada push no GitHub fará deploy automático no Render!

---

Se precisar de comandos prontos para copiar e colar, me avise!  
Se tiver qualquer dúvida durante o processo, é só perguntar!

Ótimo, agora o Render está conseguindo fazer o build do seu projeto!  
Porém, o erro principal é:

```
bash: line 1: gunicorn: command not found
```

Isso significa que o pacote **gunicorn** não está instalado no ambiente do Render.

---

## Como resolver

### 1️⃣ Adicione o gunicorn ao seu `requirements.txt`

Abra o arquivo `requirements.txt` e adicione a seguinte linha (se ainda não estiver lá):

```
gunicorn==21.2.0
```

> Dica: O gunicorn deve estar no mesmo arquivo que já tem flask, transformers, etc.

---

### 2️⃣ Salve, faça commit e envie para o GitHub

No terminal, execute:

```powershell
git add requirements.txt
git commit -m "Adiciona gunicorn ao requirements.txt para deploy no Render"
git push origin main
```

---

### 3️⃣ No Render, clique em “Manual Deploy” > “Deploy latest commit”

Isso vai forçar o Render a instalar o gunicorn e rodar o comando corretamente.

---

## Observação sobre FastAPI

O Render instalou FastAPI e Uvicorn porque seu `requirements.txt` começa com:

```
fastapi
uvicorn[standard]
```

Se o seu projeto é Flask, **remova** essas linhas do `requirements.txt`!  
Seu arquivo deve começar assim:

```
flask==2.3.3
flask-cors==4.0.0
...
gunicorn==21.2.0
```

---

## Resumo dos passos:

1. Remova `fastapi` e `uvicorn` do `requirements.txt` se não usa FastAPI.
2. Adicione `gunicorn==21.2.0` ao `requirements.txt`.
3. Commit e push para o GitHub.
4. Faça novo deploy no Render.

---

Se seguir esses passos, seu deploy Flask no Render vai funcionar!  
Se aparecer outro erro, envie o log aqui que te ajudo a resolver.

O Render (e o pip) está tentando instalar um pacote chamado `siteroteirodedispersacao` do PyPI, mas esse pacote não existe.

---

## Como resolver (passo a passo):

1. **Abra o arquivo `requirements.txt`** no seu editor de texto.

2. **Remova a linha** que contém apenas:
   ```
   siteroteirodedispersacao
   ```
   (ou qualquer variação desse nome)

3. **Salve o arquivo.**

4. **No terminal, execute:**
   ```powershell
   git add requirements.txt
   git commit -m "Remove linha siteroteirodedispersacao do requirements.txt"
   git push origin main
   ```

5. **No Render, clique em “Manual Deploy” > “Deploy latest commit”**  
   Isso vai rodar o build novamente, agora sem esse erro.

---

**Resumo:**  
Seu `requirements.txt` deve conter apenas pacotes reais do PyPI, como flask, gunicorn, transformers, etc.  
Não coloque o nome do seu projeto nesse arquivo.

---

Se seguir esses passos, o erro será resolvido!  
Se aparecer outro erro, envie o log aqui que te ajudo a resolver. 

---

Seu projeto deve ser Flask puro, sem FastAPI.  
Se seguir esses passos, o deploy vai funcionar!

Se aparecer outro erro, envie o log aqui que te ajudo a resolver. 

---

Seu projeto deve ser Flask puro, sem FastAPI.  
Se seguir esses passos, o deploy vai funcionar!

Se aparecer outro erro, envie o log aqui que te ajudo a resolver. 