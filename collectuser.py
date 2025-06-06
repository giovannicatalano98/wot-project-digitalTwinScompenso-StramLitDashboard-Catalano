from pymongo import MongoClient

# Connessione al server MongoDB
client = MongoClient("mongodb://localhost:27018/")

# Creazione del database
db = client["health_data"]

# Creazione della collezione "utenti"
collection_utenti = db["utente"]

# Esempio di documento utente da inserire
utente = {
    "nome": "Mario",
    "cognome": "Rossi",
    "numero_telefono": "+39 123 456 789",
    "email": "mario.rossi@example.com",
    "data_nascita": "1990-05-15",
    "peso": 75,  # in kg
    "altezza": 178,  # in cm
    "data_registrazione": "2024-02-20T14:30:00Z"
}

# Inserimento del documento nella collezione
result = collection_utenti.insert_one(utente)

# Stampa dell'ID del documento inserito
print(f"Documento inserito con ID: {result.inserted_id}")

# Visualizzazione di tutti i documenti nella collezione "utenti"
print("Elenco utenti presenti nel database:")
for doc in collection_utenti.find():
    print(doc)
