# 🎨 GUIA COMPLETO - INTEGRAÇÃO COM LANGFLOW

## 📋 Visão Geral

Este guia mostra como integrar o **Langflow** com seu chatbot de hanseníase, criando fluxos visuais de IA mais avançados e flexíveis.

## 🎯 O que é o Langflow?

**Langflow** é uma ferramenta visual para criar fluxos de IA (LLM workflows) sem código. Permite:
- ✅ Criar fluxos visuais de IA
- ✅ Conectar diferentes modelos e componentes
- ✅ Testar e iterar rapidamente
- ✅ Deploy de fluxos como APIs
- ✅ Interface web intuitiva

## 🚀 Vantagens da Integração

### Para seu Chatbot de Hanseníase:
- **Fluxos Visuais**: Crie pipelines de IA arrastando e soltando
- **Múltiplos Modelos**: Combine diferentes modelos de IA
- **Processamento Avançado**: Chunking, embeddings, busca semântica
- **Fallback Inteligente**: Sistema padrão como backup
- **Monitoramento**: Logs e métricas detalhadas

## 📦 Arquivos Criados

### 🔧 Arquivos de Integração
- **`langflow_integration.py`** - Classe principal de integração
- **`app_with_langflow.py`** - App Flask com integração automática
- **`setup_langflow.bat`** - Script de instalação automática

### 📋 Guias e Documentação
- **`GUIA_LANGFLOW_INTEGRATION.md`** - Este guia completo

## 🛠️ Instalação e Configuração

### Passo 1: Instalação Automática (Recomendado)
```bash
# Execute o script de instalação
setup_langflow.bat
```

### Passo 2: Instalação Manual
```bash
# Instalar Langflow
pip install langflow

# Instalar dependências adicionais
pip install requests typing-extensions

# Testar instalação
python langflow_integration.py
```

### Passo 3: Iniciar o Langflow
```bash
# Iniciar servidor Langflow
langflow run

# Acessar interface web
# http://localhost:7860
```

## 🎨 Criando Fluxos no Langflow

### Fluxo Básico para Hanseníase

1. **Acesse a Interface**
   - Vá para: http://localhost:7860
   - Clique em "Create New Flow"

2. **Adicione Componentes**
   ```
   Input → Document Loader → Text Splitter → 
   Embedding Model → Vector Store → 
   Retriever → LLM → Prompt Template → Output
   ```

3. **Configure Cada Componente**

#### Input Node
```json
{
  "input_type": "str",
  "required": true,
  "placeholder": "Digite sua pergunta sobre hanseníase"
}
```

#### Document Loader
```json
{
  "file_path": "PDFs/Roteiro de Dsispensação - Hanseníase.md",
  "loader_type": "markdown"
}
```

#### Text Splitter
```json
{
  "chunk_size": 1500,
  "chunk_overlap": 300,
  "separator": "\n\n"
}
```

#### Embedding Model
```json
{
  "model_name": "all-MiniLM-L6-v2",
  "device": "cpu"
}
```

#### Vector Store
```json
{
  "store_type": "memory",
  "similarity_metric": "cosine"
}
```

#### Retriever
```json
{
  "top_k": 3,
  "similarity_threshold": 0.3
}
```

#### LLM Node
```json
{
  "model_name": "deepset/roberta-base-squad2",
  "task": "question-answering",
  "max_length": 512
}
```

#### Prompt Template
```json
{
  "template": """
  Você é um especialista em hanseníase. Responda baseado no contexto fornecido.
  
  Personalidade: {personality}
  - Dr. Gasnelio: Tom sério e técnico, linguagem formal
  - Gá: Tom descontraído e acessível, linguagem simples
  
  Contexto: {context}
  Pergunta: {question}
  
  Resposta:
  """,
  "input_variables": ["personality", "context", "question"]
}
```

## 🔗 Integração com seu Sistema

### Opção 1: Sistema Híbrido (Recomendado)
```python
# Usar app_with_langflow.py
python app_with_langflow.py
```

**Vantagens:**
- ✅ Detecta Langflow automaticamente
- ✅ Fallback para sistema padrão
- ✅ Cache inteligente
- ✅ Monitoramento completo

### Opção 2: Integração Manual
```python
from langflow_integration import HanseniaseLangflowBridge

# Criar bridge
bridge = HanseniaseLangflowBridge()

# Configurar ambiente
setup_result = bridge.setup_langflow_environment()

# Processar pergunta
result = bridge.answer_question(
    question="Qual o tratamento para hanseníase?",
    personality="dr_gasnelio"
)
```

## 📊 Monitoramento e Logs

### Endpoints de Monitoramento
```bash
# Status do sistema
GET /api/system-status

# Health check
GET /api/health

# Informações da API
GET /api/info
```

### Logs Importantes
```python
# Verificar se Langflow está ativo
if chatbot.use_langflow:
    print("✅ Langflow ativo")
else:
    print("ℹ️ Usando sistema padrão")

# Verificar cache
print(f"Cache size: {len(chatbot.cache)}")

# Verificar chunks
print(f"Chunks loaded: {len(chatbot.chunks)}")
```

## 🎯 Fluxos Avançados

### Fluxo 1: Análise de Documentos
```
Input → Document Loader → Text Splitter → 
Embedding → Vector Store → 
Retriever → LLM → 
Sentiment Analysis → Output
```

### Fluxo 2: Resposta Personalizada
```
Input → Personality Detector → 
Document Loader → Text Splitter → 
Embedding → Vector Store → 
Retriever → LLM → 
Personality Filter → Output
```

