import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
load_dotenv()

import home, account, about,ai

# Imposta il layout una sola volta all'inizio
st.set_page_config(layout='wide')

# Crea il menu laterale
with st.sidebar:
    app = option_menu(
        menu_title='HeartApp ',
        options=['Home', 'Account','AI', 'About'],
        icons=['house-fill', 'person-circle', 'nvidia','info-circle-fill'],
        menu_icon='heart-pulse',
        default_index=0,  # Parte dalla Home
        styles={
            "container": {"padding": "5!important", "background-color": "#800020"},
            "icon": {"color": "white", "font-size": "23px"}, 
            "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

# Logica di navigazione tra le pagine
if app == "Home":
    home.app()
elif app == "Account":
    account.app()    
elif app == "About":
    about.app()
elif app == "AI":
    ai.app()
