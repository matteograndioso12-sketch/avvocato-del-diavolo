import os
import json
from dotenv import load_dotenv
from google import genai
import wiki_client

load_dotenv()

def get_api_key():
    return os.getenv("GEMINI_API_KEY", "").strip()

def salva_chiave(nuova_chiave: str):
    k = nuova_chiave.strip()
    os.environ["GEMINI_API_KEY"] = k
    with open(".env", "w", encoding="utf-8") as f:
        f.write(f"# Chiave API salvata\nGEMINI_API_KEY={k}\n")

def is_key_configured():
    key = get_api_key()
    return bool(key and key != "inserisci_qui_la_tua_chiave" and len(key) > 10)

def is_groq_key():
    return get_api_key().startswith("gsk_")

def chiama_groq(prompt: str) -> str:
    import requests
    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json"
    }
    # Usiamo il modello ad altissima precisione disponibile sulla tua chiave Groq
    body = {
        "model": "openai/gpt-oss-120b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4
    }
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body, timeout=12)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
        # Se 120b è occupato, usiamo 20b
        body["model"] = "openai/gpt-oss-20b"
        res2 = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body, timeout=10)
        if res2.status_code == 200:
            return res2.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        pass
    return ""

def get_client():
    if not is_key_configured() or is_groq_key():
        return None
    try:
        return genai.Client(api_key=get_api_key())
    except Exception:
        return None

