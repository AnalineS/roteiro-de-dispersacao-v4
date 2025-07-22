# 🐍 Deploy no PythonAnywhere - Especializado em Python

## ✅ Por que PythonAnywhere?

- **Especializado em Python:** Otimizado para aplicações Python
- **Plano gratuito:** 512MB RAM, 1GB storage
- **Sem limite de tempo:** Sempre online
- **SSL gratuito:** HTTPS automático
- **Domínio personalizado:** Gratuito
- **IDE integrado:** Editor de código online

---

## 🚀 Passo a Passo - PythonAnywhere

### 1️⃣ Criar Conta
- Acesse: [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)
- Crie uma conta gratuita
- Faça login no painel

### 2️⃣ Upload dos Arquivos

#### Opção A: Upload via Git
```bash
# No terminal do PythonAnywhere
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

#### Opção B: Upload Manual
- Vá em "Files" no painel
- Crie pasta `roteiro-dispersacao`
- Upload dos arquivos:
  - `app_production.py`
  - `requirements.txt`
  - `index.html`
  - `script.js`
  - Pasta `PDFs/`

### 3️⃣ Configurar Ambiente Python

#### Instalar dependências:
```bash
# No terminal do PythonAnywhere
cd roteiro-dispersacao
pip3 install --user -r requirements.txt
```

#### Verificar instalação:
```bash
python3 -c "import flask, transformers, torch; print('✅ Dependências instaladas')"
```

### 4️⃣ Configurar Web App

#### No painel do PythonAnywhere:
1. Vá em "Web" > "Add a new web app"
2. Escolha "Manual configuration"
3. Selecione Python 3.9
4. Configure:
   - **Source code:** `/home/seu-usuario/roteiro-dispersacao`
   - **Working directory:** `/home/seu-usuario/roteiro-dispersacao`
   - **WSGI configuration file:** Editar automaticamente

#### Editar WSGI file:
```python
import sys
import os

# Adicionar o diretório do projeto ao path
path = '/home/seu-usuario/roteiro-dispersacao'
if path not in sys.path:
    sys.path.append(path)

# Importar a aplicação Flask
from app_production import app as application

# Configurar para produção
application.config['DEBUG'] = False
```

### 5️⃣ Configurar Arquivos Estáticos

#### Criar pasta static:
```bash
mkdir static
cp index.html static/
cp script.js static/
```

#### Configurar no Flask:
```python
# No app_production.py
from flask import send_from_directory

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)
```

### 6️⃣ Configurar Domínio

#### No painel "Web":
- **Domain:** `seu-usuario.pythonanywhere.com`
- **HTTPS:** Ativado automaticamente

---

## 🎯 Vantagens do PythonAnywhere

✅ **Sempre online** (sem cold start)  
✅ **Especializado em Python**  
✅ **IDE integrado** para edição  
✅ **Terminal Linux** completo  
✅ **SSL gratuito** automático  
✅ **Domínio personalizado** gratuito  
✅ **Backup automático**  
✅ **Logs detalhados**  

---

## 📊 Limitações do Plano Gratuito

| Recurso | Limite |
|---------|--------|
| **RAM** | 512 MB |
| **Storage** | 1 GB |
| **CPU** | Limitado |
| **Domínios** | 1 subdomínio |
| **Web apps** | 1 app |
| **Always-on tasks** | Não disponível |

---

## 🔧 Configuração Otimizada

### Para PythonAnywhere:
```python
# No app_production.py
if __name__ == '__main__':
    # PythonAnywhere usa porta 8000 por padrão
    app.run(host='0.0.0.0', port=8000, debug=False)
```

### Otimizar uso de memória:
```python
# Carregar modelos apenas quando necessário
class HanseniaseChatbot:
    def __init__(self):
        self.models_loaded = False
        self.qa_pipeline = None
        self.embedding_model = None
    
    def load_models_if_needed(self):
        if not self.models_loaded:
            self.load_models()
            self.models_loaded = True
```

### Health Check:
```python
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'platform': 'PythonAnywhere',
        'timestamp': datetime.now().isoformat()
    })
```

---

## 🎉 Resultado

Após o deploy, você terá:
- **URL:** `https://seu-usuario.pythonanywhere.com`
- **Sempre online** (sem cold start)
- **IDE integrado** para edições
- **Logs** detalhados
- **SSL** automático

---

## 🆘 Troubleshooting

### Erro: "Memory limit exceeded"
- PythonAnywhere tem limite de 512MB
- Otimize o modelo de IA
- Use carregamento lazy dos modelos

### Erro: "Import error"
- Verifique se as dependências foram instaladas
- Use `pip3 install --user` para instalar localmente
- Verifique o path no WSGI file

### Erro: "Static files not found"
- Configure corretamente a pasta static
- Verifique as permissões dos arquivos
- Use `send_from_directory` no Flask

### Erro: "Timeout"
- PythonAnywhere tem limite de 30 segundos por requisição
- Otimize o processamento de IA
- Use cache para respostas

---

## 💡 Dicas de Otimização

### 1. Usar modelo menor:
```python
# Usar modelo mais leve
self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
```

### 2. Implementar cache:
```python
# Cache simples em memória
self.cache = {}
cache_key = hashlib.md5(question.encode()).hexdigest()
if cache_key in self.cache:
    return self.cache[cache_key]
```

### 3. Otimizar carregamento:
```python
# Carregar PDF apenas uma vez
if not hasattr(self, 'pdf_loaded'):
    self.load_pdf_content()
    self.pdf_loaded = True
```

---

## 🎯 Próximos Passos

1. **Crie conta** no PythonAnywhere
2. **Upload dos arquivos** via Git ou manual
3. **Configure o web app** seguindo o guia
4. **Teste o site** após o deploy
5. **Configure domínio personalizado** (opcional)
6. **Monitore performance** através dos logs

---

## 🔄 Migração do Netlify

### Vantagens da migração:
- ✅ **Sem problemas de build** complexos
- ✅ **Sempre online** (sem cold start)
- ✅ **Especializado em Python**
- ✅ **IDE integrado** para manutenção
- ✅ **Logs mais detalhados**

### Desvantagens:
- ❌ **Limite de RAM** (512MB)
- ❌ **Interface menos moderna**
- ❌ **Menos recursos** que Netlify

---

**🐍 PythonAnywhere é perfeito para aplicações Python!**
**✅ Sempre online e sem problemas de build!** 