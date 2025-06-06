import requests
import pandas as pd
from datetime import datetime, timedelta

# Definire i parametri di autenticazione e l'endpoint API base
base_url = "https://api.fitbit.com/1/user/-/activities/heart/date/{}/1d/1min.json"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BLNFEiLCJzdWIiOiJDNFIzNkwiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNzMyMzMxMTA3LCJpYXQiOjE3MzIzMDIzMDd9.4BwXDTG4ODLb93r_wkvvmFJOtZcJm5z8oNMnDXq-kkk"
}

# Definire l'intervallo di date
start_date = datetime.strptime("2024-06-24", "%Y-%m-%d")
end_date = datetime.strptime("2024-11-22", "%Y-%m-%d")
current_date = start_date

# Ciclo per generare un CSV per ogni giorno
while current_date <= end_date:
    # Formattare la data per l'endpoint API
    date_str = current_date.strftime("%Y-%m-%d")
    url = base_url.format(date_str)
    
    # Fare la richiesta API
    response = requests.get(url, headers=headers)
    
    # Controllare se la richiesta ha avuto successo
    if response.status_code == 200:
        data = response.json()
        heart_data = data.get("activities-heart-intraday", {}).get("dataset", [])
        
        # Creare un DataFrame con i dati estratti
        df = pd.DataFrame(heart_data)
        
        # Aggiungere la colonna della data completa
        if not df.empty:
            df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S").dt.strftime(f"{date_str} %H-%M-%S")
            df.rename(columns={"time": "datetime", "value": "heartrate"}, inplace=True)
            
            # Salvare il DataFrame in un file CSV
            csv_file_path = f"heart_rate_{date_str}.csv"
            df.to_csv(csv_file_path, index=False)
            print(f"File salvato: {csv_file_path}")
        else:
            print(f"Nessun dato disponibile per la data: {date_str}")
    else:
        print(f"Errore API per la data {date_str}: {response.status_code} - {response.text}")
    
    # Passare al giorno successivo
    current_date += timedelta(days=1)
