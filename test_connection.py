
from flask import Flask

app = Flask(__name__)

@app.route('/test')
def test():
    return {"status": "ok", "message": "Conexão funcionando"}

if __name__ == '__main__':
    print("Iniciando servidor de teste...")
    app.run(debug=True, port=5001)
