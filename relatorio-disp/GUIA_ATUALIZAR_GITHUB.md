# Guia para Atualizar o render.yaml no GitHub

## Problema Atual
O Render está tentando executar `gunicorn app_production:app` em vez de `gunicorn app_simple:app`, porque o arquivo `render.yaml` no GitHub não está atualizado.

## Solução

### 1. Instalar o Git (se necessário)
- Baixe o Git de: https://git-scm.com/download/win
- Instale seguindo as instruções padrão
- Reinicie o PowerShell após a instalação

### 2. Abrir o PowerShell no diretório do projeto
```powershell
cd "C:\Users\Ana\Meu Drive\Imagens site Junin\gemini v2"
```

### 3. Inicializar o repositório Git (se necessário)
```powershell
git init
git remote add origin https://github.com/AnalineS/siteroteirodedispersacao.git
```

### 4. Verificar se o render.yaml está correto
O arquivo `render.yaml` deve conter:
```yaml
services:
  - type: web
    name: roteiro-dispersacao
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app_simple:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.13.4
      - key: FLASK_ENV
        value: production
```

### 5. Adicionar arquivos ao Git
```powershell
git add .
```

### 6. Fazer commit
```powershell
git commit -m "Atualizar render.yaml para usar app_simple:app"
```

### 7. Enviar para o GitHub
```powershell
git push -u origin main
```

### 8. Fazer novo deploy no Render
1. Acesse: https://dashboard.render.com
2. Vá para o serviço "roteiro-dispersacao"
3. Clique em "Manual Deploy"
4. Aguarde o build e deploy

### 9. Verificar o site
O site deve ficar disponível em: https://roteiro-dispersacao.onrender.com

## Arquivos Importantes
- ✅ `render.yaml` - Configuração do Render
- ✅ `app_simple.py` - Aplicação Flask simplificada
- ✅ `requirements.txt` - Dependências Python
- ✅ `runtime.txt` - Versão do Python

## Comandos Alternativos (se houver problemas)
Se o push falhar, tente:
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

Ou force o push (use com cuidado):
```powershell
git push -u origin main --force
``` 

---

## 1. Restaurar o `app_production.py` e arquivos necessários

Vou restaurar o arquivo `app_production.py` da última versão funcional que estava no seu projeto, mas **corrigindo qualquer vestígio de FastAPI** e garantindo que só tenha Flask.

## 2. Corrigir problemas do deploy

- O `app_production.py` deve começar assim:
  ```python
  from flask import Flask, request, jsonify, render_template_string
  from flask_cors import CORS
  # ...restante dos imports...

  app = Flask(__name__)
  CORS(app)
  # ...restante do código...
  ```

- Não pode haver nenhum `@app.get("/")` ou decorador de FastAPI.
- O `render.yaml` deve conter:
  ```yaml
  services:
    - type: web
      name: roteiro-dispersacao
      env: python
      buildCommand: pip install -r requirements.txt
      startCommand: gunicorn app_production:app
      envVars:
        - key: PYTHON_VERSION
          value: 3.13.4
        - key: FLASK_ENV
          value: production
  ```

- O `requirements.txt` deve conter todas as dependências do `app_production.py` (inclusive `gunicorn`, `flask`, `flask-cors`, `PyPDF2`, `numpy`, `requests`, `python-dotenv`, e as de IA se usadas).

---

## 3. Commit e push

Após restaurar e corrigir tudo, vou fazer commit e push para o GitHub.

---

## 4. Novo deploy

Você só precisará acionar o deploy manual no Render.

---

**Confirme para mim:**
- Você quer restaurar o `app_production.py` com todas as funcionalidades de IA e PDF, certo?
- Quer que o deploy rode usando `app_production:app` (ou seja, o app mais completo)?

Se sim, vou restaurar e corrigir tudo agora!  
Se quiser algum ajuste especial, me avise antes de eu começar. 

Esse erro geralmente está relacionado a arquivos ocultos do Windows (`desktop.ini`) que foram acidentalmente versionados ou corrompidos no repositório.

### Como resolver:

1. **Remover referências a `desktop.ini` do Git**
2. **Adicionar `desktop.ini` ao `.gitignore`**
3. **Fazer um novo commit e tentar novamente o pull/push**

Posso executar esses passos para você agora? (Isso não afeta seu código, apenas limpa arquivos desnecessários do controle de versão.) 

### Passos para resolver o problema do histórico corrompido:

1. **Renomear o repositório atual no GitHub para `siteroteirodedispersacao-old`**
2. **Criar um novo repositório chamado `siteroteirodedispersacao`**
3. **Apontar seu repositório local para o novo repositório**
4. **Fazer push de todo o projeto limpo para o novo repositório**

---

## 1. Renomear o repositório atual no GitHub

- Acesse o GitHub, vá em **Settings** do repositório atual.
- Na seção **Repository name**, renomeie para:  
  ```
  siteroteirodedispersacao-old
  ```

## 2. Criar um novo repositório

- No GitHub, clique em **New repository**.
- Nomeie como:  
  ```
  siteroteirodedispersacao
  ```
- Não adicione README, .gitignore ou licença (deixe vazio).

## 3. Apontar o repositório local para o novo

Quando terminar os passos acima, me avise!  
Assim que você criar o novo repositório, me envie o link dele ou apenas confirme que está pronto, e eu faço a troca do remoto e subo tudo limpo para o novo repositório.

Se quiser, posso te passar os comandos para você mesmo executar, ou faço tudo por aqui.  
Me avise quando o novo repositório estiver criado! 