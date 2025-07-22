## ✅ Checklist de Modularização

### 1. Estrutura de Pastas
- [x] Separar claramente backend (`app/`), frontend (`frontend/`), testes (`tests/`) e scripts utilitários (`scripts/`).
- [x] Criar subpastas para serviços/utilitários dentro de `app/services/`.

### 2. Centralização de Funções Utilitárias
- [x] Centralizar funções de chunking de texto (`chunk_text`).
- [x] Centralizar funções de extração de PDF (`extract_text_from_pdf`).
- [x] Centralizar funções de expansão de sinônimos (`expand_query_with_synonyms`).
- [x] Centralizar outras funções utilitárias duplicadas (ex: pré-processamento, pós-processamento, validação).

### 3. Remoção de Duplicidade
- [x] Remover implementações duplicadas de funções utilitárias nos arquivos de origem.
- [x] Remover/arquivar versões antigas de apps (`app_simple.py`, `app_production.py`, `app_optimized.py`, `app.py`, `chatbot_dispersacao.py`).
- [x] Remover/arquivar scripts de debug/teste/exemplo (`debug_site.py`, `debug_search.py`, `quick_test.py`, `test_*.py`, `demo_melhorias.py`, `pdf_analyzer.py`, `install_and_check.py`, etc).
- [x] Remover/arquivar scripts de deploy/build antigos (`deploy_*.bat`, `deploy_*.sh`, `deploy_*.ps1`, `deploy_*.zip`, etc).
- [x] Remover arquivos de configuração/temporários não utilizados (`optimized_config.json`, `pdf_analysis.json`, `.venv/`, `temp_check/`, arquivos vazios/rascunhos).
- [x] Consolidar documentação e guias antigos em um README principal.

### 4. Importação Correta
- [x] Garantir que todos os módulos e apps importam as funções utilitárias centralizadas.
- [x] Atualizar exemplos e notebooks (se houver) para usar as funções centralizadas.

### 5. Documentação
- [x] Adicionar docstrings em todas as funções, métodos e classes.
- [x] Comentar lógicas complexas ou decisões de design.
- [x] Atualizar o README.md com a nova estrutura e instruções de uso.

### 6. Testes
- [ ] Garantir que os testes utilizam as funções centralizadas.
- [ ] Adicionar testes para os utilitários centralizados, se ainda não existirem.

### 7. Revisão de Dependências
- [x] Limpar o `requirements.txt` para conter apenas o necessário.
- [x] Remover dependências não utilizadas dos scripts e módulos.

### 8. Padronização de Estilo
- [x] Rodar um linter (ex: flake8, black) para padronizar o estilo do código.
- [x] Corrigir warnings e erros de estilo.

### 9. Realize os commits, git pull e faça os deploys do frontend/backend no render
---

> Marque cada item conforme for concluindo. Priorize a centralização e remoção de duplicidade antes de avançar para testes e documentação. Ao final, rode todos os testes para garantir que a modularização não quebrou nenhum fluxo. 