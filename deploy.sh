#!/bin/bash

# Script de Deploy Automatizado
# Chatbot Tese Hanseníase

echo "🚀 Iniciando deploy do Chatbot Tese Hanseníase..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para imprimir com cores
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se o PDF existe
if [ ! -f "Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf" ]; then
    print_error "PDF da tese não encontrado!"
    print_warning "Certifique-se de que o arquivo 'Roteiro-de-Dsispensacao-Hanseniase-F.docx.pdf' está na raiz do projeto."
    exit 1
fi

print_status "PDF encontrado ✓"

# Verificar se as dependências estão instaladas
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 não encontrado!"
    exit 1
fi

print_status "Python 3 encontrado ✓"

# Instalar dependências
print_status "Instalando dependências..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_status "Dependências instaladas ✓"
else
    print_error "Erro ao instalar dependências!"
    exit 1
fi

# Testar a aplicação localmente
print_status "Testando aplicação localmente..."
python3 functions/api.py &
APP_PID=$!

# Aguardar o servidor iniciar
sleep 5

# Executar testes
print_status "Executando testes..."
python3 test_api.py

# Parar o servidor
kill $APP_PID

print_status "Testes concluídos ✓"

# Opções de deploy
echo ""
echo "📦 Escolha uma opção de deploy:"
echo "1) Heroku"
echo "2) Railway"
echo "3) Render"
echo "4) Local apenas"
echo "5) Sair"

read -p "Digite sua escolha (1-5): " choice

case $choice in
    1)
        print_status "Deploy no Heroku..."
        if command -v heroku &> /dev/null; then
            heroku create
            git add .
            git commit -m "Deploy chatbot tese hanseníase"
            git push heroku main
            print_status "Deploy no Heroku concluído!"
        else
            print_error "Heroku CLI não encontrado. Instale em: https://devcenter.heroku.com/articles/heroku-cli"
        fi
        ;;
    2)
        print_status "Deploy no Railway..."
        if command -v railway &> /dev/null; then
            railway login
            railway init
            railway up
            print_status "Deploy no Railway concluído!"
        else
            print_error "Railway CLI não encontrado. Instale com: npm install -g @railway/cli"
        fi
        ;;
    3)
        print_status "Deploy no Render..."
        print_warning "Para deploy no Render:"
        echo "1. Acesse https://render.com"
        echo "2. Conecte seu repositório"
        echo "3. Configure como Web Service"
        echo "4. Build Command: pip install -r requirements.txt"
        echo "5. Start Command: gunicorn app:app"
        ;;
    4)
        print_status "Executando localmente..."
        print_status "Acesse: http://localhost:5000"
        python3 functions/api.py
        ;;
    5)
        print_status "Saindo..."
        exit 0
        ;;
    *)
        print_error "Opção inválida!"
        exit 1
        ;;
esac

print_status "Deploy concluído! 🎉"
print_status "Lembre-se de atualizar a URL da API no frontend se necessário." 