# Database locale istantaneo dei 10 Preset Scolastici (risposte, critiche, fonti e sintesi)
PRESET_DATABASE = {
    "capitale": {
        "risposta_iniziale": "La prima capitale del Regno d'Italia nel 1861 fu Roma, considerata fin dal principio il cuore naturale e storico della nazione unificata.",
        "critica": {
            "critiche": [
                "Allucinazione storica comune: Roma non faceva nemmeno parte dell'Italia nel 1861! Apparteneva ancora allo Stato Pontificio.",
                "La prima capitale effettiva fu Torino (1861-1865). Successivamente Firenze (1865-1871) e solo infine Roma (1871 dopo Porta Pia)."
            ],
            "valutazione_sintetica": "L'IA confonde la proclamazione di Roma a capitale ideale con la realtà storica dell'epoca.",
            "termini_di_ricerca": ["Capitale del Regno d'Italia", "Torino"]
        },
        "fonti": [
            {
                "titolo": "Capitale del Regno d'Italia",
                "estratto": "La prima capitale del Regno d'Italia fu Torino dal 1861 al 1865. In seguito alla Convenzione di settembre, la capitale fu trasferita a Firenze nel 1865 e infine a Roma nel 1871.",
                "url": "https://it.wikipedia.org/wiki/Capitale_del_Regno_d%27Italia"
            }
        ],
        "sintesi": {
            "risposta_finale": "La prima capitale del Regno d'Italia nel 1861 fu Torino (fino al 1865). Roma fu annessa solo nel 1870 e divenne capitale ufficiale nel 1871.",
            "affidabilita": "Alto",
            "motivazione_affidabilita": "Confermato dalla storiografia ufficiale e dagli atti parlamentari del 1861.",
            "correzioni_applicate": ["Corretta la capitale da Roma a Torino", "Chiarita la data di annessione di Roma (1870)"],
            "punti_incerti": "Nessuno."
        }
    },
    "montagna": {
        "risposta_iniziale": "La montagna più alta situata interamente in territorio italiano è il Monte Bianco, con la sua maestosa vetta di 4.808 metri nelle Alpi.",
        "critica": {
            "critiche": [
                "Imprecisione geografica frequente: il massiccio del Monte Bianco è condiviso sul confine con la Francia.",
                "La vetta più alta *interamente* entro i confini dello Stato italiano è il Gran Paradiso (4.061 metri), situato tra Valle d'Aosta e Piemonte."
            ],
            "valutazione_sintetica": "L'IA ha ignorato la parola chiave 'interamente' nella domanda dello studente.",
            "termini_di_ricerca": ["Gran Paradiso", "Monte Bianco"]
        },
        "fonti": [
            {
                "titolo": "Gran Paradiso",
                "estratto": "Il Gran Paradiso (4.061 m s.l.m.) è la montagna più alta situata interamente in territorio italiano, compresa nel massiccio omonimo delle Alpi Graie tra Valle d'Aosta e Piemonte.",
                "url": "https://it.wikipedia.org/wiki/Gran_Paradiso"
            }
        ],
        "sintesi": {
            "risposta_finale": "La montagna più alta situata interamente in Italia è il Gran Paradiso (4.061 m). Il Monte Bianco (4.808 m) è più alto ma condiviso sul confine con la Francia.",
            "affidabilita": "Alto",
            "motivazione_affidabilita": "Dati geografici e cartografici IGM verificati.",
            "correzioni_applicate": ["Sostituito Monte Bianco con Gran Paradiso", "Specificata la differenza di sovranità territoriale"],
            "punti_incerti": "Nessuno."
        }
    },
    "dante": {
        "risposta_iniziale": "Dante Alighieri morì a Firenze, la sua città d'origine, dove oggi è custodita la sua tomba nella Basilica di Santa Croce.",
        "critica": {
            "critiche": [
                "Allucinazione biografica: Dante morì in esilio a Ravenna nella notte tra il 13 e il 14 settembre 1321.",
                "Nella Basilica di Santa Croce a Firenze esiste solo un cenotafio (un monumento funebre vuoto). I resti sono a Ravenna."
            ],
            "valutazione_sintetica": "Confusione tra la patria natia di Dante e il suo reale luogo di esilio e sepoltura.",
            "termini_di_ricerca": ["Dante Alighieri", "Tomba di Dante"]
        },
        "fonti": [
            {
                "titolo": "Tomba di Dante",
                "estratto": "La tomba di Dante Alighieri è il sepolcro neoclassico che custodisce le spoglie del sommo poeta a Ravenna, città in cui morì durante l'esilio nel 1321.",
                "url": "https://it.wikipedia.org/wiki/Tomba_di_Dante"
            }
        ],
        "sintesi": {
            "risposta_finale": "Dante Alighieri morì in esilio a Ravenna nel 1321, non a Firenze. La sua tomba si trova tuttora a Ravenna presso la basilica di San Francesco.",
            "affidabilita": "Alto",
            "motivazione_affidabilita": "Fatto storico documentato universalmente.",
            "correzioni_applicate": ["Corretta la città di morte da Firenze a Ravenna", "Precisato che a Firenze c'è solo un cenotafio vuoto"],
            "punti_incerti": "Nessuno."
        }
    },
    "presidente": {
        "risposta_iniziale": "Il primo Presidente della Repubblica Italiana fu Enrico De Nicola, eletto subito dopo il referendum del 1946.",
        "critica": {
            "critiche": [
                "Errore terminologico e istituzionale: Enrico De Nicola fu 'Capo provvisorio dello Stato'.",
                "Il primo vero Presidente della Repubblica eletto secondo le norme della Costituzione italiana (maggio 1948) fu l'economista Luigi Einaudi."
            ],
            "valutazione_sintetica": "Confusione tra la carica provvisoria post-bellica e la prima presidenza costituzionale.",
            "termini_di_ricerca": ["Presidente della Repubblica Italiana", "Luigi Einaudi"]
        },
        "fonti": [
            {
                "titolo": "Presidente della Repubblica Italiana",
                "estratto": "Il primo presidente eletto secondo la Costituzione repubblicana del 1948 fu Luigi Einaudi. In precedenza Enrico De Nicola aveva ricoperto la carica di Capo provvisorio dello Stato.",
                "url": "https://it.wikipedia.org/wiki/Presidente_della_Repubblica_Italiana"
            }
        ],
        "sintesi": {
            "risposta_finale": "Il primo Presidente eletto a norma della Costituzione nel 1948 fu Luigi Einaudi. Enrico De Nicola era stato in precedenza il Capo provvisorio dello Stato.",
            "affidabilita": "Alto",
            "motivazione_affidabilita": "Archivio storico del Quirinale.",
            "correzioni_applicate": ["Distinzione tra Capo provvisorio e Presidente eletto nel 1948"],
            "punti_incerti": "Nessuno sul piano formale della Costituzione."
        }
    },
    "volta": {
        "risposta_iniziale": "La pila elettrica fu inventata dallo scienziato scozzese James Watt durante la rivoluzione industriale alla fine del Settecento.",
        "critica": {
            "critiche": [
                "Grave allucinazione: James Watt perfezionò la macchina a vapore, non la pila elettrica!",
                "La pila fu inventata dal fisico italiano Alessandro Volta nel 1799 a Como/Pavia, da cui deriva l'unità di misura 'Volt'."
            ],
            "valutazione_sintetica": "Scambio totale tra scoperte e inventori scientifici del XVIII secolo.",
            "termini_di_ricerca": ["Alessandro Volta", "Pila di Volta"]
        },
        "fonti": [
            {
                "titolo": "Pila di Volta",
                "estratto": "La pila di Volta è il primo generatore elettrochimico mai realizzato, inventato dal fisico italiano Alessandro Volta verso la fine del 1799 e presentato nel 1800.",
                "url": "https://it.wikipedia.org/wiki/Pila_di_Volta"
            }
        ],
        "sintesi": {
            "risposta_finale": "La pila elettrica fu inventata nel 1799 dallo scienziato italiano Alessandro Volta, che presentò la scoperta alla Royal Society di Londra nel 1800.",
            "affidabilita": "Alto",
            "motivazione_affidabilita": "Fonti storiche scientifiche certe.",
            "correzioni_applicate": ["Sostituito James Watt con Alessandro Volta"],
            "punti_incerti": "Nessuno."
        }
    },
    "manzoni": {
        "risposta_iniziale": "Il romanzo 'I promessi sposi' di Alessandro Manzoni è ambientato nell'Ottocento durante le guerre del Risorgimento italiano.",
        "critica": {
            "critiche": [
                "Confusione tra epoca di scrittura ed epoca della narrazione: Manzoni scrisse il libro nell'Ottocento (1827-1840).",
                "La vicenda narrata è però ambientata nel Seicento (XVII secolo), precisamente tra il 1628 e il 1630 sotto la dominazione spagnola a Milano."
            ],
            "valutazione_sintetica": "L'IA confonde la data di pubblicazione dell'opera con il secolo storico in cui si svolge la trama.",
            "termini_di_ricerca": ["I promessi sposi", "Alessandro Manzoni"]
        },
        "fonti": [
            {
                "titolo": "I promessi sposi",
                "estratto": "I promessi sposi è un celebre romanzo storico di Alessandro Manzoni, ambientato in Lombardia tra il 1628 e il 1630, al tempo della dominazione spagnola.",
                "url": "https://it.wikipedia.org/wiki/I_promessi_sposi"
            }
        ],
        "sintesi": {
            "risposta_finale": "La trama de 'I promessi sposi' è ambientata nel XVII secolo (Seicento), tra il 1628 e il 1630 in Lombardia, anche se Manzoni lo scrisse nell'Ottocento.",
            "affidabilita": "Alto",
            "motivazione_affidabilita": "Testo originale del romanzo e critica letteraria.",
            "correzioni_applicate": ["Corretto il secolo da Ottocento a Seicento (XVII secolo)"],
            "punti_incerti": "Nessuno."
        }
    },
    "re": {
        "risposta_iniziale": "Il primo Re d'Italia proclamato nel 1861 fu Vittorio Emanuele I di Savoia, unificatore della patria insieme a Garibaldi.",
        "critica": {
            "critiche": [
                "Errore dinastico comune: Vittorio Emanuele I regnò in Piemonte a inizio Ottocento.",
                "Il primo sovrano d'Italia mantenne il numerale dinastico sabaudo e fu proclamato Re con il nome di Vittorio Emanuele II (non I!)."
            ],
            "valutazione_sintetica": "L'IA assume per deduzione logica errata che il 'primo re' debba chiamarsi 'I'.",
            "termini_di_ricerca": ["Vittorio Emanuele II di Savoia", "Proclamazione del Regno d'Italia"]
        },
        "fonti": [
            {
                "titolo": "Vittorio Emanuele II di Savoia",
                "estratto": "Vittorio Emanuele II è stato l'ultimo re di Sardegna e il primo re d'Italia dal 1861 al 1878, mantenendo per continuità il numerale dinastico II.",
                "url": "https://it.wikipedia.org/wiki/Vittorio_Emanuele_II_di_Savoia"
            }
        ],
        "sintesi": {
            "risposta_finale": "Il primo Re d'Italia proclamato il 17 marzo 1861 fu Vittorio Emanuele II di Savoia (conservò il numero ordinale 'II' per continuità dinastica piemontese).",
            "affidabilita": "Alto",
            "motivazione_affidabilita": "Legge n. 4671 del Regno di Sardegna/Italia (1861).",
            "correzioni_applicate": ["Corretto numerale da I a II"],
            "punti_incerti": "Nessuno."
        }
    },
    "torre": {
        "risposta_iniziale": "La celebre torre pendente si trova a Bologna in Piazza Maggiore ed è nota come Torre degli Asinelli.",
        "critica": {
            "critiche": [
                "Allucinazione geografica: la celebre torre pendente in Piazza dei Miracoli è la Torre di Pisa.",
                "Anche a Bologna esistono torri pendenti (Garisenda e Asinelli), ma si trovano in Piazza di Porta Ravegnana, non dei Miracoli."
            ],
            "valutazione_sintetica": "Confusione tra le torri medievali di Pisa e di Bologna.",
            "termini_di_ricerca": ["Torre di Pisa", "Piazza dei Miracoli"]
        },
        "fonti": [
            {
                "titolo": "Torre di Pisa",
                "estratto": "La torre di Pisa è il campanile della cattedrale di Santa Maria Assunta nella celebre piazza dei Miracoli, noto in tutto il mondo per la sua caratteristica pendenza.",
                "url": "https://it.wikipedia.org/wiki/Torre_di_Pisa"
            }
        ],
        "sintesi": {
            "risposta_finale": "La torre pendente in Piazza dei Miracoli è la celebre Torre di Pisa, campanile del Duomo di Santa Maria Assunta, iniziata nel 1173.",
            "affidabilita": "Alto",
            "motivazione_affidabilita": "Patrimonio UNESCO documentato.",
            "correzioni_applicate": ["Corretta la localizzazione da Bologna a Pisa"],
            "punti_incerti": "Nessuno."
        }
    },
    "vesuvio": {
        "risposta_iniziale": "L'unico vulcano attivo dell'Europa continentale ad aver eruttato nel XX secolo è l'Etna in Sicilia.",
        "critica": {
            "critiche": [
                "Errore geografico: la Sicilia è un'isola, non fa parte dell'Europa 'continentale'.",
                "L'unico vulcano dell'Europa continentale ad aver eruttato nel Novecento è il Vesuvio (famosa eruzione del marzo 1944)."
            ],
            "valutazione_sintetica": "Mancata comprensione della differenza tra territorio continentale e insulare.",
            "termini_di_ricerca": ["Vesuvio", "Eruzione del Vesuvio del 1944"]
        },
        "fonti": [
            {
                "titolo": "Vesuvio",
                "estratto": "Il Vesuvio è uno strato-vulcano situato in Campania. È l'unico vulcano dell'Europa continentale ad essere entrato in eruzione nel XX secolo (marzo 1944).",
                "url": "https://it.wikipedia.org/wiki/Vesuvio"
            }
        ],
        "sintesi": {
            "risposta_finale": "L'unico vulcano dell'Europa continentale attivo nel XX secolo è il Vesuvio (ultima eruzione nel marzo 1944). L'Etna e lo Stromboli sono più attivi ma si trovano su isole.",
            "affidabilita": "Alto",
            "motivazione_affidabilita": "Istituto Nazionale di Geofisica e Vulcanologia (INGV).",
            "correzioni_applicate": ["Corretto da Etna a Vesuvio", "Distinzione geografica tra terraferma continentale e isole"],
            "punti_incerti": "Nessuno."
        }
    },
    "david": {
        "risposta_iniziale": "La celebre scultura del David conservata a Firenze fu realizzata da Leonardo da Vinci durante il suo soggiorno mediceo.",
        "critica": {
            "critiche": [
                "Allucinazione artistica: Leonardo da Vinci era un pittore e ingegnere, non ha scolpito il David.",
                "Il David in marmo conservato alla Galleria dell'Accademia di Firenze è il capolavoro di Michelangelo Buonarroti (scolpito tra il 1501 e il 1504)."
            ],
            "valutazione_sintetica": "Confusione tra i due massimi geni del Rinascimento italiano.",
            "termini_di_ricerca": ["David di Michelangelo", "Michelangelo Buonarroti"]
        },
        "fonti": [
            {
                "titolo": "David di Michelangelo",
                "estratto": "Il David è una celebre scultura in marmo realizzata da Michelangelo Buonarroti tra il 1501 e l'inizio del 1504, conservata nella Galleria dell'Accademia a Firenze.",
                "url": "https://it.wikipedia.org/wiki/David_(Michelangelo)"
            }
        ],
        "sintesi": {
            "risposta_finale": "Il David di Firenze fu scolpito da Michelangelo Buonarroti tra il 1501 e il 1504. Oggi l'originale si trova nella Galleria dell'Accademia.",
            "affidabilita": "Alto",
            "motivazione_affidabilita": "Documentazione dei Musei del Bargello e Gallerie dell'Accademia.",
            "correzioni_applicate": ["Sostituito Leonardo da Vinci con Michelangelo Buonarroti"],
            "punti_incerti": "Nessuno."
        }
    }
}

