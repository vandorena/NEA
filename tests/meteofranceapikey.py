import requests
import base64

client_id = 'eyJ4NXQiOiJZV0kxTTJZNE1qWTNOemsyTkRZeU5XTTRPV014TXpjek1UVmhNbU14T1RSa09ETXlOVEE0Tnc9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9'
url = "https://portail-api.meteofrance.fr/token"
auth_header_value = base64.b64encode(f"{client_id}".encode()).decode()

headers = {
    'Authorization': f"Basic {auth_header_value}",
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {'grant_type': 'client_credentials'}

try:
    response = requests.post(url, headers=headers, data=data, verify=False)
    response.raise_for_status()
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")