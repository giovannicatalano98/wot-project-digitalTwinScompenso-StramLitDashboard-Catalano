import os
import pandas as pd
from pymongo import MongoClient

# Configurazione MongoDB
client = MongoClient("mongodb://localhost:27018/")  # Cambia porta se necessario
db = client["health_data"]  # Nome del database
collection = db["heart_rates"]  # Nome della collezione

# Percorso della directory contenente i CSV
csv_dir = "./heart_rate_december_2024"

# Funzione per caricare un singolo file CSV
def load_csv_to_mongo(file_path):
    # Leggere il CSV con nomi corretti
    df = pd.read_csv(file_path, header=None, names=["timestamp", "heartrate"])
    
    # Conversione della colonna timestamp in formato ISO 8601
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H-%M-%S", errors="coerce")
    
    # Rimuovere righe con timestamp non validi
    df = df.dropna(subset=["timestamp"])
    
    # Inserimento in MongoDB
    records = df.to_dict("records")
    collection.insert_many(records)
    print(f"Inseriti {len(records)} record da {file_path}.")

# Caricamento di tutti i file CSV nella directory
for file_name in os.listdir(csv_dir):
    if file_name.endswith(".csv"):
        file_path = os.path.join(csv_dir, file_name)
        load_csv_to_mongo(file_path)

print("Tutti i file CSV sono stati caricati in MongoDB.")
