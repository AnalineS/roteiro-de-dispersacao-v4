# TODO - Correções para Deploy no Render

## Problemas Identificados
- [x] Atualizar versão do astrapy de 0.7.0 para ≥ 1.0 (DataAPIClient não existe na 0.7.0)
- [x] Verificar imports absolutos no backend/rag_service_openai.py
- [x] Verificar se todas as dependências estão corretas
- [x] Testar conexão com Astra DB localmente
- [x] Verificar configuração do gunicorn
- [x] Validar estrutura de templates do Flask

## Correções a Implementar
- [x] Atualizar requirements_light.txt com astrapy>=1.0.0
- [x] Corrigir imports no rag_service_openai.py se necessário
- [x] Verificar se o arquivo rag_service_openai.py na raiz está vazio (possível duplicação)
- [x] Testar aplicação localmente antes do deploy
- [ ] Configurar variáveis de ambiente necessárias

## Deploy no Render
- [ ] Fazer push das correções para o repositório
- [ ] Configurar serviço no Render
- [ ] Configurar variáveis de ambiente no Render
- [ ] Testar deploy e health check
- [ ] Verificar logs de erro

