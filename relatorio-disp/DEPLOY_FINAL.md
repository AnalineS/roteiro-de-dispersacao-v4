# 🚀 Deploy Final - Netlify

## ✅ Arquivo ZIP Criado!

O arquivo `deploy_netlify.zip` foi criado com todos os arquivos necessários para o deploy.

## 📋 Passo a Passo Rápido

### 1. Acesse o Netlify
- Vá para: [https://app.netlify.com/](https://app.netlify.com/)
- Faça login na sua conta

### 2. Crie Novo Site
- Clique em **"Add new site"**
- Selecione **"Deploy manually"**

### 3. Upload do Arquivo
- **Opção A:** Arraste o arquivo `deploy_netlify.zip` para a área de upload
- **Opção B:** Clique em "Browse files" e selecione o ZIP

### 4. Configure o Build
Na tela de configuração, defina:

```
Build command: pip install -r requirements.txt
Publish directory: .
Functions directory: functions
Python version: 3.9
```

### 5. Deploy
- Clique em **"Deploy site"**
- Aguarde o build (pode demorar 2-5 minutos)

## 🎯 Resultado Esperado

Após o deploy bem-sucedido, você terá:
- ✅ Site funcionando em: `https://seu-site.netlify.app`
- ✅ Chatbot com todas as melhorias implementadas
- ✅ Duas personalidades: Dr. Gasnelio e Gá
- ✅ Respostas baseadas no PDF da tese
- ✅ Sistema de sinônimos e busca otimizada

## 🔍 Teste o Deploy

1. **Teste a API:**
   ```
   https://seu-site.netlify.app/api/chat
   ```

2. **Teste o Chat:**
   - Acesse o site
   - Faça perguntas como:
     - "O que é hanseníase?"
     - "Como tratar a lepra?"
     - "Quais são os sintomas?"

## 🆘 Se Houver Problemas

### Erro de Build
- Verifique se o Python 3.9 está selecionado
- Confirme se o `requirements.txt` está no ZIP

### Erro de Função
- Verifique os logs em: Functions > Logs
- As funções têm limite de 10 segundos

### PDF não Encontrado
- Confirme se a pasta `PDFs/` está no ZIP
- Verifique o nome do arquivo PDF

## 📞 Suporte

Se precisar de ajuda:
1. Verifique os logs no painel do Netlify
2. Teste localmente primeiro: `python app_production.py`
3. Consulte: `SOLUCAO_DEPLOY_NETLIFY.md`

---

**🎉 Pronto! Seu chatbot de hanseníase estará online com todas as melhorias!** 