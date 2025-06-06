import streamlit as st
import base64


def app():
    # Stile CSS migliorato per immagine, colori e box
    st.markdown(
        """
        <style>
        .title {
            font-size: 42px;
            font-weight: bold;
            color: #fffff; /* Verde petrolio */
            text-align: center;
            margin-bottom: 10px;
        }
        .profile-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 20px;
        }
        .profile {
            border-radius: 50%;
            width: 200px;
            height: 200px;
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
            border: 4px solid #2A9D8F; /* Bordo verde acqua */
        }
        .name {
            font-size: 30px;
            font-weight: bold;
            color: #F8F9FA;
            text-align: left;
            margin-top: 15px;
        }
        .container {
            background-color: #121212; /* Grigio chiaro */
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
        }
        .key {
            font-weight: bold;
            color: #1D3557; /* Blu petrolio */
            font-size: 20px;
        }
        .value {
            color: #E63946; /* Rosso tenue */
            font-size: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Titolo della pagina
    st.markdown("<div class='title'>Il Mio Account</div>", unsafe_allow_html=True)

    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
         return base64.b64encode(img_file.read()).decode()

        # Converte l'immagine
    image_base64 = get_base64_image("charizard.png")

# HTML per centrare immagine e nome
    st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{image_base64}" width="250" style="border-radius: 50%; box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);">
        <h2 style="color: #FFFFF; margin-top: 10px;">Giovanni Catalano</h2>
    </div>
    """,
    unsafe_allow_html=True
  )
    

    # Box Dati Personali
    st.markdown("### 📋 Dati Personali")
    st.markdown(
        """
        <div class="container">
            <p><span class="key">Nome:</span> <span class="value">Giovanni Catalano</span></p>
            <p><span class="key">Età:</span> <span class="value">26 anni</span></p>
            <p><span class="key">Email:</span> <span class="value">giovanni.catalano@example.com</span></p>
            <p><span class="key">Numero di Telefono:</span> <span class="value">+39 123 456 789</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Box Stato di Salute
    st.markdown("### 💓 Stato di Salute")
    st.markdown(
        """
        <div class="container">
            <p><span class="key">Battito Cardiaco Medio:</span> <span class="value">75 BPM</span></p>
            <p><span class="key">Frequenza Cardiaca Massima:</span> <span class="value">120 BPM</span></p>
            <p><span class="key">Frequenza Cardiaca Minima:</span> <span class="value">60 BPM</span></p>
            <p><span class="key">Passi Giornalieri:</span> <span class="value">10,000 passi</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Box Obiettivi di Salute
    st.markdown("### 🎯 Obiettivi di Salute")
    st.markdown(
        """
        <div class="container">
            <p><span class="key">Obiettivo Passi:</span> <span class="value">10,000 passi al giorno</span></p>
            <p><span class="key">Obiettivo Frequenza Cardiaca:</span> <span class="value">70-100 BPM</span></p>
            <p><span class="key">Obiettivo Peso:</span> <span class="value">70 kg</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Box Suggerimenti
    st.markdown("### 🩺 Suggerimenti")
    st.markdown(
        """
        <div class="container">
            <ul>
                <li>💧 Bevi almeno 2 litri d'acqua al giorno.</li>
                <li>🚶‍♂️ Fai una passeggiata di almeno 30 minuti ogni giorno.</li>
                <li>🛌 Dormi almeno 7 ore ogni notte.</li>
                <li>🥗 Segui una dieta equilibrata ricca di frutta e verdura.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    app()
