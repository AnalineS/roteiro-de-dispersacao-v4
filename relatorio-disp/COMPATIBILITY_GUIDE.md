# Guia de Compatibilidade - Chatbot Tese Hanseníase

## 📊 Análise de Compatibilidade por Tamanho de PDF

### 🟢 PDFs Pequenos (< 50.000 caracteres)
**Características:**
- Até 20-30 páginas
- Texto simples e direto
- Poucos termos técnicos

**Configuração Recomendada:**
```json
{
  "chunk_size": 2000,
  "overlap": 200,
  "max_answer_length": 200,
  "confidence_threshold": 0.3,
  "use_semantic_search": false,
  "use_caching": false,
  "complexity_level": "LOW"
}
```

**Performance Esperada:**
- ⚡ Resposta rápida (< 2 segundos)
- 🎯 Alta precisão
- 💾 Baixo uso de memória
- 🔄 Processamento direto

---

### 🟡 PDFs Médios (50.000 - 100.000 caracteres)
**Características:**
- 30-80 páginas
- Texto moderadamente complexo
- Alguns termos técnicos

**Configuração Recomendada:**
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

**Performance Esperada:**
- ⚡ Resposta moderada (2-5 segundos)
- 🎯 Boa precisão
- 💾 Uso moderado de memória
- 🔄 Chunking básico

---

### 🔴 PDFs Grandes (> 100.000 caracteres)
**Características:**
- 80+ páginas
- Texto muito complexo
- Muitos termos técnicos
- Estrutura complexa

**Configuração Recomendada:**
```json
{
  "chunk_size": 1500,
  "overlap": 300,
  "max_answer_length": 150,
  "confidence_threshold": 0.4,
  "use_semantic_search": true,
  "use_caching": true,
  "complexity_level": "HIGH"
}
```

**Performance Esperada:**
- ⚡ Resposta lenta (5-10 segundos)
- 🎯 Precisão moderada
- 💾 Alto uso de memória
- 🔄 Chunking avançado + cache

---

## 🧠 Análise de Complexidade

### Fatores que Afetam a Complexidade

1. **Tamanho do Texto**
   - Caracteres totais
   - Número de páginas
   - Densidade de texto

2. **Complexidade Linguística**
   - Palavras por frase
   - Vocabulário técnico
   - Estrutura de frases

3. **Conteúdo Técnico**
   - Termos médicos
   - Procedimentos
   - Protocolos

4. **Estrutura do Documento**
   - Seções e subseções
   - Tabelas e gráficos
   - Referências cruzadas

---

## ⚙️ Otimizações Automáticas

### Sistema de Chunking Inteligente
```python
def create_optimized_chunks(text, complexity_level):
    if complexity_level == "LOW":
        return simple_chunking(text, 2000)
    elif complexity_level == "MEDIUM":
        return smart_chunking(text, 2000, 200)
    else:  # HIGH
        return advanced_chunking(text, 1500, 300)
```

### Cache Inteligente
- **PDFs Pequenos**: Sem cache (desnecessário)
- **PDFs Médios**: Cache básico
- **PDFs Grandes**: Cache avançado + persistência

### Busca Semântica
- **PDFs Pequenos**: Busca por palavras-chave
- **PDFs Médios**: Busca híbrida
- **PDFs Grandes**: Busca semântica completa

---

## 📈 Métricas de Performance

### Tempo de Resposta
| Tamanho PDF | Tempo Esperado | Otimização |
|-------------|----------------|------------|
| Pequeno     | < 2s          | Direto     |
| Médio       | 2-5s          | Cache      |
| Grande      | 5-10s         | Avançado   |

### Precisão
| Complexidade | Confiança Mínima | Estratégia |
|--------------|------------------|------------|
| Baixa        | 30%             | Direta     |
| Média        | 35%             | Chunking   |
| Alta         | 40%             | Semântica  |

### Uso de Memória
| Tamanho PDF | RAM Estimada | Otimização |
|-------------|--------------|------------|
| Pequeno     | < 500MB      | Mínima     |
| Médio       | 500MB-1GB    | Moderada   |
| Grande      | 1GB-2GB      | Máxima     |

---

## 🔧 Configurações Específicas por Tipo

### Tese Acadêmica
```json
{
  "chunk_size": 1800,
  "overlap": 250,
  "max_answer_length": 180,
  "confidence_threshold": 0.4,
  "use_semantic_search": true,
  "use_caching": true,
  "technical_terms": ["metodologia", "resultados", "discussão", "conclusão"]
}
```

### Manual Técnico
```json
{
  "chunk_size": 1600,
  "overlap": 300,
  "max_answer_length": 150,
  "confidence_threshold": 0.45,
  "use_semantic_search": true,
  "use_caching": true,
  "technical_terms": ["procedimento", "protocolo", "especificação", "requisito"]
}
```

### Documento Clínico
```json
{
  "chunk_size": 2000,
  "overlap": 200,
  "max_answer_length": 200,
  "confidence_threshold": 0.35,
  "use_semantic_search": false,
  "use_caching": true,
  "technical_terms": ["diagnóstico", "tratamento", "medicação", "posologia"]
}
```

---

## 🚀 Recomendações de Deploy

### Para PDFs Pequenos
- **Servidor**: Básico (512MB RAM)
- **Modelo**: RoBERTa base
- **Cache**: Desabilitado
- **Monitoramento**: Básico

### Para PDFs Médios
- **Servidor**: Padrão (1GB RAM)
- **Modelo**: RoBERTa base
- **Cache**: Habilitado
- **Monitoramento**: Moderado

### Para PDFs Grandes
- **Servidor**: Avançado (2GB+ RAM)
- **Modelo**: RoBERTa large (se disponível)
- **Cache**: Persistente
- **Monitoramento**: Avançado

---

## 🛠️ Scripts de Análise

### Análise Automática
```bash
python pdf_analyzer.py seu_arquivo.pdf
```

### Teste de Performance
```bash
python test_api.py
```

### Otimização Automática
```bash
python optimize_config.py
```

---

## 📊 Monitoramento

### Métricas Importantes
- Tempo de resposta
- Taxa de cache hit
- Confiança média
- Uso de memória
- Erros de processamento

### Alertas Recomendados
- Resposta > 10 segundos
- Confiança < 20%
- Erro de memória
- Falha no modelo

---

## 🔄 Atualizações e Manutenção

### Para PDFs Pequenos
- Atualização mensal
- Backup simples
- Monitoramento básico

### Para PDFs Médios
- Atualização quinzenal
- Backup incremental
- Monitoramento moderado

### Para PDFs Grandes
- Atualização semanal
- Backup completo
- Monitoramento avançado

---

## 💡 Dicas de Otimização

1. **Sempre analise o PDF antes do deploy**
2. **Use o script de análise automática**
3. **Ajuste configurações baseado nos resultados**
4. **Monitore performance em produção**
5. **Atualize cache regularmente**
6. **Considere usar modelos mais avançados para PDFs muito grandes**

---

## 🆘 Troubleshooting

### Problemas Comuns

**Resposta muito lenta:**
- Reduza chunk_size
- Aumente overlap
- Habilite cache

**Baixa precisão:**
- Aumente confidence_threshold
- Habilite semantic_search
- Ajuste chunk_size

**Erro de memória:**
- Reduza chunk_size
- Desabilite cache
- Use modelo menor

**PDF não carrega:**
- Verifique formato
- Teste extração
- Verifique permissões 