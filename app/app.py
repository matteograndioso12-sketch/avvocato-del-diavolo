import streamlit as st
import pandas as pd
import time
import os
import socket
from dotenv import load_dotenv

import gemini_client
import wiki_client

@st.cache_data
def get_current_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.1.52"

# Configurazione della pagina
st.set_page_config(
    page_title="Avvocato del Diavolo - Verifica Allucinazioni IA",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stile grafico personalizzato per studenti di liceo e ottimizzazione iPhone / iOS
st.markdown("""
<head>
    <!-- Meta tag per velocizzare il caricamento e full-screen su smartphone -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="Avvocato IA">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
</head>
<style>
    /* Stile Apple iOS / Cupertino moderno e pulito */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .disclaimer-box {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 12px 16px;
        border-radius: 12px;
        font-size: 0.95rem;
        color: #92400E;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .step-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .badge-alto {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 5px 14px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-medio {
        background-color: #FEF08A;
        color: #713F12;
        padding: 5px 14px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-basso {
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 5px 14px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
    }
    /* Pulsanti touch ottimizzati per smartphone */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 12px 20px;
        transition: transform 0.1s ease;
    }
    .stButton > button:active {
        transform: scale(0.98);
    }
</style>
""", unsafe_allow_html=True)

# Barra laterale (Sidebar) per navigazione e stato chiave
with st.sidebar:
    st.markdown("<div style='font-size: 3rem; margin-bottom: -15px;'>⚖️</div>", unsafe_allow_html=True)
    st.title("Avvocato del Diavolo")
    st.caption("Progetto scolastico: Premio Innovazione Digitale")
    st.markdown("---")
    
    sezione = st.radio(
        "Seleziona modalità:",
        [
            "🎓 Modalità Studente (Verifica Domanda)",
            "📊 Pagina Benchmark (Test di Massa)",
            "📱 Installa su iPhone & Android"
        ]
    )
    
    st.markdown("---")
    st.subheader("⚙️ Modalità Sistema")
    chiave_presente = gemini_client.is_key_configured()
    
    if chiave_presente:
        provider = "Groq" if gemini_client.is_groq_key() else "Google Gemini"
        st.success(f"✅ Connessione IA Live Attiva ({provider})")
        demo_mode = False
    else:
        st.info("🎓 Modalità Didattica (Pronta all'uso)")
        demo_mode = True

    with st.expander("🔑 Inserisci qui la tua Chiave API", expanded=not chiave_presente):
        input_chiave = st.text_input("Incolla qui la chiave che hai copiato:", type="password", placeholder="Incolla...")
        if st.button("💾 Salva Chiave nell'App"):
            if input_chiave.strip():
                gemini_client.salva_chiave(input_chiave)
                st.success("✅ Chiave salvata con successo!")
                st.rerun()


    st.markdown("---")
    st.caption("💡 **Regola aurea contro la disinformazione:** Nessun modello di IA garantisce il 100% di precisione. L'Avvocato del Diavolo educa al pensiero critico e alla verifica delle fonti.")

# Avviso di sicurezza e privacy (obbligatorio da requisiti)
st.markdown("""
<div class="disclaimer-box">
    <strong>🛡️ Regola di sicurezza & Privacy:</strong> Non inserire dati personali (nomi reali di persone, indirizzi, numeri). Usa solo domande di studio, storiche, scientifiche o di cultura generale.<br>
    <strong>⚖️ Nota sull'affidabilità:</strong> Non promettiamo "zero allucinazioni". Il sistema ammette l'incertezza quando le fonti non offrono conferme univoche.
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# MODALITÀ 1: MODALITÀ STUDENTE (VERIFICA INTERATTIVA)
# ==============================================================================
if sezione == "🎓 Modalità Studente (Verifica Domanda)":
    st.markdown('<div class="main-title">🎓 Verifica Guidata delle Allucinazioni</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Scopri come l\'Intelligenza Artificiale può sbagliare e come smascherare le risposte ingannevoli passo dopo passo.</div>', unsafe_allow_html=True)

    # I 10 Esempi Scolastici con allucinazioni tipiche e verifiche istantanee
    domande_esempi = [
        "Personalizzata (scrivi tu la domanda)",
        "Quale fu la prima capitale del Regno d'Italia nel 1861?",
        "Qual è la montagna più alta situata interamente in territorio italiano?",
        "In quale città morì Dante Alighieri e dove si trova la sua tomba?",
        "Chi fu il primo Presidente della Repubblica Italiana eletto nel 1948?",
        "Chi ha inventato la pila elettrica nel 1799?",
        "In quale secolo è ambientato il romanzo 'I promessi sposi'?",
        "Chi fu il primo Re d'Italia proclamato nel 1861?",
        "Quale celebre torre campanaria italiana è famosa per la sua pendenza in Piazza dei Miracoli?",
        "Qual è l'unico vulcano attivo dell'Europa continentale ad aver eruttato nel XX secolo?",
        "Chi è l'autore della celebre scultura 'Il David' conservata a Firenze?"
    ]
    
    scelta_esempio = st.selectbox("Scegli un esempio scolastico oppure scrivi liberamente:", domande_esempi)
    
    if scelta_esempio == "Personalizzata (scrivi tu la domanda)":
        domanda_input = st.text_input("Scrivi qui la tua domanda:", placeholder="Es. In che anno è stata fondata l'Università di Bologna?")
    else:
        domanda_input = st.text_input("Domanda selezionata:", value=scelta_esempio)

    pulsante_avvia = st.button("🔍 Metti alla prova con l'Avvocato del Diavolo", type="primary", use_container_width=True)

    if pulsante_avvia:
        if not domanda_input or not domanda_input.strip():
            st.warning("⚠️ Per favore, inserisci una domanda prima di avviare la verifica.")
        else:
            # Inizio dei 4 passaggi
            progress_bar = st.progress(0, text="Fase 1/4: Generazione della risposta iniziale dell'IA...")
            
            try:
                # -------------------------------------------------------------
                # PASSAGGIO 1: Risposta Iniziale
                # -------------------------------------------------------------
                with st.spinner("🤖 Passo 1: Un modello IA sta formulando una prima risposta..."):
                    risposta_iniziale = gemini_client.genera_risposta_iniziale(domanda_input, force_demo=demo_mode)
                progress_bar.progress(25, text="Fase 2/4: L'Avvocato del Diavolo analizza e attacca la risposta...")

                # -------------------------------------------------------------
                # PASSAGGIO 2: Avvocato del Diavolo
                # -------------------------------------------------------------
                with st.spinner("😈 Passo 2: L'Avvocato del Diavolo sta cercando errori, miti ed imprecisioni..."):
                    critica = gemini_client.critica_avvocato_del_diavolo(domanda_input, risposta_iniziale, force_demo=demo_mode)
                progress_bar.progress(50, text="Fase 3/4: Consultazione delle fonti indipendenti su Wikipedia...")

                # -------------------------------------------------------------
                # PASSAGGIO 3: Verifica Fonti Esterne (Wikipedia)
                # -------------------------------------------------------------
                fonti_raccolte = gemini_client.get_preset_fonti(domanda_input)
                if not fonti_raccolte:
                    termini = critica.get("termini_di_ricerca", [domanda_input[:30]])
                    with st.spinner("📚 Passo 3: Ricerca rapida su Wikipedia in italiano..."):
                        for termine in termini:
                            ris = wiki_client.cerca_wikipedia(termine, max_risultati=1)
                            if ris:
                                fonti_raccolte.extend(ris)
                progress_bar.progress(75, text="Fase 4/4: Redazione della risposta finale con livello di affidabilità...")

                # -------------------------------------------------------------
                # PASSAGGIO 4: Sintesi e Risposta Finale
                # -------------------------------------------------------------
                with st.spinner("⚖️ Passo 4: Elaborazione della risposta finale corretta..."):
                    sintesi = gemini_client.genera_risposta_finale(domanda_input, risposta_iniziale, critica, fonti_raccolte, force_demo=demo_mode)
                progress_bar.progress(100, text="✅ Verifica completata con successo!")

                st.markdown("---")

                # VISUALIZZAZIONE MODALITÀ STUDENTE (I 4 PASSAGGI SPIEGATI)
                col_sx, col_dx = st.columns([1, 1])

                with col_sx:
                    st.markdown("### 🤖 1. La Risposta Iniziale dell'IA")
                    st.info(risposta_iniziale)
                    st.caption("Questa è la risposta grezza che un comune assistente virtuale fornirebbe allo studente.")

                    st.markdown("### 😈 2. L'Attacco dell'Avvocato del Diavolo")
                    with st.expander("Vedi tutte le obiezioni e i dubbi rilevati", expanded=True):
                        st.markdown(f"**Valutazione critica:** {critica.get('valutazione_sintetica', '')}")
                        st.markdown("**Possibili allucinazioni o punti da chiarire:**")
                        for c in critica.get("critiche", []):
                            st.markdown(f"- ⚠️ {c}")
                        st.markdown(f"**Parole chiave ricercate:** `{', '.join(termini)}`")

                with col_dx:
                    st.markdown("### 📚 3. Verifica con Fonti Esterne (Wikipedia)")
                    if fonti_raccolte:
                        for f in fonti_raccolte:
                            with st.expander(f"📖 Fonte: {f['titolo']}", expanded=False):
                                st.write(f['estratto'])
                                st.markdown(f"[🔗 Leggi l'articolo completo su Wikipedia]({f['url']})")
                    else:
                        st.warning("Nessuna pagina Wikipedia trovata direttamente per i termini cercati.")

                    st.markdown("### ⚖️ 4. Risposta Finale Verificata")
                    affidabilita = sintesi.get("affidabilita", "Medio").capitalize()
                    badge_class = f"badge-{affidabilita.lower()}"
                    
                    st.markdown(f'Affidabilità calcolata: <span class="{badge_class}">{affidabilita}</span>', unsafe_allow_html=True)
                    st.caption(f"Motivazione: {sintesi.get('motivazione_affidabilita', '')}")
                    
                    st.success(sintesi.get("risposta_finale", ""))

                    if sintesi.get("correzioni_applicate"):
                        st.markdown("**🔧 Correzioni applicate rispetto alla prima risposta:**")
                        for corr in sintesi.get("correzioni_applicate", []):
                            st.markdown(f"- {corr}")

                    if sintesi.get("punti_incerti"):
                        st.markdown(f"**❓ Cosa resta incerto:** *{sintesi.get('punti_incerti')}*")

            except Exception as e:
                st.error(f"Si è verificato un errore durante l'elaborazione: {str(e)}")
                st.info("Suggerimento: controlla che la tua connessione internet sia attiva e che la chiave Gemini sia valida.")

# ==============================================================================
# MODALITÀ 2: PAGINA BENCHMARK (CONFRONTO E STATISTICHE)
# ==============================================================================
elif sezione == "📊 Pagina Benchmark (Test di Massa)":
    st.markdown('<div class="main-title">📊 Pagina Benchmark & Sperimentazione</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Confronta la percentuale di accuratezza delle risposte con e senza la verifica dell\'Avvocato del Diavolo.</div>', unsafe_allow_html=True)

    st.write("Questa sezione permette di eseguire un test scientifico su una serie di domande scolastiche per misurare concretamente quanto la verifica riduca le risposte errate o imprecise.")

    tab1, tab2 = st.tabs(["📁 Carica / Usa Dataset di Esempio", "⚙️ Esegui Test"])

    with tab1:
        st.markdown("#### File di domande per il test")
        file_caricato = st.file_uploader("Carica un file CSV con le tue domande (opzionale):", type=["csv"])
        
        usare_default = st.checkbox("Usa il file di esempio integrato (10 domande scolastiche e locali)", value=True)

        df_benchmark = None
        if file_caricato is not None:
            df_benchmark = pd.read_csv(file_caricato)
            st.success(f"File caricato con successo! Trovate {len(df_benchmark)} domande.")
        elif usare_default and os.path.exists("benchmark_domande.csv"):
            df_benchmark = pd.read_csv("benchmark_domande.csv")
            st.info("Caricato il file di esempio predefinito con 10 domande.")

        if df_benchmark is not None:
            st.dataframe(df_benchmark, use_container_width=True)

    with tab2:
        if df_benchmark is None:
            st.warning("Carica prima un file CSV nella scheda precedente.")
        else:
            num_domande = st.slider("Numero di domande da testare nel benchmark:", min_value=1, max_value=len(df_benchmark), value=min(3, len(df_benchmark)))
            st.caption("Nota per il test rapido: seleziona quante domande vuoi confrontare.")

            if st.button("🚀 Avvia Benchmark Comparativo", type="primary"):
                risultati = []
                barra = st.progress(0, text="Inizio benchmark...")

                for idx, row in df_benchmark.head(num_domande).iterrows():
                    domanda = row.get("domanda", "")
                    attesa = row.get("risposta_corretta_attesa", "")
                    
                    barra.progress((idx) / num_domande, text=f"Testando domanda {idx+1}/{num_domande}: {domanda[:35]}...")
                    
                    # 1. Senza verifica (solo risposta base)
                    risp_base = gemini_client.genera_risposta_iniziale(domanda, force_demo=demo_mode)
                    
                    # 2. Con verifica Avvocato del Diavolo
                    critica = gemini_client.critica_avvocato_del_diavolo(domanda, risp_base, force_demo=demo_mode)
                    fonti = gemini_client.get_preset_fonti(domanda)
                    if not fonti:
                        for t in critica.get("termini_di_ricerca", [domanda[:30]]):
                            r = wiki_client.cerca_wikipedia(t, 1)
                            if r:
                                fonti.extend(r)
                    risp_verificata = gemini_client.genera_risposta_finale(domanda, risp_base, critica, fonti, force_demo=demo_mode)
                    
                    # Valutazione di correttezza (semplificata per il benchmark)
                    # Controlliamo la presenza delle parole chiave della risposta corretta
                    parole_chiave = [w.lower() for w in attesa.replace("(", "").replace(")", "").split() if len(w) > 4]
                    
                    ok_base = sum(1 for w in parole_chiave if w in risp_base.lower()) >= (len(parole_chiave) // 2) if parole_chiave else True
                    ok_verif = sum(1 for w in parole_chiave if w in risp_verificata.get("risposta_finale", "").lower()) >= (len(parole_chiave) // 2) if parole_chiave else True

                    risultati.append({
                        "ID": row.get("id", idx+1),
                        "Domanda": domanda,
                        "Risposta Attesa": attesa,
                        "Risposta Base (Senza Verifica)": risp_base[:120] + "...",
                        "Base Corretta?": "✅ Sì" if ok_base else "❌ Dubbia/No",
                        "Risposta Verificata (Con Avvocato)": risp_verificata.get("risposta_finale", "")[:120] + "...",
                        "Verificata Corretta?": "✅ Sì" if ok_verif else "❌ Dubbia/No",
                        "Affidabilità": risp_verificata.get("affidabilita", "Medio")
                    })

                barra.progress(100, text="Benchmark completato!")

                df_risultati = pd.DataFrame(risultati)
                
                # Statistiche
                tot = len(df_risultati)
                corrette_base = sum(1 for r in risultati if r["Base Corretta?"] == "✅ Sì")
                corrette_verif = sum(1 for r in risultati if r["Verificata Corretta?"] == "✅ Sì")
                perc_base = int((corrette_base / tot) * 100) if tot else 0
                perc_verif = int((corrette_verif / tot) * 100) if tot else 0

                st.markdown("### 📈 Risultati Comparativi")
                c1, c2, c3 = st.columns(3)
                c1.metric("Domande Testate", tot)
                c2.metric("Accuratezza Senza Verifica", f"{perc_base}%")
                c3.metric("Accuratezza Con Avvocato del Diavolo", f"{perc_verif}%", delta=f"+{perc_verif - perc_base}%")

                st.dataframe(df_risultati, use_container_width=True)

                # Pulsante di esportazione in CSV (richiesto esplicitamente)
                csv_export = df_risultati.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Scarica Tabella Risultati in CSV",
                    data=csv_export,
                    file_name="risultati_benchmark_avvocato_diavolo.csv",
                    mime="text/csv"
                )

# ==============================================================================
# MODALITÀ 3: INSTALLA SU IPHONE & ANDROID
# ==============================================================================
elif sezione == "📱 Installa su iPhone & Android":
    st.markdown('<div class="main-title">📱 Installa l\'App su iPhone e Android</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Guida rapida per avere l\'applicazione installata a schermo intero sullo smartphone per il concorso scolastico.</div>', unsafe_allow_html=True)

    curr_ip = get_current_ip()
    curr_url = f"http://{curr_ip}:8501"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=240x240&data={curr_url}"

    tab_ios, tab_android = st.tabs(["🍏 Versione per iPhone (Apple iOS)", "🤖 Versione per Android (APK & WebApp)"])

    with tab_ios:
        c_sx, c_dx = st.columns([1, 1])
        with c_sx:
            st.markdown("### 🍏 Come installarla su iPhone in 3 tocchi:")
            st.markdown(f"""
            1. **Collega l'iPhone al Wi-Fi** di casa o della scuola (lo stesso a cui è connesso questo PC).
            2. Inquadra il **QR Code** qui a destra con la **fotocamera dell'iPhone** (oppure apri **Safari** e scrivi `{curr_url}`).
            3. In basso su Safari tocca l'icona di **Condivisione** *(il quadratino con la freccia in su `⎋`)*.
            4. Scorri il menu e tocca **'Aggiungi alla schermata Home'** *(icona `+`)*.
            5. Tocca in alto a destra **'Aggiungi'**.
            """)
            st.success("🎉 **Fatto!** L'icona dell'Avvocato del Diavolo comparirà sulla schermata principale del tuo iPhone e si aprirà come una vera app nativa a tutto schermo!")
        with c_dx:
            st.image(qr_url, caption=f"Inquadra con la fotocamera dell'iPhone ({curr_url})")

    with tab_android:
        c_sx, c_dx = st.columns([1, 1])
        with c_sx:
            st.markdown("### 🤖 Come usarla su Android:")
            st.markdown(f"""
            * **Metodo Rapido (Schermata Home):**  
              Inquadra il QR Code, apri in Chrome, tocca i **3 puntini ⋮** in alto a destra e seleziona **'Installa app'** o **'Aggiungi a Home'**.
            
            * **Metodo File .APK (da consegnare ai docenti):**  
              1. Vai su [FreeWebToApk](https://freewebtoapk.com) o [WebIntoApp](https://www.webintoapp.com).  
              2. Incolla l'indirizzo: `{curr_url}`  
              3. Clicca su **'Generate APK'** e scarica il file `.apk` sul tuo telefono!
            """)
        with c_dx:
            st.image(qr_url, caption=f"Inquadra con il telefono ({curr_url})")

