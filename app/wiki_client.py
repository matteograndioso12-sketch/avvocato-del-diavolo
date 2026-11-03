import requests
from typing import List, Dict

WIKI_API_URL = "https://it.wikipedia.org/w/api.php"
HEADERS = {
    "User-Agent": "AvvocatoDelDiavoloScuola/1.0"
}

_CACHE_WIKI = {}

def cerca_wikipedia(query: str, max_risultati: int = 1) -> List[Dict[str, str]]:
    """
    Ricerca Wikipedia ultra-rapida con salvaguardia istantanea contro blocchi di rete/DNS.
    """
    if not query or not query.strip():
        return []
    
    q = query.strip()
    if q in _CACHE_WIKI:
        return _CACHE_WIKI[q]
    
    try:
        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": q,
            "gsrlimit": max_risultati,
            "prop": "extracts",
            "exintro": 1,
            "explaintext": 1,
            "format": "json",
            "utf8": 1
        }
        # Timeout brevissimo: se la rete o il DNS non risponde entro 0.8s, esce subito senza bloccare l'app
        res = requests.get(WIKI_API_URL, params=params, headers=HEADERS, timeout=0.8)
        if res.status_code == 200:
            pages = res.json().get("query", {}).get("pages", {})
            ris = []
            for _, pdata in pages.items():
                titolo = pdata.get("title", "")
                estratto = pdata.get("extract", "")[:500]
                if titolo and estratto:
                    ris.append({
                        "titolo": titolo,
                        "estratto": estratto,
                        "url": f"https://it.wikipedia.org/wiki/{titolo.replace(' ', '_')}"
                    })
            _CACHE_WIKI[q] = ris
            return ris
    except Exception:
        # Errore di connessione o timeout: non bloccare mai l'utente
        pass

    _CACHE_WIKI[q] = []
    return []
