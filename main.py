from main import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORGANIZATION = os.getenv('ORGANIZATION')

@app.route("/webhook", method=['POST'])
def github_webhook():
    data = request.json
    if request.headers.get('X-GitHub-Event') == 'star':
        sender = data['sender']
        user = sender['login']
        send_invite(user)
        return jsonify({"message": f"Convite enviado para {user}"}), 200

    return jsonify({"message": "Evento não é uma estrela"}), 400

def send_invite(user):
    url = f"https://api.github.com/orgs/{ORGANIZATION}/invitations"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"invitee_id": user}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Convite enviado para {user}")
    else:
        print(f"Falha ao enviar convite para {user}: {response.status_code} - {response.text}")

if __name__ == '__main__':
    app.run(port=5000)