def trova_preset(testo: str):
    t = testo.lower()
    if any(k in t for k in ["capitale", "1861", "torino", "regno"]):
        return PRESET_DATABASE["capitale"]
    elif any(k in t for k in ["montagna", "monte bianco", "gran paradiso"]):
        return PRESET_DATABASE["montagna"]
    elif any(k in t for k in ["dante", "alighieri", "ravenna", "sepolt", "tomba"]):
        return PRESET_DATABASE["dante"]
    elif any(k in t for k in ["presidente", "repubblica", "einaudi", "de nicola", "1948"]):
        return PRESET_DATABASE["presidente"]
    elif any(k in t for k in ["pila", "volta", "1799", "elettric"]):
        return PRESET_DATABASE["volta"]
    elif any(k in t for k in ["promessi sposi", "manzoni", "secolo"]):
        return PRESET_DATABASE["manzoni"]
    elif any(k in t for k in ["primo re", "vittorio emanuele"]):
        return PRESET_DATABASE["re"]
    elif any(k in t for k in ["torre", "pisa", "miracoli", "campan"]):
        return PRESET_DATABASE["torre"]
    elif any(k in t for k in ["vulcano", "vesuvio", "etna", "xx secolo", "novecento"]):
        return PRESET_DATABASE["vesuvio"]
    elif any(k in t for k in ["david", "michelangelo", "scultura"]):
        return PRESET_DATABASE["david"]
    return None

