# Roteiro de Dispersação v4 - Modernização do Site e Chatbot

## Descrição
Modernização do site e chatbot de Roteiro de Dispensação utilizando a metodologia PREVC. O projeto visa melhorar a usabilidade e o desempenho, adicionando um chatbot moderno com suporte a duas personas (técnica e leiga) baseado em RAG com LangFlow e Kimie K2 via OpenRouter.

## Arquitetura
- **Backend**: Python com Flask/FastAPI + Gunicorn
- **Frontend**: Streamlit para interface do chatbot
- **RAG**: LangFlow com embeddings Hugging Face
- **Banco Vetorial**: FAISS local ou Astra DB
- **LLM**: Kimie K2 Free via OpenRouter
- **Hospedagem**: Render com CI/CD automatizada
- **Base de Conhecimento**: Tese de doutorado sobre roteiro de dispensação

## Personas do Chatbot
1. **Dr. Gasnelio (Técnica)**: Linguagem culta, profissional, para público especializado
2. **Gá (Leiga)**: Linguagem simples, empática, para público geral

## Estrutura do Projeto
```
roteiro-de-dispersacao-v4/
├── backend/          # Aplicação Python (Flask/FastAPI)
├── frontend/         # Interface Streamlit
├── langflow/         # Configurações e fluxos LangFlow
├── data/            # Base de conhecimento (tese)
├── docs/            # Documentação
├── tests/           # Testes automatizados
├── render.yaml      # Configuração CI/CD Render
├── requirements.txt # Dependências Python
└── README.md       # Este arquivo
```

## Instalação Local

### Pré-requisitos
- Python 3.9+
- Git

### Configuração
1. Clone o repositório:
```bash
git clone https://github.com/AnalineS/roteiro-de-dispersacao-v4.git
cd roteiro-de-dispersacao-v4
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate   # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

5. Execute a aplicação:
```bash
# Backend
cd backend
python app.py

# Frontend (em outro terminal)
cd frontend
streamlit run chatbot.py
```

## Variáveis de Ambiente
- `OPENROUTER_API_KEY`: Chave da API OpenRouter
- `ASTRA_DB_TOKEN`: Token do Astra DB (opcional)
- `ASTRA_DB_ENDPOINT`: Endpoint do Astra DB (opcional)
- `HUGGINGFACE_API_KEY`: Chave da API Hugging Face

## Deploy no Render
O projeto está configurado para deploy automático no Render via `render.yaml`. O deploy é acionado automaticamente a cada push na branch `main`.

## Metodologia PREVC
- **P**lanejamento: Definição de objetivos, personas e arquitetura
- **R**evisão: Análise do site atual e tecnologias
- **E**xecução: Implementação do sistema RAG e chatbot
- **V**alidação: Testes de funcionalidade e usabilidade
- **C**onfirmação: Deploy e verificação em produção

## Contribuição
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Contato
- Repositório: https://github.com/AnalineS/roteiro-de-dispersacao-v4
- Issues: https://github.com/AnalineS/roteiro-de-dispersacao-v4/issues

