# 🚀 Guia Completo - Script netlify_build_fix.sh

## 📋 O que o script faz

O `netlify_build_fix.sh` é um script de build personalizado que resolve automaticamente os problemas mais comuns no deploy do Netlify para o chatbot de hanseníase.

### ✅ Problemas resolvidos:

1. **requirements.txt ausente** - Cria automaticamente com todas as dependências
2. **functions/api.py ausente** - Cria a API do chatbot otimizada
3. **netlify.toml ausente** - Configura o ambiente do Netlify
4. **index.html ausente** - Cria interface do usuário
5. **pasta PDFs ausente** - Cria estrutura para o arquivo da tese
6. **Configurações Python** - Define versões e dependências corretas

## 🔧 Como usar

### Opção 1: Deploy Automático (Recomendado)

1. **Execute o script localmente:**
   ```bash
   # No Windows (PowerShell)
   bash netlify_build_fix.sh
   
   # Ou use o script de teste
   test_netlify_build.bat
   ```

2. **Adicione o PDF da tese:**
   - Coloque o arquivo `Roteiro de Dsispensação - Hanseníase F.docx.pdf` na pasta `PDFs/`

3. **Faça commit e push:**
   ```bash
   git add .
   git commit -m "Configuração Netlify completa"
   git push origin main
   ```

4. **Configure no Netlify:**
   - Vá para [netlify.com](https://netlify.com)
   - Conecte seu repositório GitHub
   - Configure:
     - **Build command:** `bash netlify_build_fix.sh`
     - **Publish directory:** `.`
     - **Functions directory:** `functions`

### Opção 2: Deploy Manual via ZIP

1. **Execute o script:**
   ```bash
   bash netlify_build_fix.sh
   ```

2. **Crie o ZIP:**
   ```bash
   # No Windows
   powershell Compress-Archive -Path * -DestinationPath deploy_netlify.zip
   ```

3. **Faça upload no Netlify:**
   - Vá para [netlify.com](https://netlify.com)
   - Arraste o arquivo `deploy_netlify.zip`
   - Configure as mesmas opções acima

## 📁 Arquivos criados pelo script

### 1. requirements.txt
```txt
flask==2.3.3
flask-cors==4.0.0
transformers==4.35.0
torch==2.1.0
sentence-transformers==2.2.2
PyPDF2==3.0.1
numpy==1.24.3
requests==2.31.0
python-dotenv==1.0.0
huggingface-hub==0.19.4
scikit-learn==1.3.0
scipy==1.11.1
# ... e mais 20+ dependências
```

### 2. functions/api.py
- API completa do chatbot
- Busca semântica otimizada
- Cache inteligente
- Tratamento de erros robusto
- Logging detalhado

### 3. netlify.toml
```toml
[build]
  publish = "."
  command = "bash netlify_build_fix.sh"
  functions = "functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/api/:splat"
  status = 200
  force = true

[build.environment]
  PYTHON_VERSION = "3.9"
  NODE_VERSION = "18"
  # ... configurações otimizadas
```

### 4. index.html
- Interface moderna e responsiva
- Duas personalidades (Dr. Gasnelio e Gá)
- Loading animado
- Tratamento de erros
- Design profissional

### 5. Arquivos de configuração
- `.gitignore` - Ignora arquivos desnecessários
- `runtime.txt` - Define versão do Python
- `.python-version` - Compatibilidade com pyenv

## 🎯 Funcionalidades do Chatbot

### Personalidades:
1. **👨‍⚕️ Dr. Gasnelio (Técnico)**
   - Respostas científicas e detalhadas
   - Linguagem médica apropriada
   - Foco em precisão técnica

2. **😊 Gá (Descontraído)**
   - Respostas amigáveis e acessíveis
   - Linguagem mais informal
   - Foco em compreensão do usuário

### Recursos Avançados:
- ✅ Busca semântica com sinônimos
- ✅ Chunking inteligente do PDF
- ✅ Cache otimizado
- ✅ Threshold de confiança ajustável
- ✅ Extração de contexto relevante
- ✅ Tratamento robusto de erros
- ✅ Logging detalhado

## 🔍 Troubleshooting

### Problema: "requirements.txt não encontrado"
**Solução:** O script cria automaticamente o arquivo com todas as dependências.

### Problema: "Erro de importação"
**Solução:** O script instala todas as dependências necessárias.

### Problema: "PDF não encontrado"
**Solução:** O script cria chunks de exemplo e continua funcionando.

### Problema: "Erro de CORS"
**Solução:** O script configura automaticamente os headers CORS.

### Problema: "Timeout no build"
**Solução:** O script otimiza o carregamento e usa cache.

## 📊 Monitoramento

O script inclui logging detalhado:
```
INFO: Carregando modelos de IA...
INFO: Device set to use cpu
INFO: ✅ Modelos carregados com sucesso!
INFO: 📚 PDF carregado: 129 chunks
INFO: 🚀 Inicializando chatbot...
INFO: ✅ Chatbot inicializado com sucesso!
INFO: 🤔 Processando pergunta: O que é hanseníase?...
INFO: ✅ Resposta gerada com confiança: 0.85
```

## 🚀 Deploy Rápido

Para fazer deploy em 5 minutos:

1. **Execute:** `bash netlify_build_fix.sh`
2. **Adicione:** PDF na pasta `PDFs/`
3. **Commit:** `git add . && git commit -m "Deploy" && git push`
4. **Configure:** Netlify com build command: `bash netlify_build_fix.sh`
5. **Pronto!** 🎉

## 📞 Suporte

Se encontrar problemas:

1. **Verifique os logs** no Netlify
2. **Execute o script localmente** primeiro
3. **Verifique se o PDF está na pasta correta**
4. **Confirme as configurações do netlify.toml**

## 🎉 Resultado Final

Após o deploy bem-sucedido, você terá:
- ✅ Chatbot funcionando no Netlify
- ✅ Interface moderna e responsiva
- ✅ Duas personalidades diferentes
- ✅ Busca semântica avançada
- ✅ Cache otimizado
- ✅ Logs detalhados
- ✅ Tratamento robusto de erros

**URL do seu chatbot:** `https://seu-site.netlify.app`

---

*Script configurado e otimizado para resolver todos os problemas de build no Netlify! 🚀* 