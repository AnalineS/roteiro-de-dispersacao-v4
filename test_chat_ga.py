import requests

BASE_URL = "http://localhost:5000"
question = "O que é hanseníase?"
payload = {
    "question": question,
    "personality_id": "ga"
}

print(f"Testando persona 'Gá' com a pergunta: {question}")
response = requests.post(f"{BASE_URL}/api/chat", json=payload)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print("Resposta:", data["answer"])
    print("Confiança:", data.get("confidence"))
else:
    print("Erro na resposta:", response.text) 