### Fluxo 3: Validação Médica
```
Input → Medical Term Extractor → 
Document Loader → Text Splitter → 
Embedding → Vector Store → 
Retriever → LLM → 
Medical Validator → Output
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```bash
# .env
LANGFLOW_API_KEY=your_api_key_here
LANGFLOW_URL=http://localhost:7860
LANGFLOW_FLOW_ID=hanseniase_default
```

### Configuração de Cache
```python
# Cache persistente
import pickle

def save_cache(cache, filename="langflow_cache.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(cache, f)

def load_cache(filename="langflow_cache.pkl"):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except:
        return {}
```

### Configuração de Modelos
```python
# Modelos alternativos
MODELS_CONFIG = {
    "qa_model": "deepset/roberta-base-squad2",
    "embedding_model": "all-MiniLM-L6-v2",
    "text_generation": "gpt2",
    "sentiment": "cardiffnlp/twitter-roberta-base-sentiment"
}
```

## 🚨 Solução de Problemas

### Erro: "Langflow não disponível"
**Causas:**
- Langflow não instalado
- Servidor não iniciado
- Porta bloqueada

**Soluções:**
```bash
# 1. Instalar Langflow
pip install langflow

# 2. Iniciar servidor
langflow run

# 3. Verificar porta
netstat -an | findstr 7860
```

### Erro: "Flow não encontrado"
**Causas:**
- Fluxo não criado
- ID incorreto
- Permissões

**Soluções:**
```python
# 1. Criar fluxo
flow_result = langflow.create_hanseniase_flow()

# 2. Verificar fluxos disponíveis
flows = langflow.get_available_flows()

# 3. Usar ID correto
result = langflow.process_question(question, flow_id=flow_result["id"])
```

### Erro: "Timeout na resposta"
**Causas:**
- Modelo muito lento
- Chunks muito grandes
- Sem cache

**Soluções:**
```python
# 1. Reduzir chunk size
chunk_size = 1000  # em vez de 1500

# 2. Usar cache
cache_enabled = True

# 3. Timeout maior
timeout = 120  # segundos
```

## 📈 Métricas e Performance

### Métricas Importantes
- **Tempo de resposta**: < 5 segundos
- **Taxa de cache hit**: > 60%
- **Confiança média**: > 40%
- **Erros**: < 5%

### Otimizações
```python
# 1. Cache inteligente
cache_ttl = 3600  # 1 hora

# 2. Chunking otimizado
chunk_size = 1500
chunk_overlap = 300

# 3. Threshold ajustável
similarity_threshold = 0.3
```

## 🎉 Exemplos de Uso

### Exemplo 1: Pergunta Simples
```python
# Pergunta sobre tratamento
result = chatbot.answer_question(
    "Qual é o tratamento para hanseníase?",
    "dr_gasnelio"
)

print(result["answer"])
# Dr. Gasnelio responde:
# Baseado na minha tese, o tratamento para hanseníase...
```

### Exemplo 2: Pergunta com Gá
```python
# Pergunta informal
result = chatbot.answer_question(
    "Como eu sei se tenho hanseníase?",
    "ga"
)

print(result["answer"])
# Gá explica: Olha, se você tem manchas na pele que não doem...
```

### Exemplo 3: Monitoramento
```python
# Verificar status
status = chatbot.get_system_info()

print(f"Langflow ativo: {status['langflow_active']}")
print(f"Cache size: {status['cache_size']}")
print(f"Chunks: {status['chunks_loaded']}")
```

## 🔄 Deploy com Langflow

### Deploy Local
```bash
# 1. Iniciar Langflow
langflow run

# 2. Iniciar chatbot
python app_with_langflow.py

# 3. Acessar
# http://localhost:5000
```

### Deploy em Produção
```bash
# 1. Configurar Langflow
export LANGFLOW_API_KEY=your_key
export LANGFLOW_URL=https://your-langflow-server.com

# 2. Deploy chatbot
gunicorn app_with_langflow:app

# 3. Configurar proxy reverso
# Nginx/Apache para rotear /api/* para Langflow
```

## 📚 Recursos Adicionais

### Documentação Oficial
- **Langflow Docs**: https://docs.langflow.org/
- **API Reference**: https://docs.langflow.org/api
- **Examples**: https://github.com/logspace-ai/langflow

### Comunidade
- **Discord**: https://discord.gg/langflow
- **GitHub**: https://github.com/logspace-ai/langflow
- **Twitter**: @LangflowAI

## ✅ Checklist de Integração

### Pré-requisitos
- [ ] Python 3.9+ instalado
- [ ] PDF da tese presente
- [ ] Dependências instaladas

### Instalação
- [ ] Langflow instalado
- [ ] Script de setup executado
- [ ] Servidor Langflow rodando

### Configuração
- [ ] Fluxo criado no Langflow
- [ ] Integração testada
- [ ] Fallback funcionando

### Testes
- [ ] Perguntas simples
- [ ] Perguntas complexas
- [ ] Ambas personalidades
- [ ] Monitoramento

## 🎯 Próximos Passos

1. **Teste a integração** com perguntas simples
2. **Crie fluxos personalizados** no Langflow
3. **Otimize performance** com cache e chunking
4. **Configure monitoramento** e logs
5. **Deploy em produção** com Langflow

---

**🎉 Sucesso!** Seu chatbot agora tem integração completa com Langflow!

### URLs Importantes
- **Chatbot**: http://localhost:5000
- **Langflow**: http://localhost:7860
- **API Status**: http://localhost:5000/api/system-status 