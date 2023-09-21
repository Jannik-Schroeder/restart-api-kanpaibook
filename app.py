import os
from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "default_api_key") 


PRIVATE_KEY_PATH = os.environ.get("PRIVATE_KEY_PATH", "/root/.ssh/id_rsa")



SERVERS = {
    "kb-web-prod-1": "10.0.0.d120",
    "kb-web-prod-2": "10.0.0.122",
    "kb-dash-prod-1": "10.0.0.124",
    "kb-dash-prod-2": "10.0.0.126",
    "kb-api-prod-1": "10.0.0.128",
    "kb-api-prod-2": "10.0.0.130",
    "kb-webhook-handler": "10.0.0.132",
    "kb-web-dev": "10.0.0.134",
    "kb-dash-dev": "10.0.0.136",
    "kb-api-dev": "10.0.0.138"
}


def execute_ssh_command(host, command):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username='root', key_filename=PRIVATE_KEY_PATH)
        
        stdin, stdout, stderr = client.exec_command(command)
        result = stdout.read().decode('utf-8')
        client.close()
        return result
    except Exception as e:
        return f"Error: {e}"

@app.route('/update/<server_name>', methods=['POST'])
def webhook_handler(server_name):
    api_key = request.headers.get('API-Key')

    if not api_key or api_key != API_KEY:
        return jsonify(error="Invalid API Key"), 401

    if server_name not in SERVERS:
        return jsonify(error="Invalid server name"), 400

    output = execute_ssh_command(SERVERS[server_name], 'cd /root/ && docker-compose pull && docker-compose up -d && docker image prune -f &&')
    return jsonify(output=output)

if __name__ == '__main__':
    app.run(debug=True)
