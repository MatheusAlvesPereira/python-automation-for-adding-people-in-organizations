from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORGANIZATION = os.getenv('ORGANIZATION')

@app.route('/')
def home():
    return "Hello world está funcionando meu servidor"

@app.route("/webhook", methods=['POST'])
def github_webhook():
    data = request.json
    if request.headers.get('X-GitHub-Event') == 'star':
        sender = data['sender']
        user = sender['login']
        send_invite(user)
        return jsonify({"message": f"Convite enviado para {user}"}), 200

    return jsonify({"message": "Evento não é uma star"}), 400

def get_user_id(username):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("id")
    else:
        print(f"Erro ao obter ID do usuário {username}: {response.status_code} - {response.text}")
        return None

def send_invite(user):
    user_id = get_user_id(user)
    if user_id is None:
        print(f"Falha ao encontrar ID do usuário {user}")
        return

    url = f"https://api.github.com/orgs/{ORGANIZATION}/invitations"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"invitee_id": user_id
    
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Convite enviado para {user}")
    else:
        print(f"Falha ao enviar convite para {user}: {response.status_code} - {response.text}")

if __name__ == '__main__':
    app.run(port=5000)