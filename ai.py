import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest
from pymongo import MongoClient
import requests

# Inserisci il tuo Token API del bot Telegram e il tuo Chat ID
TELEGRAM_BOT_TOKEN = "7541037849:AAGq6Vx2ScjzI0bZkLuRf3ZDquyJsMp02cE"
TELEGRAM_CHAT_ID = "451521516"

def send_telegram_message(message):
    """
    Invia un messaggio Telegram all'utente con il bot.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.ok


# Connessione a MongoDB
@st.cache_resource
def get_mongo_client():
    try:
        client = MongoClient("mongodb://localhost:27018/", serverSelectionTimeoutMS=5000)
        client.server_info()
        return client
    except Exception as e:
        st.error("⚠️ Errore di connessione a MongoDB. Assicurati che il database sia avviato.")
        return None

# Caricamento dati da MongoDB
@st.cache_data
def load_data_from_mongodb():
    client = get_mongo_client()
    if client is None:
        st.stop()

    db = client["health_data"]
    collection = db["heart_rates"]
    data = list(collection.find({}, {"_id": 0, "timestamp": 1, "heartrate": 1}))

    if not data:
        return pd.DataFrame(columns=["timestamp", "heartrate"])

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["heartrate"] = pd.to_numeric(df["heartrate"])
    df["date"] = df["timestamp"].dt.date  # Estrai solo la data per la selezione

    return df

# Funzione per rilevare anomalie con Isolation Forest
def detect_anomalies(data, contamination):
    model = IsolationForest(contamination=contamination, random_state=42)
    data["anomaly_score"] = model.fit_predict(data[["heartrate"]])
    data["anomaly"] = data["anomaly_score"].apply(lambda x: "Anomalia" if x == -1 else "Normale")
    return data

# Streamlit UI
def app():
    st.title("📊 Rilevamento Anomalie Frequenza Cardiaca")

    # Caricamento dati
    data = load_data_from_mongodb()

    if data.empty:
        st.warning("⚠️ Nessun dato disponibile nel database.")
        return

    # Ottenere solo le date con dati disponibili
    available_dates = sorted(data["date"].unique())

    # Selettore di data con solo i giorni disponibili
    selected_date = st.sidebar.selectbox("📅 Seleziona una data", available_dates, format_func=lambda x: x.strftime("%d %b %Y"))

    # Filtraggio dei dati per la data selezionata
    filtered_data = data[data["date"] == selected_date]

    if filtered_data.empty:
        st.warning(f"⚠️ Nessun dato per il giorno {selected_date}.")
        return

    # Selettore per la sensibilità delle anomalie
    contamination_level = st.sidebar.slider("🔍 Sensibilità del rilevamento anomalie", 0.01, 0.2, 0.05, 0.01)

    # Applicare il modello di anomalie con la sensibilità scelta
    filtered_data = detect_anomalies(filtered_data, contamination_level)

    # Layout a colonne per i due grafici principali
    col1, col2 = st.columns(2)

    # 📈 **Grafico a Linea con anomalie**
    with col1:
        st.subheader("📈 Frequenza Cardiaca con Anomalie")
        fig_line = px.line(filtered_data, x="timestamp", y="heartrate", title=f"Frequenza Cardiaca - {selected_date}")
        anomalous_points = filtered_data[filtered_data["anomaly"] == "Anomalia"]
        fig_line.add_scatter(x=anomalous_points["timestamp"], y=anomalous_points["heartrate"],
                        mode="markers", marker=dict(color="red", size=10), name="Anomalie")
        st.plotly_chart(fig_line, use_container_width=True)

    # 📊 **Grafico a dispersione (Scatter Plot)**
    with col2:
        st.subheader("📊 Grafico a Dispersione (Scatter Plot)")
        fig_scatter = px.scatter(filtered_data, x="timestamp", y="heartrate", color="anomaly",
                                 title="Distribuzione BPM con Anomalie",
                                 color_discrete_map={"Normale": "blue", "Anomalia": "red"})
        st.plotly_chart(fig_scatter, use_container_width=True)

    # 📊 **Istogramma della Distribuzione BPM**
    st.subheader("📊 Istogramma della Frequenza Cardiaca")
    fig_hist = px.histogram(filtered_data, x="heartrate", color="anomaly", 
                            title="Distribuzione BPM",
                            nbins=30,  # Numero di fasce di frequenza cardiaca
                            color_discrete_map={"Normale": "blue", "Anomalia": "red"})
    st.plotly_chart(fig_hist, use_container_width=True)

    # 🚨 ALERT TELEGRAM SE CI SONO ANOMALIE
    critical_anomalies = len(anomalous_points)
    if critical_anomalies > 0:
        st.error(f"⚠️ ATTENZIONE! {critical_anomalies} anomalie critiche rilevate il {selected_date}!")

        # 🔹 Bottone per inviare la notifica Telegram
        telegram_message = f"🚨 ALERT! Rilevate {critical_anomalies} anomalie cardiache il {selected_date}!"

        if st.button("📩 Invia Notifica Telegram"):
            success = send_telegram_message(telegram_message)
            if success:
                st.success("✅ Notifica inviata con successo!")
            else:
                st.error("❌ Errore nell'invio della notifica!")

    # Mostrare tabella con dati e anomalie
    st.subheader("📋 Dati del giorno con rilevamento anomalie")
    st.dataframe(filtered_data)

if __name__ == "__main__":
    app()