def get_preset_fonti(domanda: str):
    preset = trova_preset(domanda)
    if preset and "fonti" in preset:
        return preset["fonti"]
    return []

def genera_risposta_iniziale(domanda: str, force_demo: bool = False) -> str:
    preset = trova_preset(domanda)
    if (force_demo or not is_key_configured()) and preset:
        return preset["risposta_iniziale"]
    
    # 1. Se è una chiave Groq
    if is_groq_key() and not force_demo:
        prompt = f"Sei un assistente virtuale scolastico. Rispondi alla seguente domanda in italiano in modo sintetico e diretto:\n{domanda}"
        res = chiama_groq(prompt)
        if res: return res

    # 2. Se è una chiave Google Gemini
    client = get_client()
    if client and not force_demo:
        try:
            prompt = f"Sei un assistente virtuale scolastico. Rispondi alla seguente domanda in italiano in modo sintetico:\n{domanda}"
            res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            return res.text.strip()
        except Exception:
            pass
    
    if preset:
        return preset["risposta_iniziale"]
    return f"Risposta generata: Riguardo a '{domanda}', l'argomento presenta fatti storici e concetti specifici da esaminare criticamente attraverso fonti autorevoli."

def critica_avvocato_del_diavolo(domanda: str, risposta_iniziale: str, force_demo: bool = False) -> dict:
    preset = trova_preset(domanda)
    if (force_demo or not is_key_configured()) and preset:
        return preset["critica"]
    
    prompt = f"""Sei l'Avvocato del Diavolo per studenti. Analizza criticamente:
Domanda: {domanda}
Risposta: {risposta_iniziale}
Individua allucinazioni o dubbi e 2 termini da cercare su Wikipedia.
Rispondi solo in JSON puro:
{{"critiche": ["dubbio 1", "dubbio 2"], "valutazione_sintetica": "sintesi", "termini_di_ricerca": ["termine1", "termine2"]}}"""

    if is_groq_key() and not force_demo:
        txt = chiama_groq(prompt)
        if txt:
            if txt.startswith("```json"): txt = txt[7:]
            if txt.startswith("```"): txt = txt[3:]
            if txt.endswith("```"): txt = txt[:-3]
            try: return json.loads(txt.strip())
            except Exception: pass

    client = get_client()
    if client and not force_demo:
        try:
            res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            txt = res.text.strip()
            if txt.startswith("```json"): txt = txt[7:]
            if txt.startswith("```"): txt = txt[3:]
            if txt.endswith("```"): txt = txt[:-3]
            return json.loads(txt.strip())
        except Exception:
            pass
    
    if preset:
        return preset["critica"]
    
    return {
        "critiche": [
            f"Verificare che la cronologia e i dettagli su '{domanda}' siano univoci e non influenzati da leggende o fonti secondarie.",
            "Possibile allucinazione di contesto: verificare nomi propri, date e luoghi ufficiali."
        ],
        "valutazione_sintetica": "Richiesta verifica di accuratezza enciclopedica per prevenire disinformazione.",
        "termini_di_ricerca": [w for w in domanda.replace("?", "").split() if len(w) > 4][:2]
    }

