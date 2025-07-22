#!/bin/bash

echo "🚀 Iniciando deploy para Netlify..."

# Verificar se o Netlify CLI está instalado
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI não encontrado. Instalando..."
    npm install -g netlify-cli
fi

# Verificar se estamos logados no Netlify
if ! netlify status &> /dev/null; then
    echo "🔐 Faça login no Netlify..."
    netlify login
fi

# Criar pasta functions se não existir
mkdir -p functions

# Criar função serverless para o backend
cat > functions/api.js << 'EOF'
const { spawn } = require('child_process');
const path = require('path');

exports.handler = async (event, context) => {
    // Configurar CORS
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    };

    // Responder a requisições OPTIONS (preflight)
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: ''
        };
    }

    try {
        // Executar o backend Python
        const pythonProcess = spawn('python', ['app_production.py'], {
            cwd: path.join(__dirname, '..'),
            env: { ...process.env, PYTHONPATH: path.join(__dirname, '..') }
        });

        // Configurar timeout
        const timeout = setTimeout(() => {
            pythonProcess.kill();
        }, 30000); // 30 segundos

        return new Promise((resolve, reject) => {
            let output = '';
            let error = '';

            pythonProcess.stdout.on('data', (data) => {
                output += data.toString();
            });

            pythonProcess.stderr.on('data', (data) => {
                error += data.toString();
            });

            pythonProcess.on('close', (code) => {
                clearTimeout(timeout);
                
                if (code !== 0) {
                    console.error('Erro no Python:', error);
                    resolve({
                        statusCode: 500,
                        headers,
                        body: JSON.stringify({ error: 'Erro interno do servidor' })
                    });
                    return;
                }

                // Processar resposta do Python
                try {
                    const response = JSON.parse(output);
                    resolve({
                        statusCode: 200,
                        headers,
                        body: JSON.stringify(response)
                    });
                } catch (e) {
                    resolve({
                        statusCode: 500,
                        headers,
                        body: JSON.stringify({ error: 'Erro ao processar resposta' })
                    });
                }
            });
        });

    } catch (error) {
        console.error('Erro na função:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Erro interno do servidor' })
        };
    }
};
EOF

# Criar package.json para as funções
cat > functions/package.json << 'EOF'
{
  "name": "hanseniase-chatbot-functions",
  "version": "1.0.0",
  "description": "Serverless functions para o chatbot de hanseníase",
  "main": "api.js",
  "dependencies": {},
  "devDependencies": {},
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": ["netlify", "serverless", "chatbot", "hanseniase"],
  "author": "Nélio Gomes",
  "license": "MIT"
}
EOF

# Criar arquivo de configuração do Netlify
cat > netlify.toml << 'EOF'
[build]
  publish = "."
  command = "pip install -r requirements.txt"
  functions = "functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/api/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  PYTHON_VERSION = "3.9"
  NODE_VERSION = "18"

[functions]
  directory = "functions"
  node_bundler = "esbuild"

[[headers]]
  for = "/api/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Access-Control-Allow-Methods = "GET, POST, OPTIONS"
    Access-Control-Allow-Headers = "Content-Type"
EOF

# Verificar se o PDF está presente
if [ ! -f "PDFs/hanseniase.pdf" ]; then
    echo "⚠️  AVISO: PDF de hanseníase não encontrado em PDFs/hanseniase.pdf"
    echo "O chatbot funcionará apenas com respostas padrão"
fi

# Fazer deploy
echo "📤 Fazendo deploy para Netlify..."
netlify deploy --prod

echo "✅ Deploy concluído!"
echo "🌐 Seu chatbot está disponível em: https://roteiro-de-dispersacao.netlify.app" 