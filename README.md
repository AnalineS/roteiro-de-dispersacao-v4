# Roteiro de Dispersão Bot v4

Sistema de chatbot modernizado com RAG (Retrieval-Augmented Generation), LangFlow, FAISS e integração OpenRouter para consultas sobre roteiro de dispersão atmosférica.

## 🚀 Características

- **Sistema RAG Avançado**: Busca e geração de respostas baseadas em documentos técnicos
- **Duas Personas**: Dr. Gasnelio (técnico) e Gá (amigável)
- **Integração LangFlow**: Fluxos avançados de processamento
- **Banco Astra DB**: Armazenamento de histórico e embeddings
- **Interface Streamlit**: Interface web moderna e responsiva
- **API Flask**: Endpoints REST para integração
- **Deploy Automático**: CI/CD com GitHub Actions e Render

## 🛠️ Tecnologias

- **Backend**: Python 3.11, Flask, FastAPI
- **Frontend**: Streamlit
- **IA/ML**: OpenRouter (Claude-3), LangChain, FAISS, Sentence Transformers
- **Banco de Dados**: Astra DB (Cassandra)
- **Orquestração**: LangFlow
- **Deploy**: Render, Docker
- **CI/CD**: GitHub Actions

## 📋 Pré-requisitos

- Python 3.11+
- Conta Astra DB
- API Key OpenRouter
- API Key LangFlow
- Conta GitHub (para deploy)
- Conta Render (para hospedagem)

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/AnalineS/roteiro-de-dispersacao-v4.git
cd roteiro-de-dispersacao-v4
```

### 2. Crie ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale dependências
```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

### 5. Execute a aplicação
```bash
# Interface Streamlit
python app/main.py --mode streamlit

# API Flask
python app/main.py --mode flask

# Apenas inicializar componentes
python app/main.py --mode init
```

## 🌐 Deploy

### Render (Recomendado)

1. Conecte seu repositório GitHub ao Render
2. Configure as variáveis de ambiente no dashboard
3. O deploy será automático a cada push na branch main

### Docker

```bash
# Build da imagem
docker build -t roteiro-dispersacao-v4 .

# Executar container
docker run -p 8501:8501 --env-file .env roteiro-dispersacao-v4

# Ou usar docker-compose
docker-compose up
```

## 📚 Uso

### Interface Streamlit

Acesse `http://localhost:8501` para usar a interface web:

- Escolha entre as personas Dr. Gasnelio ou Gá
- Digite perguntas sobre roteiro de dispersão
- Visualize o histórico da conversa
- Limpe o chat quando necessário

### API Flask

A API está disponível em `http://localhost:5000`:

#### Endpoints principais:

- `GET /` - Informações da API
- `GET /api/health` - Status da aplicação
- `POST /api/chat` - Enviar mensagem para o chatbot
- `GET /api/flows` - Listar fluxos LangFlow
- `POST /api/flows` - Criar novo fluxo
- `POST /api/calculate` - Calcular parâmetros de dispersão
- `POST /api/upload` - Upload de documentos

#### Exemplo de uso:

```bash
# Chat básico
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "O que é roteiro de dispersão?",
    "persona": "Dr. Gasnelio",
    "session_id": "test-session"
  }'

# Cálculo de dispersão
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "wind_speed": 5.0,
      "temperature": 25.0,
      "emission_rate": 100.0
    }
  }'
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/ -v

# Executar testes específicos
pytest tests/test_basic.py -v

# Executar com cobertura
pytest tests/ --cov=app --cov-report=html
```

## 📁 Estrutura do Projeto

```
roteiro-de-dispersacao-v4/
├── app/
│   ├── __init__.py
│   ├── main.py              # Arquivo principal
│   ├── streamlit_app.py     # Interface Streamlit
│   ├── flask_api.py         # API Flask
│   ├── rag_system.py        # Sistema RAG
│   ├── database.py          # Conexão Astra DB
│   └── langflow_integration.py  # Integração LangFlow
├── config/
│   ├── __init__.py
│   └── settings.py          # Configurações
├── tests/
│   ├── __init__.py
│   └── test_basic.py        # Testes básicos
├── static/                  # Arquivos estáticos
├── templates/               # Templates HTML
├── data/                    # Dados e documentos
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD GitHub Actions
├── requirements.txt         # Dependências Python
├── render.yaml             # Configuração Render
├── Dockerfile              # Container Docker
├── docker-compose.yml      # Orquestração local
├── .env.example            # Exemplo de variáveis
├── .gitignore              # Arquivos ignorados
└── README.md               # Esta documentação
```

## 🔐 Variáveis de Ambiente

```bash
# Astra DB
ASTRA_DB_TOKEN=your_token_here

# OpenRouter
OPENROUTER_API_KEY=your_key_here

# LangFlow
LANGFLOW_API_KEY=your_key_here

# Configurações opcionais
DEBUG=False
DEFAULT_MODEL=anthropic/claude-3-haiku
TEMPERATURE=0.7
MAX_TOKENS=4000
```

## 👥 Personas

### Dr. Gasnelio
- **Estilo**: Técnico e preciso
- **Uso**: Consultas especializadas, cálculos, normas técnicas
- **Linguagem**: Terminologia específica da área

### Gá
- **Estilo**: Amigável e acessível
- **Uso**: Explicações básicas, conceitos gerais
- **Linguagem**: Coloquial com exemplos práticos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou problemas:

1. Abra uma issue no GitHub
2. Consulte a documentação técnica
3. Verifique os logs da aplicação

## 🔄 Changelog

### v4.0.0
- Sistema RAG completo com FAISS
- Integração LangFlow
- Duas personas (Dr. Gasnelio e Gá)
- Interface Streamlit moderna
- API Flask completa
- Deploy automático no Render
- Testes automatizados
- Documentação completa
