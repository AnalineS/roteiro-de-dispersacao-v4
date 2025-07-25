# Chatbot Roteiro de Dispensação v6 - Cursor

## 🎯 Objetivo

Esta é a versão v6 do chatbot de Roteiro de Dispensação, otimizada para funcionar com modelo AI gratuito e duas personas bem definidas: **Dr. Gasnelio** (técnico) e **Gá** (amigável).

## 🚀 Características Principais

### ✅ Duas Personas Funcionais
- **Dr. Gasnelio**: Professor especialista em farmácia clínica
  - Linguagem técnica, culta e profissional
  - Respostas baseadas em evidências científicas
  - Tom acadêmico e objetivo

- **Gá**: Amigo descontraído que explica de forma simples
  - Linguagem cotidiana e acessível
  - Explicações com emojis e analogias
  - Tom empático e bem-humorado

### ✅ Modelo AI Gratuito
- Sistema híbrido: API gratuita + regras baseadas
- Fallback automático para respostas baseadas em regras
- Sem dependência de modelos pagos

### ✅ Base de Conhecimento
- Tese de doutorado sobre roteiro de dispensação para hanseníase
- Busca contextual inteligente
- Respostas relevantes e precisas

## 🛠️ Instalação e Uso

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Rápida

1. **Clone o repositório** (já feito)
2. **Execute o script de inicialização**:
   ```bash
   start_server_v6.bat
   ```
   
   Ou manualmente:
   ```bash
   pip install -r requirements_v6.txt
   python app_v6_cursor.py
   ```

3. **Acesse o chatbot**:
   - URL: http://localhost:5000
   - Clique em "Conversar com a IA"
   - Escolha entre as duas personas

### Testes

Para verificar se tudo está funcionando:

```bash
python test_chatbot_v6.py
```

## 📁 Estrutura do Projeto

```
roteiro-de-dispersacao-v6-cursor/
├── app_v6_cursor.py          # Aplicação principal
├── requirements_v6.txt       # Dependências otimizadas
├── test_chatbot_v6.py       # Script de testes
├── start_server_v6.bat      # Script de inicialização
├── README_v6.md             # Este arquivo
├── PDFs/                    # Base de conhecimento
│   └── Roteiro de Dsispensação - Hanseníase.md
├── templates/               # Templates HTML
│   ├── index.html
│   └── tese.html
└── static/                  # Arquivos estáticos
    └── script.js
```

## 🔧 API Endpoints

### Chat
- **POST** `/api/chat`
  - Body: `{"question": "sua pergunta", "personality_id": "dr_gasnelio" | "ga"}`
  - Retorna resposta formatada da persona selecionada

### Informações
- **GET** `/api/health` - Status do servidor
- **GET** `/api/info` - Informações da API
- **GET** `/api/personas` - Lista de personas disponíveis

## 🎨 Interface

A interface web permite:
- Seleção fácil entre as duas personas
- Chat em tempo real
- Histórico de conversas
- Design responsivo
- Avatares personalizados para cada persona

## 🔍 Exemplos de Uso

### Dr. Gasnelio (Técnico)
```
Pergunta: "O que é hanseníase?"
Resposta: "A hanseníase é uma doença infecciosa crônica causada pelo Mycobacterium leprae. O roteiro de dispensação para hanseníase visa padronizar o processo de entrega de medicamentos, garantindo segurança e adesão ao tratamento."
```

### Gá (Amigável)
```
Pergunta: "O que é hanseníase?"
Resposta: "A hanseníase é uma doença de pele que precisa de tratamento especial. O roteiro que criamos ajuda a farmácia a entregar os remédios do jeito certo, explicando tudo direitinho para a pessoa que está tratando! 😊"
```

## 🚀 Deploy

### Local
```bash
python app_v6_cursor.py
```

### Render (Produção)
1. Configure o `render.yaml`
2. Defina as variáveis de ambiente
3. Deploy automático via Git

## 📊 Monitoramento

- Logs detalhados no console
- Endpoint de health check
- Métricas de confiança das respostas
- Status das personas

## 🔧 Configuração

### Variáveis de Ambiente
- `PORT`: Porta do servidor (padrão: 5000)
- `FLASK_ENV`: Ambiente (development/production)

### Personalização
- Edite `PERSONAS` em `app_v6_cursor.py` para modificar as personas
- Ajuste `keyword_responses` para adicionar novas respostas baseadas em regras

## 🐛 Troubleshooting

### Problema: Servidor não inicia
**Solução**: Verifique se o Python está instalado e execute `pip install -r requirements_v6.txt`

### Problema: Base de conhecimento não carrega
**Solução**: Verifique se o arquivo `PDFs/Roteiro de Dsispensação - Hanseníase.md` existe

### Problema: API não responde
**Solução**: Execute `python test_chatbot_v6.py` para diagnosticar

## 📈 Próximos Passos

- [ ] Integração com mais APIs gratuitas
- [ ] Expansão da base de conhecimento
- [ ] Melhorias na interface
- [ ] Deploy em produção

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do servidor
2. Execute os testes: `python test_chatbot_v6.py`
3. Consulte este README
4. Abra uma issue no repositório

---

**Versão**: 6.0.0  
**Data**: Janeiro 2025  
**Status**: ✅ Funcional 