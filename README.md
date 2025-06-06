# wot-project-digitalTwinScompenso-StramLitDashboard-Catalano

📊 Rilevamento Anomalie Frequenza Cardiaca

Questa applicazione è una webapp sviluppata con **Streamlit**  per analizzare i dati della frequenza cardiaca raccolti con Google Pixel Watch 2 e successivamente scaricati grazie ad API.
Utilizzando l’algoritmo **Isolation Forest**, l’app rileva anomalie nei battiti cardiaci giornalieri e permette di inviare **notifiche Telegram** in caso di eventi critici.
Questo progetto nasce con l’obiettivo di monitorare e analizzare la frequenza cardiaca degli utenti attraverso il Google Pixel Watch 2, sfruttando l’integrazione con la piattaforma Fitbit. I dati raccolti vengono analizzati tramite un modello di machine learning non supervisionato, nello specifico Isolation Forest, che consente di rilevare anomalie nei battiti cardiaci senza bisogno di una fase iniziale di etichettatura dei dati. L’utilizzo di tecnologie come Python, Scikit-learn e Streamlit permette di creare un’interfaccia semplice e funzionale per l’utente, offrendo una visualizzazione immediata delle anomalie individuate. L’approccio adottato è pensato per fornire uno strumento interpretabile e facilmente integrabile con sistemi sanitari o progetti personali di prevenzione. Il progetto rappresenta un esempio concreto di come i dispositivi indossabili e l’intelligenza artificiale possano collaborare per promuovere il benessere e la salute.

**Funzionalità**

- Connessione automatica a un database MongoDB locale
-  Selezione della data con dati disponibili
-  Analisi delle anomalie tramite **modello Isolation Forest**
-  Visualizzazioni interattive con **Plotly**:
-  Notifiche via **Telegram Bot** in caso di anomalie
-  Esportazione e visualizzazione tabellare dei dati

 **Tecnologie utilizzate**

- [Streamlit](https://streamlit.io/) per l'interfaccia utente
- [MongoDB](https://www.mongodb.com/) per la gestione dati
- [Plotly](https://plotly.com/python/) per la visualizzazione grafica
- [Scikit-learn](https://scikit-learn.org/) per il machine learning
- [Telegram Bot API](https://core.telegram.org/bots/api) per gli alert automatici

 
 **Requisiti**
 Python 3.8 o superiore

 La presentazione del sistema è disponibile nella seguente repository,con relativa documentazione completa: [wot-project-digitalTwinScompenso-Presentation-Catalano-](https://github.com/giovannicatalano98/wot-project-digitalTwinScompenso-Presentation-Catalano-)

 
