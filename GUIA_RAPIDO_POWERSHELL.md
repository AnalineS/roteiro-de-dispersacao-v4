# 🚀 GUIA RÁPIDO - POWERSHELL

## ✅ Configuração Rápida

### 1. Configurar Langflow
```powershell
# Execute o script de configuração
.\setup_langflow.ps1
```

### 2. Iniciar Langflow
```powershell
# Em um terminal separado
.\start_langflow.ps1
```

### 3. Iniciar Chatbot
```powershell
# Em outro terminal
python app_simple_langflow.py
```

## 🎯 URLs Importantes

- **Chatbot**: http://localhost:5000
- **Langflow**: http://localhost:7860
- **Status**: http://localhost:5000/api/system-status

## 🔧 Configuração Automática

O script `setup_langflow.ps1` faz automaticamente:

1. ✅ Verifica Python
2. ✅ Corrige versão do NumPy
3. ✅ Detecta Langflow em `C:\Program Files\Langflow`
4. ✅ Configura variáveis de ambiente
5. ✅ Instala dependências
6. ✅ Cria arquivo `.env` com API key

## 🚨 Solução de Problemas

### Erro: "Execution Policy"
```powershell
# Permitir execução de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "Langflow não encontrado"
```powershell
# Verificar se existe
Test-Path "C:\Program Files\Langflow\langflow.exe"
```

### Erro: "Porta ocupada"
```powershell
# Verificar processos na porta 7860
netstat -ano | findstr :7860
```

## 📊 Verificar Status

### Teste da Integração
```powershell
python test_langflow_integration.py
```

### Status do Sistema
```powershell
# Via API
Invoke-RestMethod -Uri "http://localhost:5000/api/system-status"
```

## 🎉 Próximos Passos

1. **Configure fluxos no Langflow**: http://localhost:7860
2. **Teste o chatbot**: http://localhost:5000
3. **Monitore logs**: Verifique o terminal do chatbot

---

**💡 Dica**: Use `.\` antes dos nomes dos scripts no PowerShell! 