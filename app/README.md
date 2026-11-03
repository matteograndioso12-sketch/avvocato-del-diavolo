# ⚖️ Avvocato del Diavolo: Verifica delle Allucinazioni dei Chatbot IA

> **Progetto scolastico per il Premio Innovazione Digitale**  
> *Categoria: Educazione digitale, sicurezza online e contrasto alla disinformazione*  
> *Target: Studenti della scuola secondaria di secondo grado (Licei e Istituti Tecnici)*

---

## 🎯 Di cosa si tratta?
Le Intelligenze Artificiali generative (come ChatGPT o Gemini) spesso producono risposte apparentemente convincenti ma contenenti **allucinazioni** (errori storici, scientifici, date inventate o miti popolari).

L'**Avvocato del Diavolo** è un'applicazione didattica che insegna agli studenti a non fidarsi ciecamente dell'IA, applicando un metodo critico e scientifico in **4 passaggi trasparenti**:

1. **🤖 Risposta Iniziale:** L'IA formula una prima risposta a una domanda.
2. **😈 Attacco dell'Avvocato del Diavolo:** Un secondo prompt specializzato agisce da revisore spietato, cercando contraddizioni, fallacie logiche ed errori di fatto.
3. **📚 Verifica Esterna Indipendente:** Vengono estratti i termini chiave e verificati in tempo reale su fonti autorevoli (l'API ufficiale di Wikipedia in italiano).
4. **⚖️ Risposta Finale Verificata:** Viene restituita la risposta corretta con un **Livello di Affidabilità** (*Alto, Medio, Basso*), l'indicazione esplicita delle correzioni apportate e ciò che rimane incerto.

---

## 📁 Struttura dei File

* `app.py`: L'interfaccia web principale creata con Streamlit.
* `gemini_client.py`: Modulo che comunica in sicurezza con l'IA Google Gemini (con modalità simulazione integrata).
* `wiki_client.py`: Modulo per consultare l'enciclopedia Wikipedia in italiano.
* `benchmark_domande.csv`: Dataset di prova con 10 domande su storia, letteratura, geografia, scienze e arte italiana.
* `.env`: File riservato dove inserire la propria chiave API di Google Gemini.
* `.env.example`: File di esempio per la configurazione.

---

## 🚀 Come avviare l'applicazione sul computer

### 1. Requisiti
Avere installato Python sul computer (incluso in Windows/Mac). I componenti necessari sono già stati predisposti:
```bash
pip install streamlit google-genai python-dotenv requests pandas
```

### 2. Configurare la chiave API Gemini
1. Apri il file `.env` con il Blocco Note.
2. Incolla la tua chiave subito dopo `GEMINI_API_KEY=` (es. `GEMINI_API_KEY=AIzaSyD...`).
3. Salva con `Ctrl + S`.
*(Nota: se vuoi solo provare subito l'app a scuola, puoi anche usare la **simulazione didattica** già inclusa senza chiave!)*

### 3. Avviare l'App
Apri il terminale (Prompt dei comandi o PowerShell) nella cartella del programma e scrivi:
```bash
streamlit run app.py
```
Il browser si aprirà automaticamente all'indirizzo `http://localhost:8501`.

---

## 📱 Come usare l'App da Smartphone (iPhone & Android)

### 🍏 Per iPhone (Apple iOS) - In 3 tocchi senza scaricare file
1. Assicurati che l'iPhone sia connesso allo **stesso Wi-Fi** del computer.
2. Apri **Safari** e digita l'indirizzo mostrato dall'app (es. `http://192.168.1.52:8501`), oppure inquadra il QR Code con la fotocamera.
3. In basso su Safari tocca l'icona di **Condivisione** *(il quadratino con la freccia in su `⎋`)*.
4. Scorri il menu e tocca **"Aggiungi alla schermata Home"**.
5. Tocca **"Aggiungi"**: l'icona ufficiale con la bilancia comparirà sulla schermata principale dell'iPhone e si aprirà come un'app vera a schermo intero senza barre del browser!

---

### 🤖 Per Android (APK e WebApp)
1. **Metodo Rapido:** Apri l'indirizzo su Google Chrome dal telefono, tocca i 3 puntini ⋮ e premi **"Aggiungi a schermata Home"**.
2. **File APK compilato:** Vai su [FreeWebToApk](https://freewebtoapk.com), inserisci l'indirizzo dell'app, clicca su **"Generate APK"** e installa il file `.apk` scaricato.

---

## 🛡️ Privacy e Trasparenza Etica
* **Nessun dato personale:** L'applicazione mostra un avviso esplicito e non raccoglie dati personali.
* **Onestà intellettuale:** Nessun modello di intelligenza artificiale è infallibile. L'applicazione non promette "zero allucinazioni", ma esplicita il grado di affidabilità e ciò che rimane da verificare.
