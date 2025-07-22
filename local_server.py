from flask import Flask, request
from functions.api import handler

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health():
    event = {
        'httpMethod': 'GET',
        'path': '/api/health',
        'headers': dict(request.headers),
        'body': None
    }
    result = handler(event, None)
    return (result['body'], result['statusCode'], result['headers'])

@app.route('/api/chat', methods=['POST'])
def chat():
    event = {
        'httpMethod': 'POST',
        'path': '/api/chat',
        'headers': dict(request.headers),
        'body': request.data.decode('utf-8')
    }
    result = handler(event, None)
    return (result['body'], result['statusCode'], result['headers'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 