# 🔧 Solução para Deploy no Netlify

## ❌ Problema Identificado

O erro indica que o arquivo `requirements.txt` não está sendo encontrado no repositório GitHub durante o build do Netlify.

## ✅ Soluções Disponíveis

### Opção 1: Upload Manual (Recomendado)

**Vantagens:** Simples, rápido, não precisa de Git
**Tempo estimado:** 5-10 minutos

#### Passo a Passo:

1. **Acesse o Netlify:**
   - Vá para [https://app.netlify.com/](https://app.netlify.com/)
   - Faça login na sua conta

2. **Crie um novo site:**
   - Clique em "Add new site"
   - Selecione "Deploy manually"

3. **Arraste a pasta do projeto:**
   - Selecione TODA a pasta do projeto (incluindo PDFs/, functions/, etc.)
   - Arraste para a área de upload

4. **Configure o build:**
   - **Build command:** `pip install -r requirements.txt`
   - **Publish directory:** `.`
   - **Functions directory:** `functions`
   - **Python version:** `3.9`

5. **Clique em "Deploy site"**

### Opção 2: Instalar Git e Fazer Push

**Vantagens:** Deploy automático, controle de versão
**Tempo estimado:** 15-20 minutos

#### Passo a Passo:

1. **Instale o Git:**
   - Baixe em: [https://git-scm.com/download/win](https://git-scm.com/download/win)
   - Instale com configurações padrão

2. **Configure o Git:**
   ```bash
   git config --global user.name "Seu Nome"
   git config --global user.email "seu.email@exemplo.com"
   ```

3. **Inicialize o repositório:**
   ```bash
   git init
   git remote add origin https://github.com/AnalineS/siteroteirodedispersacao.git
   ```

4. **Adicione os arquivos:**
   ```bash
   git add .
   git commit -m "Deploy das melhorias para Netlify"
   git push -u origin main
   ```

### Opção 3: Usar GitHub Desktop

**Vantagens:** Interface gráfica, mais fácil
**Tempo estimado:** 10-15 minutos

1. **Instale GitHub Desktop:**
   - Baixe em: [https://desktop.github.com/](https://desktop.github.com/)

2. **Clone o repositório:**
   - Abra GitHub Desktop
   - Clone: `https://github.com/AnalineS/siteroteirodedispersacao`

3. **Adicione os arquivos:**
   - Arraste todos os arquivos para a pasta
   - Commit e push

## 📋 Arquivos Essenciais para o Deploy

Certifique-se de que estes arquivos estão incluídos:

```
✅ requirements.txt          # Dependências Python
✅ netlify.toml             # Configuração do Netlify
✅ functions/api.py         # Função serverless
✅ index.html              # Interface principal
✅ script.js               # JavaScript do chat
✅ PDFs/                   # Pasta com o PDF da tese
✅ .gitignore              # Arquivos a ignorar
```

## 🚀 Configurações Recomendadas no Netlify

### Build Settings:
- **Build command:** `pip install -r requirements.txt`
- **Publish directory:** `.`
- **Functions directory:** `functions`

### Environment Variables:
- **PYTHON_VERSION:** `3.9`
- **NODE_VERSION:** `18`

### Redirects:
```
/api/*  /.netlify/functions/api/:splat  200
/*      /index.html                     200
```

## 🔍 Verificação Pós-Deploy

1. **Teste a API:**
   - Acesse: `https://seu-site.netlify.app/api/chat`
   - Deve retornar status 200

2. **Teste o chat:**
   - Acesse: `https://seu-site.netlify.app`
   - Faça uma pergunta sobre hanseníase

3. **Verifique os logs:**
   - No painel do Netlify > Functions > Logs

## 🆘 Troubleshooting

### Erro: "requirements.txt not found"
- Verifique se o arquivo está na raiz do projeto
- Confirme que foi incluído no upload/commit

### Erro: "Function timeout"
- As funções têm limite de 10 segundos
- Otimize o código se necessário

### Erro: "PDF not found"
- Verifique se a pasta PDFs/ está incluída
- Confirme o nome do arquivo PDF

## 📞 Suporte

Se ainda tiver problemas:
1. Verifique os logs no painel do Netlify
2. Teste localmente primeiro: `python app_production.py`
3. Consulte a documentação: [https://docs.netlify.com/](https://docs.netlify.com/)

---

**Recomendação:** Use a **Opção 1 (Upload Manual)** para um deploy rápido e simples! 