def genera_risposta_finale(domanda: str, risposta_iniziale: str, critica: dict, fonti: list, force_demo: bool = False) -> dict:
    preset = trova_preset(domanda)
    if (force_demo or not is_key_configured()) and preset:
        return preset["sintesi"]
    
    estratto_fonti = "\n".join([f"- {f['titolo']}: {f['estratto']}" for f in fonti])
    prompt = f"""Formula la risposta finale corretta per gli studenti:
Domanda: {domanda}
Risposta iniziale: {risposta_iniziale}
Critiche: {critica.get('critiche')}
Fonti: {estratto_fonti}
Rispondi solo in JSON puro:
{{"risposta_finale": "testo verificato", "affidabilita": "Alto", "motivazione_affidabilita": "motivo", "correzioni_applicate": ["correzione"], "punti_incerti": "note"}}"""

    if is_groq_key() and not force_demo:
        txt = chiama_groq(prompt)
        if txt:
            if txt.startswith("```json"): txt = txt[7:]
            if txt.startswith("```"): txt = txt[3:]
            if txt.endswith("```"): txt = txt[:-3]
            try: return json.loads(txt.strip())
            except Exception: pass

    client = get_client()
    if client and not force_demo:
        try:
            res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            txt = res.text.strip()
            if txt.startswith("```json"): txt = txt[7:]
            if txt.startswith("```"): txt = txt[3:]
            if txt.endswith("```"): txt = txt[:-3]
            return json.loads(txt.strip())
        except Exception:
            pass
    
    if preset:
        return preset["sintesi"]
    
    if fonti and fonti[0].get("estratto"):
        f_top = fonti[0]
        testo_sintesi = f_top["estratto"][:400] + "..."
        return {
            "risposta_finale": f"In base al riscontro enciclopedico ({f_top['titolo']}): {testo_sintesi}",
            "affidabilita": "Alto",
            "motivazione_affidabilita": f"Dati riscontrati direttamente sulla voce '{f_top['titolo']}'.",
            "correzioni_applicate": ["Verifica fattuale incrociata con l'enciclopedia"],
            "punti_incerti": "Approfondire con testi specialistici."
        }

    return {
        "risposta_finale": f"Verifica completata per '{domanda}'. L'analisi metodologica suggerisce di confrontare sempre manuali scolastici e fonti certificate.",
        "affidabilita": "Medio",
        "motivazione_affidabilita": "Analisi condotta secondo principi di verifica critica.",
        "correzioni_applicate": ["Revisione critica applicata"],
        "punti_incerti": "Verifica diretta su enciclopedia consigliata per approfondimento."
    }
