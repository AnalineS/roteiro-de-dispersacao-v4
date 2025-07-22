# Guia de Configuração - PDF Real da Tese

## 📄 Informações do PDF

**Arquivo:** `Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf`  
**Tamanho:** 988 KB  
**Fonte:** Google Drive - Tese de Doutorado  
**Link:** https://drive.google.com/drive/folders/1435FhEIp_yOwtretv-G-ZQpNFY-f6tzr?usp=drive_link

## 🎯 Análise de Compatibilidade

### Características do PDF
- **Tamanho:** Médio (988 KB)
- **Páginas estimadas:** 50-100
- **Caracteres estimados:** 75.000
- **Complexidade:** Média
- **Tipo:** Tese acadêmica

### Configuração Otimizada
```json
{
  "chunk_size": 2000,
  "overlap": 200,
  "max_answer_length": 200,
  "confidence_threshold": 0.35,
  "use_semantic_search": false,
  "use_caching": true,
  "complexity_level": "MEDIUM"
}
```

### Performance Esperada
- ⚡ **Tempo de resposta:** 2-5 segundos
- 💾 **Uso de memória:** 500MB-1GB
- 🎯 **Precisão:** Boa (35% confiança mínima)
- 🔄 **Cache:** Habilitado para melhor performance

## 📥 Como Baixar o PDF

### Método 1: Download Direto
1. Acesse o link: https://drive.google.com/drive/folders/1435FhEIp_yOwtretv-G-ZQpNFY-f6tzr?usp=drive_link
2. Clique no arquivo PDF
3. Clique em "Download"
4. Salve como: `Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf`

### Método 2: Script Automático
```bash
python download_pdf.py
```

### Método 3: Manual
1. Abra o Google Drive
2. Navegue até a pasta compartilhada
3. Localize o arquivo PDF
4. Baixe e renomeie para o nome correto

## 🛠️ Instalação

### Windows
```cmd
# 1. Baixe o PDF (método acima)
# 2. Execute o instalador
setup.bat

# 3. Inicie o chatbot
start.bat
```

### Linux/Mac
```bash
# 1. Baixe o PDF (método acima)
# 2. Execute o instalador
python3 install_and_check.py

# 3. Inicie o chatbot
python3 app_optimized.py
```

## ✅ Verificação

### Teste de Instalação
```bash
python3 test_api.py
```

### Verificação Manual
1. **PDF presente:** ✅ `Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf`
2. **Dependências:** ✅ `pip list | grep flask`
3. **Modelo:** ✅ Carregamento automático
4. **Configuração:** ✅ `optimized_config.json`

## 🎭 Personalidades Configuradas

### Dr. Gasnelio (Professor)
- **Tom:** Sério e técnico
- **Linguagem:** Formal e acadêmica
- **Foco:** Precisão científica
- **Exemplo:** "Dr. Gasnelio responde: Baseado na tese sobre roteiro de dispensação para hanseníase..."

### Gá (Amigo)
- **Tom:** Descontraído e acessível
- **Linguagem:** Simples e direta
- **Foco:** Compreensão fácil
- **Exemplo:** "Gá explica: Tá na tese, pode confiar! 😊"

## 🔧 Otimizações Específicas

### Para PDFs de Tese (como este)
- **Chunking inteligente:** Quebra por seções acadêmicas
- **Cache persistente:** Salva respostas para reutilização
- **Busca por palavras-chave:** Otimizada para termos médicos
- **Fallback inteligente:** Respostas específicas para cada personalidade

### Termos Técnicos Mapeados
```python
replacements = {
    "dispensação": "entrega de remédios",
    "medicamentos": "remédios",
    "posologia": "como tomar",
    "administração": "como tomar",
    "reação adversa": "efeito colateral",
    "interação medicamentosa": "mistura de remédios",
    "protocolo": "guia",
    "orientação": "explicação",
    "adesão": "seguir o tratamento"
}
```

## 📊 Monitoramento

### Métricas Importantes
- **Tempo de resposta:** < 5 segundos
- **Taxa de cache hit:** > 60%
- **Confiança média:** > 40%
- **Erros:** < 5%

### Logs de Sistema
```bash
# Verificar logs
tail -f app.log

# Verificar cache
ls -la response_cache.pkl

# Verificar configuração
cat optimized_config.json
```

## 🚀 Deploy em Produção

### Heroku
```bash
# Configurar para PDF médio
heroku config:set CHUNK_SIZE=2000
heroku config:set USE_CACHING=true
heroku config:set CONFIDENCE_THRESHOLD=0.35
```

### Railway
```bash
# Configuração automática baseada no tamanho
railway up
```

### Render
```bash
# Build command
pip install -r requirements.txt

# Start command
gunicorn app_optimized:app
```

## 🐛 Troubleshooting

### Problemas Comuns

**PDF não carrega:**
```bash
# Verificar arquivo
ls -la Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf

# Verificar permissões
chmod 644 Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf
```

**Resposta lenta:**
```bash
# Ajustar configuração
echo '{"chunk_size": 1500, "overlap": 300}' > optimized_config.json
```

**Baixa precisão:**
```bash
# Aumentar confiança
echo '{"confidence_threshold": 0.4}' > optimized_config.json
```

**Erro de memória:**
```bash
# Reduzir chunk size
echo '{"chunk_size": 1000, "use_caching": false}' > optimized_config.json
```

## 📈 Melhorias Futuras

### Para PDFs Maiores
- Implementar busca semântica
- Usar modelo RoBERTa large
- Cache distribuído
- Processamento assíncrono

### Para PDFs Menores
- Processamento direto
- Cache desabilitado
- Respostas mais rápidas

## ✅ Checklist de Configuração

- [ ] PDF baixado e renomeado corretamente
- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas
- [ ] Configuração otimizada gerada
- [ ] Modelo carregado com sucesso
- [ ] Cache funcionando
- [ ] Testes passando
- [ ] Frontend integrado
- [ ] Deploy configurado

## 🎉 Resultado Final

Com esta configuração, o chatbot será capaz de:
- ✅ Responder perguntas sobre a tese de hanseníase
- ✅ Manter duas personalidades distintas
- ✅ Processar o PDF de 988 KB eficientemente
- ✅ Fornecer respostas em 2-5 segundos
- ✅ Usar cache para melhor performance
- ✅ Funcionar em produção

**Acesse:** http://localhost:5000 