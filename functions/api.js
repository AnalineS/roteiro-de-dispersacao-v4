const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  // Configurar CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json'
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
    // URL do backend Render (substitua pela sua URL real)
    const RENDER_BACKEND_URL = process.env.RENDER_BACKEND_URL || 'https://roteiro-dispersacao-chatbot.onrender.com';
    
    // Roteamento baseado no path
    const path = event.path.replace('/.netlify/functions/api', '');
    
    if (path === '/chat' && event.httpMethod === 'POST') {
      // Proxy para o endpoint de chat
      const response = await fetch(`${RENDER_BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: event.body
      });
      
      const data = await response.json();
      
      return {
        statusCode: response.status,
        headers,
        body: JSON.stringify(data)
      };
    }
    
    if (path === '/health' && event.httpMethod === 'GET') {
      // Health check
      const response = await fetch(`${RENDER_BACKEND_URL}/api/health`);
      const data = await response.json();
      
      return {
        statusCode: response.status,
        headers,
        body: JSON.stringify(data)
      };
    }
    
    if (path === '/info' && event.httpMethod === 'GET') {
      // Info endpoint
      const response = await fetch(`${RENDER_BACKEND_URL}/api/info`);
      const data = await response.json();
      
      return {
        statusCode: response.status,
        headers,
        body: JSON.stringify(data)
      };
    }
    
    // Endpoint padrão
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        message: 'Netlify Function funcionando!',
        available_endpoints: ['/chat', '/health', '/info'],
        backend_url: RENDER_BACKEND_URL
      })
    };
    
  } catch (error) {
    console.error('Erro na função Netlify:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Erro interno do servidor',
        message: error.message
      })
    };
  }
}; 