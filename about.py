import streamlit as st
import base64

def app():
    # Stile CSS
    st.markdown(
        """
        <style>
        .title {
            font-size: 42px;
            font-weight: bold;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 20px;
        }
        .container {
            background-color: #121212;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.3);
            color: #EAEAEA;
            font-size: 18px;
            line-height: 1.6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Funzione per convertire immagine in base64
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Caricamento loghi
    logo1_base64 = get_base64_image("UniSalento-Universita-del-Salento.svg.png")
    logo2_base64 = get_base64_image("IDA.png")

    # Visualizzazione loghi centrati e più grandi
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; gap: 50px; margin-bottom: 30px;">
            <img src="data:image/png;base64,{logo1_base64}" width="200">
            <img src="data:image/png;base64,{logo2_base64}" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Titolo
    st.markdown("<div class='title'>About il Progetto</div>", unsafe_allow_html=True)

    # Testo continuo del progetto
    st.markdown(
        """
        <div class="container">
        Questo progetto nasce con l’obiettivo di monitorare e analizzare la frequenza cardiaca degli utenti attraverso il Google Pixel Watch 2, sfruttando l’integrazione con la piattaforma Fitbit. I dati raccolti vengono analizzati tramite un modello di machine learning non supervisionato, nello specifico Isolation Forest, che consente di rilevare anomalie nei battiti cardiaci senza bisogno di una fase iniziale di etichettatura dei dati. L’utilizzo di tecnologie come Python, Scikit-learn e Streamlit permette di creare un’interfaccia semplice e funzionale per l’utente, offrendo una visualizzazione immediata delle anomalie individuate. L’approccio adottato è pensato per fornire uno strumento interpretabile e facilmente integrabile con sistemi sanitari o progetti personali di prevenzione. Il progetto rappresenta un esempio concreto di come i dispositivi indossabili e l’intelligenza artificiale possano collaborare per promuovere il benessere e la salute.
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    app()
