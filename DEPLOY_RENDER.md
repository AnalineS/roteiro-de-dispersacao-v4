# 🎨 Deploy no Render - Alternativa Gratuita

## ✅ Por que Render?

- **Totalmente gratuito:** 750 horas/mês
- **Python nativo:** Suporte completo a Flask
- **Deploy automático:** Integração com GitHub
- **SSL gratuito:** HTTPS automático
- **Domínio personalizado:** Gratuito
- **Sem cartão de crédito:** Necessário

---

## 🚀 Passo a Passo - Render

### 1️⃣ Preparar o Projeto

#### Criar `render.yaml`:
```yaml
services:
  - type: web
    name: roteiro-dispersacao
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app_production:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: FLASK_ENV
        value: production
```

#### Atualizar `requirements.txt`:
```
flask==2.3.3
flask-cors==4.0.0
transformers==4.35.0
torch==2.1.0
sentence-transformers==2.2.2
PyPDF2==3.0.1
numpy==1.24.3
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

#### Criar `gunicorn.conf.py`:
```python
bind = "0.0.0.0:10000"
workers = 2
timeout = 120
max_requests = 1000
max_requests_jitter = 100
```

### 2️⃣ Criar Conta no Render
- Acesse: [https://render.com/](https://render.com/)
- Faça login com GitHub
- Clique em "New +" > "Web Service"

### 3️⃣ Deploy
- Conecte seu repositório GitHub
- Configure:
  - **Name:** `roteiro-dispersacao`
  - **Environment:** `Python 3`
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `gunicorn app_production:app`
- Clique em "Create Web Service"

### 4️⃣ Configurar Variáveis de Ambiente
No painel do Render, adicione:
```
FLASK_ENV=production
PYTHON_VERSION=3.9.0
```

---

## 🎯 Vantagens do Render

✅ **750 horas gratuitas** por mês  
✅ **Deploy automático** do GitHub  
✅ **SSL gratuito** automático  
✅ **Domínio personalizado** gratuito  
✅ **Logs em tempo real**  
✅ **Health checks** automáticos  
✅ **Backup automático**  

---

## 📊 Comparação de Limitações

| Recurso | Plano Gratuito |
|---------|----------------|
| **Horas/mês** | 750 horas |
| **RAM** | 512 MB |
| **CPU** | 0.1 vCPU |
| **Storage** | 1 GB |
| **Bandwidth** | Ilimitado |
| **Domínios** | Ilimitado |

---

## 🔧 Configuração Otimizada

### Para melhor performance no Render:
```python
# No app_production.py
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
```

### Health Check otimizado:
```python
@app.route('/api/health')
def health_check():
    try:
        # Verificar se os modelos estão carregados
        if hasattr(app, 'chatbot') and app.chatbot.qa_pipeline:
            return jsonify({
                'status': 'healthy',
                'models_loaded': True,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'loading',
                'models_loaded': False,
                'timestamp': datetime.now().isoformat()
            }), 503
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500
```

---

## 🎉 Resultado

Após o deploy, você terá:
- **URL:** `https://roteiro-dispersacao.onrender.com`
- **Deploy automático** a cada push no GitHub
- **Logs** em tempo real
- **Monitoramento** de performance
- **SSL** automático

---

## 🆘 Troubleshooting

### Erro: "Build timeout"
- Render tem limite de 15 minutos para build
- Otimize o `requirements.txt`
- Use versões específicas das dependências

### Erro: "Memory limit exceeded"
- Render tem limite de 512MB
- Otimize o modelo de IA
- Reduza o número de workers no Gunicorn

### Erro: "Service not responding"
- Verifique se o health check está funcionando
- Confirme se a porta está correta (10000)
- Verifique os logs no Render

### Erro: "Cold start"
- Render "dorme" após 15 minutos de inatividade
- Primeira requisição pode demorar 30-60 segundos
- Considere usar um serviço de "ping" para manter ativo

---

## 💡 Dicas de Otimização

### 1. Reduzir tamanho do modelo:
```python
# Usar modelo menor
self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
```

### 2. Otimizar carregamento:
```python
# Carregar modelos apenas quando necessário
def __init__(self):
    self.models_loaded = False
    # Carregar modelos na primeira requisição
```

### 3. Usar cache:
```python
# Implementar cache Redis ou similar
# Para o plano gratuito, usar cache em memória
```

---

## 🎯 Próximos Passos

1. **Faça o deploy** no Render seguindo o guia
2. **Teste o site** após o deploy
3. **Configure domínio personalizado** (opcional)
4. **Monitore performance** através dos logs
5. **Configure alertas** para downtime

---

**🚀 Render é uma excelente alternativa gratuita ao Netlify!**
**✅ 750 horas gratuitas por mês são suficientes para projetos pequenos!** 