import requests
import pandas as pd

# Definire l'endpoint e i parametri della richiesta
url = "https://api.fitbit.com/1/user/-/activities/heart/date/2024-11-22/1d/1min.json"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BLNFEiLCJzdWIiOiJDNFIzNkwiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNzM0MzkxNjU4LCJpYXQiOjE3MzQzNjI4NTh9.HFQEXtDxjThH5H6HSMhC2gbaV-2-lcnURKodfxuSZl0"
}

# Fare la richiesta GET all'API
response = requests.get(url, headers=headers)

# Controllare se la richiesta ha avuto successo
if response.status_code == 200:
    data = response.json()
    
    # Estrarre i dati di time e value
    heart_data = data["activities-heart-intraday"]["dataset"]
    
    # Creare un DataFrame con i dati estratti
    df = pd.DataFrame(heart_data)
    
    # Definire il percorso del file CSV
    csv_file_path = "heart_rate_data.csv"
    
    # Salvare il DataFrame in un file CSV
    df.to_csv(csv_file_path, index=False)
    
    print(f"I dati del battito cardiaco sono stati salvati in {csv_file_path}")
else:
    print(f"Errore nella richiesta API: {response.status_code} - {response.text}")

