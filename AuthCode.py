import requests
from requests.auth import HTTPBasicAuth

# Dati della tua applicazione Fitbit
client_id = '23PK4Q'
client_secret = 'ee52a6d836d5f371275c58ee1d5b3b07'
redirect_uri = 'http://127.0.0.1:8080'
authorization_code = 'c1d6cd12feb8f6ab6d5448cd971898bc4eee58ad'
code_verifier = '01234567890123456789012345678901234567890123456789'


# URL per ottenere il token
token_url = 'https://api.fitbit.com/oauth2/token'

# Parametri della richiesta
payload = {
    'client_id': client_id,
    'grant_type': 'authorization_code',
    'redirect_uri': redirect_uri,
    'code': authorization_code,
    'code_verifier': code_verifier
}

# Autenticazione di base
auth = HTTPBasicAuth(client_id, client_secret)

# Header della richiesta
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Effettua la richiesta POST
response = requests.post(token_url, data=payload, headers=headers, auth=auth)

# Controlla la risposta
if response.status_code == 200:
    # Successo
    token_info = response.json()
    print('Access Token:', token_info['access_token'])
    print('Refresh Token:', token_info['refresh_token'])
else:
    # Errore
    print('Errore:', response.status_code)
    print(response.json())
