import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

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

# Caricamento dati
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
    
    return df

# Filtraggio per data
def filter_data_by_date(data, selected_date):
    return data[data["timestamp"].dt.date == selected_date]

# Valori di picco massimo e minimo della frequenza cardiaca
def get_peak_values(data):
    if data.empty:
        return None, None, None, None
    peak_row = data.loc[data["heartrate"].idxmax()]
    min_row = data.loc[data["heartrate"].idxmin()]
    return peak_row["timestamp"], peak_row["heartrate"], min_row["timestamp"], min_row["heartrate"]

# Grafico con picco massimo e minimo
def plot_chart_with_peaks(data, chart_type):
    peak_time, peak_value, min_time, min_value = get_peak_values(data)
    
    if chart_type == "Linea":
        fig = px.line(data, x='timestamp', y='heartrate', title='📈 Frequenza Cardiaca', markers=True)
    elif chart_type == "Area":
        fig = px.area(data, x='timestamp', y='heartrate', title='📈 Frequenza Cardiaca')
    elif chart_type == "Combinato":
        fig = px.scatter(data, x='timestamp', y='heartrate', title='📈 Frequenza Cardiaca')
        fig.add_scatter(x=data['timestamp'], y=data['heartrate'], mode='lines', line=dict(color='royalblue'), name='Linea')
    else:
        fig = px.bar(data, x='timestamp', y='heartrate', title='📊 Frequenza Cardiaca')

    if peak_time and peak_value:
        fig.add_trace(go.Scatter(x=[peak_time], y=[peak_value], mode='markers', marker=dict(color='red', size=10), name='Picco Max'))
    if min_time and min_value:
        fig.add_trace(go.Scatter(x=[min_time], y=[min_value], mode='markers', marker=dict(color='blue', size=10), name='Picco Min'))
    
    return fig

# Grafico a torta
def create_pie_chart(data):
    data['Fascia BPM'] = data['heartrate'].apply(lambda x: "<60" if x < 60 else "60-79" if x < 80 else "80-99" if x < 100 else "100-119" if x < 120 else "120-139" if x < 140 else "140+")
    bpm_counts = data['Fascia BPM'].value_counts(normalize=True) * 100
    bpm_counts = bpm_counts.reset_index()
    bpm_counts.columns = ['Fascia BPM', 'Percentuale']
    
    return px.pie(bpm_counts, names='Fascia BPM', values='Percentuale', title='📊 Distribuzione Frequenze Cardiache', hole=0.2)

# Funzione principale
def app():
    st.title("🏠 Frequenza Cardiaca")

    # Caricamento dati
    data = load_data_from_mongodb()
    data["date"] = data["timestamp"].dt.date
    
    if data.empty:
        st.warning("⚠️ Nessun dato disponibile nel database.")
        return
    
    # Sidebar
    st.sidebar.header("📅 Seleziona il Giorno")
    selected_date = st.sidebar.selectbox("Seleziona la data", options=sorted(data["date"].unique()), format_func=lambda x: x.strftime("%d %b %Y"))

    chart_type = st.sidebar.selectbox("📊 Seleziona il tipo di grafico", ["Linea", "Area", "Combinato", "Barre"])
    
    # Filtraggio dati
    filtered_data = filter_data_by_date(data, selected_date)

    if filtered_data.empty:
        st.warning(f"⚠️ Nessun dato per il giorno {selected_date}.")
        return
    
    peak_time, peak_value, min_time, min_value = get_peak_values(filtered_data)

    # Bottone per scaricare il CSV nella sidebar
    st.sidebar.markdown("---")
    st.sidebar.download_button("📥 Scarica CSV", data=filtered_data.to_csv(index=False).encode("utf-8"), file_name=f"dati_frequenza_{selected_date}.csv", mime="text/csv")

    # Layout in riquadri
    with st.container():
        st.markdown("""
        <style>
        .box {
            padding: 15px;
            border: 2px solid rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            background-color: #636363;
            margin-bottom: 1px;
        }
        .big-text {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            margin: 0;
        }
        .small-text {
            text-align: center;
            font-size: 16px;
            color: #555;
            margin-top: -5px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Riquadro Grafico
        with st.container():
            st.markdown("<div class='box'>", unsafe_allow_html=True)
            st.subheader(f"📈 Frequenza Cardiaca - {selected_date.strftime('%d %b %Y')}")
            st.plotly_chart(plot_chart_with_peaks(filtered_data, chart_type), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1.5])

        with col1:
            with st.container():
                st.markdown("<div class='box'>", unsafe_allow_html=True)
                st.subheader("📋 Dati del Giorno")
                st.dataframe(filtered_data.rename(columns={"timestamp": "Orario", "heartrate": "BPM"}), height=250)
                st.markdown("</div>", unsafe_allow_html=True)

            with st.container():
                st.markdown("<div class='box'>", unsafe_allow_html=True)
                st.subheader("📊 Distribuzione BPM")
                st.plotly_chart(create_pie_chart(filtered_data), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            with st.container():
                st.markdown("<div class='box' style='text-align: center;'>", unsafe_allow_html=True)
                st.subheader("📌 Valori di Picco")

                if peak_value is not None:
                    st.markdown(f"<p class='big-text' style='color: red;'>{peak_value} BPM</p>", unsafe_allow_html=True)
                    st.markdown("<p class='small-text'>Frequenza Cardiaca Massima</p>", unsafe_allow_html=True)

                if min_value is not None:
                    st.markdown(f"<p class='big-text' style='color: blue;'>{min_value} BPM</p>", unsafe_allow_html=True)
                    st.markdown("<p class='small-text'>Frequenza Cardiaca Minima</p>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    app()
