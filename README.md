# 🏥 Roteiro de Dispensação v4 - Chatbot Inteligente

Uma aplicação moderna de chatbot baseada em IA para consultas sobre roteiro de dispensação farmacêutica, desenvolvida com tecnologias de ponta em processamento de linguagem natural.

## 🌟 Características Principais

- **🤖 IA Conversacional**: Assistente virtual Dr. Gasnelio treinado com tese de doutorado
- **🔍 Busca Semântica**: Pipeline RAG com Astra DB para respostas precisas
- **👥 Duas Personas**: Modo Professor (técnico) e Amigável (acessível)
- **🎨 Interface Moderna**: Design inspirado no site original com UX aprimorada
- **📱 Responsivo**: Funciona perfeitamente em desktop e mobile
- **☁️ Deploy Automático**: Infraestrutura no Render com CI/CD

## 🚀 Demo

**Acesso Local:** http://localhost:8502  
**Produção:** https://roteiro-dispersacao-frontend.onrender.com

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.11** - Linguagem principal
- **Astra DB** - Banco de dados vetorial
- **SentenceTransformer** - Embeddings (all-MiniLM-L6-v2)
- **OpenRouter** - API para Claude-3.5-Sonnet
- **LangChain** - Framework RAG

### Frontend
- **Streamlit** - Interface web interativa
- **CSS Customizado** - Design responsivo
- **JavaScript** - Interações dinâmicas

### Infraestrutura
- **Render** - Deploy e hospedagem
- **GitHub** - Controle de versão
- **Docker** - Containerização

## 📦 Instalação

### Pré-requisitos

- Python 3.11+
- Git
- Conta no Astra DB
- API Key do OpenRouter

### Configuração Local

```bash
# 1. Clonar o repositório
git clone https://github.com/AnalineS/roteiro-de-dispersacao-v4.git
cd roteiro-de-dispersacao-v4

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais
```

### Variáveis de Ambiente

```bash
# OpenRouter (obrigatório)
OPENROUTER_API_KEY=sk-or-v1-...

# Astra DB (obrigatório)
ASTRA_DB_TOKEN=AstraCS:...
ASTRA_DB_ENDPOINT=https://...

# Opcionais
HUGGINGFACE_API_KEY=hf_...
LANGFLOW_API_KEY=sk-...
```

### Executar Aplicação

```bash
# Modo desenvolvimento
streamlit run streamlit_app_friendly.py

# Modo produção
streamlit run streamlit_app_friendly.py --server.port 8502 --server.address 0.0.0.0
```

## 🎯 Como Usar

### 1. Escolher Persona

- **Professor**: Respostas técnicas e acadêmicas
- **Amigável**: Explicações simples com emojis

### 2. Fazer Perguntas

Exemplos de perguntas:
- "O que é roteiro de dispensação?"
- "Como aplicar o roteiro na prática?"
- "Quais foram os resultados da pesquisa?"
- "Como melhorar a adesão ao tratamento?"

### 3. Explorar Funcionalidades

- 📤 **Upload de documentos** para expandir base de conhecimento
- 📊 **Métricas em tempo real** de uso
- 🗑️ **Controles de sessão** para limpar histórico
- 💡 **Exemplos de perguntas** organizados por categoria

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   RAG Pipeline  │    │   Astra DB      │
│   Frontend      │◄──►│   (Python)      │◄──►│   (Vectors)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │    │ SentenceTransf. │    │   Knowledge     │
│   Processing    │    │   Embeddings    │    │   Base          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Estrutura do Projeto

```
roteiro-de-dispersacao-v4/
├── 📄 streamlit_app_friendly.py    # Interface principal
├── 🔧 rag_pipeline.py              # Pipeline RAG
├── 🛠️ reset_collection.py          # Utilitário Astra DB
├── 📋 requirements.txt             # Dependências
├── ⚙️ render.yaml                  # Config deploy
├── 📝 .env.example                 # Exemplo variáveis
├── 📖 README.md                    # Esta documentação
├── 📊 RELATORIO_FINAL.md          # Relatório técnico
└── 📂 docs/                       # Documentação adicional
```

## 🧪 Testes

```bash
# Testar pipeline RAG
python rag_pipeline.py

# Testar conexão Astra DB
python reset_collection.py

# Testar interface
streamlit run streamlit_app_friendly.py
```

## 🚀 Deploy

### Render (Recomendado)

1. Fork este repositório
2. Conecte sua conta Render ao GitHub
3. Crie novo Web Service
4. Configure variáveis de ambiente
5. Deploy automático!

### Docker

```bash
# Build
docker build -t roteiro-dispensacao .

# Run
docker run -p 8502:8502 --env-file .env roteiro-dispensacao
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Changelog

### v4.0 (2025-07-20)
- ✅ Interface amigável inspirada no site original
- ✅ Pipeline RAG com Astra DB e SentenceTransformer
- ✅ Duas personas (Professor/Amigável)
- ✅ Deploy automatizado no Render
- ✅ Design responsivo e acessível

### v3.0 (Anterior)
- Sistema com FAISS e LangFlow
- Interface básica Streamlit

## 🐛 Problemas Conhecidos

- Respostas podem demorar devido ao processamento de embeddings
- OpenRouter limitado por créditos disponíveis
- Upload de PDF/DOCX em desenvolvimento

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/AnalineS/roteiro-de-dispersacao-v4/issues)
- **Documentação**: [Wiki do Projeto](https://github.com/AnalineS/roteiro-de-dispersacao-v4/wiki)
- **Email**: [Contato do Projeto]

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **Dr. Gasnelio** - Autor da tese de doutorado
- **UnB** - Universidade de Brasília
- **Comunidade Open Source** - Ferramentas e bibliotecas utilizadas

---

**Desenvolvido com ❤️ para a comunidade farmacêutica**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)
[![Astra DB](https://img.shields.io/badge/Astra_DB-000000?style=for-the-badge&logo=datastax&logoColor=white)](https://astra.datastax.com/)

