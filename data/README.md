# Base de Conhecimento - Tese de Doutorado

Esta pasta contém a base de conhecimento do chatbot, baseada na tese de doutorado sobre roteiro de dispensação para hanseníase.

## Como Adicionar a Tese

1. **Formato PDF (Recomendado):**
   - Coloque o arquivo PDF da tese nesta pasta
   - Nome sugerido: `tese_roteiro_dispensacao.pdf`

2. **Formato Markdown (Alternativo):**
   - Se a tese estiver em formato Markdown, coloque o arquivo `.md` aqui
   - Nome sugerido: `tese_roteiro_dispensacao.md`

## Processamento da Base de Conhecimento

Após adicionar a tese, execute o script de processamento:

```bash
cd scripts
python build_knowledge_base.py
```

Este script irá:
1. Ler todos os arquivos PDF e Markdown desta pasta
2. Dividir o conteúdo em chunks menores
3. Gerar embeddings usando Sentence Transformers
4. Criar um índice FAISS para busca semântica
5. Salvar o índice para uso pelo chatbot

## Arquivos Gerados

Após o processamento, serão criados:
- `faiss_index.bin` - Índice FAISS para busca vetorial
- `documents.pkl` - Chunks de texto processados

## Estrutura Esperada da Tese

A tese deve conter informações sobre:
- Roteiro de dispensação para hanseníase
- Práticas de farmácia clínica
- Protocolos de tratamento
- Orientações para profissionais de saúde
- Informações para pacientes e familiares

## Formatos Suportados

- ✅ PDF (.pdf)
- ✅ Markdown (.md)
- ❌ Word (.docx) - não suportado diretamente
- ❌ Texto simples (.txt) - funciona mas sem formatação

## Troubleshooting

### Erro ao processar PDF
- Verifique se o PDF não está corrompido
- Certifique-se de que o PDF contém texto (não apenas imagens)
- PDFs escaneados podem precisar de OCR primeiro

### Chunks muito pequenos
- Ajuste os parâmetros `chunk_size` e `chunk_overlap` no script
- Valores padrão: chunk_size=1000, chunk_overlap=200

### Memória insuficiente
- Para teses muito grandes, considere processar em partes
- Monitore o uso de RAM durante o processamento

## Exemplo de Uso

```bash
# 1. Adicione a tese nesta pasta
cp ~/Downloads/tese_doutorado.pdf ./data/

# 2. Execute o processamento
python scripts/build_knowledge_base.py

# 3. Verifique se os arquivos foram criados
ls -la data/
# Deve mostrar: faiss_index.bin e documents.pkl
```

